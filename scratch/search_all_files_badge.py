import os

terms = ['updatesyncbadge']
results = []
for root, dirs, files in os.walk('.'):
    # Skip standard directories
    if '.git' in root or '.venv' in root or 'node_modules' in root or '.gemini' in root:
        continue
    for fname in files:
        if fname.endswith(('.js', '.html', '.css', '.py')):
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if any(t in line.lower() for t in terms):
                            results.append(f"{fpath}:{i+1} -> {line.strip()}")
            except Exception:
                pass

print("Search results:")
for r in results:
    print(r)
