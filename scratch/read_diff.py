import subprocess

diff = subprocess.check_output(['git', 'diff'], text=True)
lines = diff.split('\n')
for i, line in enumerate(lines):
    if 'updatesyncbadge' in line.lower():
        start = max(0, i - 10)
        end = min(len(lines), i + 10)
        print(f"--- Context {i} ---")
        for j in range(start, end):
            print(lines[j])
