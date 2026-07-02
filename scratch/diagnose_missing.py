import os
import json
import ast
import re

with open('ui/agui/translations.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

def parse_js_dict(js_code, dict_name):
    match = re.search(dict_name + r'\s*=\s*(\{[\s\S]*?\n\s*\});', js_code)
    if not match:
        match = re.search(dict_name + r'\s*=\s*(\{[\s\S]*?\n\s*\})', js_code)
    dict_str = match.group(1)
    dict_str = re.sub(r'//.*', '', dict_str)
    return ast.literal_eval(dict_str)

translations = parse_js_dict(js_code, 'TRANSLATIONS')
schema_translations = parse_js_dict(js_code, 'SCHEMA_TRANSLATIONS')

# Get all keys referenced in schemas
keys = set()
schema_dir = 'ui/schemas'
for fname in os.listdir(schema_dir):
    if not fname.endswith('.json'):
        continue
    with open(os.path.join(schema_dir, fname), 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    def recurse(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.endswith('Key') and isinstance(v, str):
                    keys.add(v)
                elif k in ['titleKey', 'descriptionKey', 'labelKey', 'placeholderKey', 'textKey', 'descKey', 'valueKey'] and isinstance(v, str):
                    keys.add(v)
                else:
                    recurse(v)
        elif isinstance(o, list):
            for item in o:
                recurse(item)
    recurse(data)

print(f"Total schema keys: {len(keys)}")
# Show missing keys for each language
for lang in ['en', 'hi', 'mr', 'te', 'sw']:
    missing = []
    for k in keys:
        in_schema = k in schema_translations[lang]
        in_layout = k in translations[lang]
        if not in_schema and not in_layout:
            missing.append(k)
    print(f"Language '{lang}' missing: {len(missing)} keys")
    if missing:
        print("Sample missing keys:", missing[:10])
