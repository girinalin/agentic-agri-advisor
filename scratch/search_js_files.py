import os

terms = ['crop', 'advisory', 'freshness', 'agents']
js_dir = 'ui/agui'
results = []
for fname in os.listdir(js_dir):
    if not fname.endswith('.js'):
        continue
    fpath = os.path.join(js_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if any(t in line.lower() for t in terms):
                results.append(f"{fname}:{i+1} -> {line.strip()}")

with open('scratch/js_search_results.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
print("Done")
