"""judge() copied verbatim from solidworks/swfea.py by source extraction (swfea imports Windows modules)."""
import ast, pathlib
src = pathlib.Path('solidworks/swfea.py').read_text(encoding='utf-8')
tree = ast.parse(src)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'judge')
code = ast.get_source_segment(src, fn)
class Failed(Exception): pass
LOG = []
def log(s): LOG.append(s)
ns = dict(Failed=Failed, log=log)
exec(code, ns)
judge = ns['judge']
