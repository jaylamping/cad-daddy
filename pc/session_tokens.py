"""Tokens used by a Claude Code session, read from its own session record.

    python pc/session_tokens.py <session.jsonl>
    python pc/session_tokens.py <search string> [--all] [--root DIR]

With a search string, every record under ~/.claude/projects is searched.  A
session is reported when the string is in its FIRST user message (the brief that
started it); --all reports every session that mentions it anywhere.  Prints JSON.

How the record is read (Claude Code 2.1.x):

* One API response is written as several "assistant" lines, one per content
  block, all with the same message.id and the same usage.  They are counted
  once, by message.id.
* usage.iterations, when present, lists the model calls inside that response.
  type "message" is the session's own model.  Any other type (an advisor call is
  "advisor_message") carries its own "model" and its own tokens, and is NOT in
  the top-level usage numbers.  Those are summed under that model, role
  "advisor".
* The last "cost-state" line is Claude Code's own running total for the session
  and is passed through unchanged as a cross-check.  It is written when the
  session ends, so a session still open has none.  It can be higher than the
  sums here: a request whose response never reached the record (compare
  api_requests_logged with api_responses) is in cost-state but not in the
  per-response usage, so the sums here are a lower bound.

Standard library only.  No prices are applied here.
"""
import glob
import json
import os
import sys
from datetime import datetime

FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
          "output_tokens")
IDLE_GAP_S = 300  # a gap longer than this between records is not counted as active


def _ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _first_user_text(d):
    c = (d.get("message") or {}).get("content")
    if isinstance(c, list):
        c = " ".join(b.get("text", "") for b in c if isinstance(b, dict))
    return c or ""


def _blank(role):
    t = {"role": role, "calls": 0}
    for f in FIELDS:
        t[f] = 0
    t["cache_creation_5m"] = 0
    t["cache_creation_1h"] = 0
    return t


def _add(t, u):
    t["calls"] += 1
    for f in FIELDS:
        t[f] += u.get(f) or 0
    cc = u.get("cache_creation") or {}
    t["cache_creation_5m"] += cc.get("ephemeral_5m_input_tokens") or 0
    t["cache_creation_1h"] += cc.get("ephemeral_1h_input_tokens") or 0


