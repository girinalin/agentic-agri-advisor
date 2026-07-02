import os

with open('ui/agui/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update database initialization to call updateSyncBadge()
old_init = """  // Initialize LocalDB schema and connectivity triage
  localDb.init().then(() => {
    console.log('[IndexedDB] Local DB initialized');
    checkOnlineStatus();
    checkBatteryStatus();
  });"""

new_init = """  // Initialize LocalDB schema and connectivity triage
  localDb.init().then(() => {
    console.log('[IndexedDB] Local DB initialized');
    checkOnlineStatus();
    checkBatteryStatus();
    updateSyncBadge();
  });"""

js = js.replace(old_init, new_init)

# 2. Insert updateSyncBadge definition before the export block
old_export = "// Export functions to global window for modular submodules"

badge_func = """  // Update sync queue badge count
  async function updateSyncBadge() {
    const badge = document.getElementById('sync-queue-badge');
    if (!badge) return;
    
    try {
      const count = await localDb.getPendingSyncCount();
      if (count > 0) {
        badge.style.display = 'inline-flex';
        badge.textContent = `🔄 ${count} Pending`;
      } else {
        badge.style.display = 'none';
      }
    } catch (e) {
      badge.style.display = 'none';
    }
  }

  // Export functions to global window for modular submodules"""

js = js.replace(old_export, badge_func)

# 3. Add to window exports
old_exports_end = """  window.showToast = showToast;
  window.renderLeftNavigation = renderLeftNavigation;
});"""

new_exports_end = """  window.showToast = showToast;
  window.renderLeftNavigation = renderLeftNavigation;
  window.updateSyncBadge = updateSyncBadge;
});"""

js = js.replace(old_exports_end, new_exports_end)

with open('ui/agui/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("dashboard.js updated with updateSyncBadge logic successfully.")
