import os

with open('ui/agui/dashboard.js', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'updatesyncbadge' in line.lower():
            print(f"{i+1}: {line.strip()}")