def read_records(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                yield json.loads(line)
            except ValueError:
                continue


def summarize(path):
    files = [path]
    side = os.path.join(os.path.splitext(path)[0], "subagents")
    files += sorted(glob.glob(os.path.join(side, "*.jsonl")))

    responses = {}       # message.id -> (model, usage, timestamp of first line)
    order = []
    stamps = []
    first_user = None
    cost_state = None
    session_id = None
    advisor_setting = set()
    advisor_blocks = 0
    api_requests = 0
    for i, f in enumerate(files):
        for d in read_records(f):
            ts = d.get("timestamp")
            if ts:
                stamps.append(ts)
            session_id = session_id or d.get("sessionId")
            typ = d.get("type")
            if typ == "api-request" and i == 0:
                api_requests += 1
            elif typ == "cost-state" and i == 0:
                cost_state = {k: v for k, v in d.items() if k not in ("type", "sessionId")}
            elif typ == "user" and first_user is None and i == 0:
                first_user = _first_user_text(d)
            elif typ == "assistant":
                m = d.get("message") or {}
                if d.get("advisorModel"):
                    advisor_setting.add(d["advisorModel"])
                for b in m.get("content") or []:
                    if b.get("type") == "server_tool_use" and b.get("name") == "advisor":
                        advisor_blocks += 1
                key = m.get("id") or d.get("uuid")
                if key not in responses:
                    order.append(key)
                    responses[key] = [m.get("model"), m.get("usage") or {}, ts, i > 0]
                else:
                    responses[key][1] = m.get("usage") or responses[key][1]

    models = {}
    advisor_calls = []
    thinking = {}
    mismatches = 0
    for key in order:
        model, u, ts, is_side = responses[key]
        its = u.get("iterations") or []
        own = [it for it in its if it.get("type") == "message"]
        t = models.setdefault(model, _blank("session"))
        if own:
            for it in own:
                _add(t, it)
            t["calls"] -= len(own) - 1          # one response, however many iterations
            t["iterations"] = t.get("iterations", 0) + len(own)
            if any(sum(it.get(f) or 0 for it in own) != (u.get(f) or 0) for f in FIELDS):
                mismatches += 1
        else:
            _add(t, u)
            t["iterations"] = t.get("iterations", 0) + 1
        thinking[model] = thinking.get(model, 0) + (
            (u.get("output_tokens_details") or {}).get("thinking_tokens") or 0)
        for n, it in enumerate(its):
            if it.get("type") == "message":
                continue
            am = it.get("model") or "(model not recorded)"
            _add(models.setdefault(am + " [" + it.get("type", "?") + "]", _blank("advisor")), it)
            before = its[n - 1] if n else {}
            advisor_calls.append({
                "timestamp": ts,
                "type": it.get("type"),
                "model": it.get("model"),
                "input_tokens": it.get("input_tokens"),
                "cache_creation_input_tokens": it.get("cache_creation_input_tokens"),
                "cache_read_input_tokens": it.get("cache_read_input_tokens"),
                "output_tokens": it.get("output_tokens"),
                "session_context_tokens_before_call": sum(
                    before.get(f) or 0 for f in FIELDS[:3]) + (before.get("output_tokens") or 0),
            })
    for model, n in thinking.items():
        models[model]["thinking_tokens"] = n

    stamps.sort()
    wall = active = None
    if stamps:
        t0, t1 = _ts(stamps[0]), _ts(stamps[-1])
        wall = round((t1 - t0).total_seconds() / 60, 1)
        prev, act = t0, 0.0
        for s in stamps[1:]:
            cur = _ts(s)
            gap = (cur - prev).total_seconds()
            if gap <= IDLE_GAP_S:
                act += gap
            prev = cur
        active = round(act / 60, 1)

    return {
        "session_id": session_id,
        "file": path,
        "subagent_files": len(files) - 1,
        "first_timestamp": stamps[0] if stamps else None,
        "last_timestamp": stamps[-1] if stamps else None,
        "wall_minutes": wall,
        "active_minutes": active,
        "active_minutes_note": "gaps over %d s between records left out" % IDLE_GAP_S,
        "first_user_message": " ".join((first_user or "").split())[:400],
        "api_requests_logged": api_requests,
        "api_responses": len(order),
        "models": models,
        "advisor": {
            "advisorModel_setting": sorted(advisor_setting),
            "server_tool_use_blocks": advisor_blocks,
            "calls_with_usage": len(advisor_calls),
            "calls": advisor_calls,
        },
        "top_level_usage_differs_from_iterations": mismatches,
        "cost_state_as_recorded": cost_state,
    }


def find(needle, root, everywhere):
    hits = []
    for f in glob.glob(os.path.join(root, "*", "*.jsonl")):
        count, in_first, seen_user = 0, False, False
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if needle not in line:
                    if not seen_user and '"type":"user"' in line.replace(" ", ""):
                        seen_user = True
                    continue
                count += line.count(needle)
                if not seen_user:
                    try:
                        d = json.loads(line)
                    except ValueError:
                        continue
                    if d.get("type") == "user":
                        seen_user = True
                        in_first = needle in _first_user_text(d)
        if count and (in_first or everywhere):
            hits.append((os.path.getmtime(f), f, count, in_first))
    return [h[1:] for h in sorted(hits)]


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    root = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
        args = [a for a in args if a != root]
    if len(args) != 1:
        sys.stderr.write(__doc__)
        return 2
    target = args[0]
    if os.path.isfile(target):
        out = summarize(target)
    else:
        out = {"search": target, "sessions": []}
        for f, count, in_first in find(target, root, "--all" in argv):
            s = summarize(f)
            s["search_hits"] = count
            s["search_in_first_user_message"] = in_first
            out["sessions"].append(s)
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
