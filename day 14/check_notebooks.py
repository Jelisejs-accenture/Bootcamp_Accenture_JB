from pathlib import Path
import ast, nbformat
folder = Path(__file__).parent
for f in sorted(folder.glob('*.ipynb')):
    nb = nbformat.read(str(f), as_version=4)
    nbformat.validate(nb)
    n = 0
    for c in nb.cells:
        if c.cell_type == 'code':
            src = '\n'.join(line for line in c.source.splitlines() if not line.lstrip().startswith('%'))
            compile(src, str(f), 'exec', flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
            n += 1
    print(f'PASS {f.name}: {n} Python code cells parsed')
print('Static checks complete. Dynamic agent calls still require local execution.')
