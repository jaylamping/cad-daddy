#!/bin/zsh
# Keep the Mac awake while a VM on it says it is working. The other half of pc/keepawake.py.
#
#   zsh keepawake_mac.sh install     # copy to ~/.keepawake, run at every login (launchd), start now
#   zsh keepawake_mac.sh status      # watcher loaded? caffeinate running? which beats are fresh?
#   zsh keepawake_mac.sh uninstall   # stop it and remove the launchd job
#
# The VM writes ~/.keepawake/<vm name>.beat every 15 s while SolidWorks works. This watcher looks every 15 s and keeps
# one `caffeinate` running while any beat is under two minutes old, and stops it otherwise, so a VM that crashes or
# shuts down cannot keep the Mac awake for ever. No sudo needed. Its on/off log is ~/.keepawake/watch.log.
# caffeinate flags: -d display, -i idle sleep, -s system sleep on power. Override with KEEPAWAKE_FLAGS in the plist.

DIR="$HOME/.keepawake"
LABEL="com.cad-daddy.keepawake"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
FLAGS="${KEEPAWAKE_FLAGS:--dis}"

fresh_beats() { find "$DIR" -maxdepth 1 -name '*.beat' -mmin -2 2>/dev/null; }

case "$1" in
  install)
    mkdir -p "$DIR" "$HOME/Library/LaunchAgents"
    [[ "${0:A}" != "$DIR/keepawake_mac.sh" ]] && cp "${0:A}" "$DIR/keepawake_mac.sh"
    cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>/bin/zsh</string><string>$DIR/keepawake_mac.sh</string><string>watch</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$DIR/watch.log</string>
  <key>StandardErrorPath</key><string>$DIR/watch.log</string>
</dict></plist>
EOF
    launchctl bootout "gui/$UID/$LABEL" 2>/dev/null
    launchctl bootstrap "gui/$UID" "$PLIST" && echo "installed and started: $LABEL (log $DIR/watch.log)"
    ;;
  uninstall)
    launchctl bootout "gui/$UID/$LABEL" 2>/dev/null
    rm -f "$PLIST"
    echo "removed $LABEL"
    ;;
  status)
    launchctl print "gui/$UID/$LABEL" >/dev/null 2>&1 && echo "watcher: loaded" || echo "watcher: NOT loaded"
    pgrep -fl "caffeinate $FLAGS" || echo "caffeinate: not running (Mac may sleep)"
    for f in "$DIR"/*.beat(N); do echo "beat: ${f:t}: $(cat "$f")"; done
    echo "fresh beats: $(fresh_beats | wc -l | tr -d ' ')"
    ;;
  watch)
    cpid=""
    trap '[[ -n "$cpid" ]] && kill $cpid 2>/dev/null; exit 0' TERM INT
    while true; do
      if [[ -n "$(fresh_beats)" ]]; then
        if [[ -z "$cpid" ]] || ! kill -0 $cpid 2>/dev/null; then
          caffeinate ${=FLAGS} -w $$ &
          cpid=$!
          echo "$(date '+%F %T') awake: caffeinate $FLAGS (PID $cpid) for $(fresh_beats | xargs -n1 basename | tr '\n' ' ')"
        fi
      elif [[ -n "$cpid" ]]; then
        kill $cpid 2>/dev/null
        echo "$(date '+%F %T') no fresh beat: caffeinate stopped"
        cpid=""
      fi
      sleep 15
    done
    ;;
  *)
    sed -n '2,12p' "${0:A}"
    exit 2
    ;;
esac
