import os

with open('ui/agui/local_db.js', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'getpending' in line.lower():
            print(f"{i+1}: {line.strip()}")
