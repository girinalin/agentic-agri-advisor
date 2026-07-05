import os

search_terms = ['agents-list', 'agent-list', 'specialist', 'status-indicator', 'agents_status', 'agent-status', 'agents-status']

results = []
with open('ui/agui/dashboard.js', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if any(term in line for term in search_terms):
            results.append(f"{i+1}: {line.strip()}")

os.makedirs('scratch', exist_ok=True)
with open('scratch/search_results.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
print("Search complete.")
