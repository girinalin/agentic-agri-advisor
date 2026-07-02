import subprocess

diff = subprocess.check_output(['git', 'diff', 'ui/agui/dashboard.js'], text=True)
print(diff)
