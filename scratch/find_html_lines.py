import os

results = []
with open('ui/agui/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'agent' in line.lower() or 'specialist' in line.lower():
            results.append(f"{i+1}: {line.strip()}")

with open('scratch/search_results_html.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
print("Search complete.")
