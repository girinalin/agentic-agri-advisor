import os
import json
import re

schema_dir = 'ui/schemas'
translations_path = 'ui/agui/translations.js'

schema_keys = set()
for fname in os.listdir(schema_dir):
    if not fname.endswith('.json'):
        continue
    fpath = os.path.join(schema_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            continue
        
        def find_keys(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k.endswith('Key') and isinstance(v, str):
                        schema_keys.add(v)
                    elif isinstance(v, (dict, list)):
                        find_keys(v)
            elif isinstance(obj, list):
                for item in obj:
                    find_keys(item)
                    
        find_keys(data)

with open(translations_path, 'r', encoding='utf-8') as f:
    translations_content = f.read()

missing_keys = []
for key in sorted(list(schema_keys)):
    # Check if key is defined in translations_content
    # e.g., 'key': or "key":
    pattern = rf"['\"]{re.escape(key)}['\"]\s*:"
    if not re.search(pattern, translations_content):
        missing_keys.append(key)

print(f"Total schema keys: {len(schema_keys)}")
print(f"Missing from translations.js: {len(missing_keys)}")
print("First 50 missing keys:")
for mk in missing_keys[:50]:
    print(mk)
