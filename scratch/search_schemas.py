import os
import json

schema_dir = 'ui/schemas'
matches = []
for fname in os.listdir(schema_dir):
    if not fname.endswith('.json'):
        continue
    fpath = os.path.join(schema_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'agent' in content.lower() or 'specialist' in content.lower() or 'coordinator' in content.lower():
            matches.append(fname)

print("Matching schemas:")
for m in matches:
    print(m)
