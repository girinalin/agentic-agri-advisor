filepath = "/Users/nalin.giri/workspaces/agentic-agri-advisor/ui/agui/dashboard.js"
with open(filepath, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# 1. Add expert route translations to TRANSLATIONS dictionary programmatically
translations_to_add = {
    'English': {
        'nav_console': '💻 Console',
        'nav_consultations': '📥 Consultations',
        'nav_outbreak': '🚨 Regional Intel',
        'nav_governance': '📖 Governance',
        'nav_evaluation': '📊 Evaluation',
        'nav_audit': '🔍 Audit Logs',
        'nav_settings': '⚙️ Settings'
    },
    'Hindi': {
        'nav_console': '💻 कंसोल',
        'nav_consultations': '📥 परामर्श',
        'nav_outbreak': '🚨 क्षेत्रीय खुफिया',
        'nav_governance': '📖 ज्ञान शासन',
        'nav_evaluation': '📊 मूल्यांकन',
        'nav_audit': '🔍 ऑडिट लॉग',
        'nav_settings': '⚙️ सेटिंग्स'
    },
    'Marathi': {
        'nav_console': '💻 कन्सोल',
        'nav_consultations': '📥 सल्लामसलत',
        'nav_outbreak': '🚨 प्रादेशिक माहिती',
        'nav_governance': '📖 ज्ञान नियंत्रण',
        'nav_evaluation': '📊 मूल्यांकन',
        'nav_audit': '🔍 ऑडिट लॉग',
        'nav_settings': '⚙️ सेटिंग्ज'
    },
    'Swahili': {
        'nav_console': '💻 Dashibodi',
        'nav_consultations': '📥 Mashauriano',
        'nav_outbreak': '🚨 Ujasusi wa Kikanda',
        'nav_governance': '📖 Utawala wa Maarifa',
        'nav_evaluation': '📊 Tathmini',
        'nav_audit': '🔍 Ukaguzi',
        'nav_settings': '⚙️ Mipangilio'
    },
    'Telugu': {
        'nav_console': '💻 కన్సోల్',
        'nav_consultations': '📥 సంప్రదింపులు',
        'nav_outbreak': '🚨 ప్రాంతీయ నిఘా',
        'nav_governance': '📖 విజ్ఞాన పరిపాలన',
        'nav_evaluation': '📊 మూల్యాంకనం',
        'nav_audit': '🔍 ఆడిట్ లాగ్స్',
        'nav_settings': '⚙️ సెట్టింగులు'
    }
}

for lang, keys in translations_to_add.items():
    target_pattern = f"'{lang}': {{"
    if target_pattern not in content:
        target_pattern = f'"{lang}": {{'

    inject_str = ""
    for k, v in keys.items():
        inject_str += f"\n      '{k}': '{v}',"

    content = content.replace(target_pattern, target_pattern + inject_str)

# 2. Inject left navigation data sections and Dynamic Rendering helpers inside DOMContentLoaded
nav_helpers_js = """
  // Phase 5: Collapsible Navigation Setup
  const NAV_SECTIONS = {
    farmer: [
      { id: 'home', icon: '🏠', trKey: 'nav_home' },
      { id: 'farm', icon: '🌱', trKey: 'nav_farm' },
      { id: 'ask', icon: '🎙️', trKey: 'nav_ask' },
      { id: 'market', icon: '📈', trKey: 'nav_market' },
      { id: 'more', icon: '📋', trKey: 'nav_more' }
    ],
    expert: [
      { id: 'console', icon: '💻', trKey: 'nav_console' },
      { id: 'consultations', icon: '📥', trKey: 'nav_consultations' },
      { id: 'outbreak', icon: '🚨', trKey: 'nav_outbreak' },
      { id: 'governance', icon: '📖', trKey: 'nav_governance' },
      { id: 'evaluation', icon: '📊', trKey: 'nav_evaluation' },
      { id: 'audit', icon: '🔍', trKey: 'nav_audit' },
      { id: 'settings', icon: '⚙️', trKey: 'nav_settings' }
    ]
  };

  // Traps keyboard focus inside the drawer element
  function trapFocus(element) {
    const focusableElements = element.querySelectorAll('button, [href], input, select, textarea, [tabindex="0"]');
    if (focusableElements.length === 0) return;
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', function(e) {
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          if (document.activeElement === firstFocusable) {
            lastFocusable.focus();
            e.preventDefault();
          }
        } else {
          if (document.activeElement === lastFocusable) {
            firstFocusable.focus();
            e.preventDefault();
          }
        }
      }
    });
  }

  function renderLeftNavigation(mode = 'farmer') {
    const list = document.getElementById('left-nav-links-list');
    if (!list) return;
    list.innerHTML = '';

    const lang = document.getElementById('language-selector')?.value || 'English';
    const dict = TRANSLATIONS[lang] || TRANSLATIONS['English'];
    const items = NAV_SECTIONS[mode] || NAV_SECTIONS['farmer'];

    items.forEach(item => {
      const label = dict[item.trKey] || item.trKey;
      const link = document.createElement('a');
      link.href = '#';
      link.className = 'left-nav-item';
      link.setAttribute('data-tab', item.id);
      link.setAttribute('title', label); // tooltip for collapsed mode
      link.setAttribute('aria-label', label);

      const currentActive = localStorage.getItem('nav_route_user') || (mode === 'expert' ? 'console' : 'home');
      if (item.id === currentActive) {
        link.classList.add('active');
      }

      link.innerHTML = `
        <span class="nav-icon">${item.icon}</span>
        <span class="nav-label">${label}</span>
      `;

      link.addEventListener('click', (e) => {
        e.preventDefault();
        window.switchTab(item.id);
      });

      list.appendChild(link);
    });

    // Translate profile labels in footer
    const profileName = document.getElementById('left-nav-profile-name');
    if (profileName) {
      profileName.textContent = mode === 'expert' ? 'Dr. Agronomist' : 'माधव जी';
    }
  }

  // Collapsible toggle buttons event setup
  const leftNavToggleBtn = document.getElementById('left-nav-toggle-btn');
  const leftNav = document.getElementById('left-nav');

  if (leftNavToggleBtn && leftNav) {
    // Restore collapsed preference
    const isCollapsed = localStorage.getItem('nav_collapsed_user') === 'true';
    if (isCollapsed) {
      leftNav.classList.add('collapsed');
      document.documentElement.style.setProperty('--sidebar-width', '72px');
      leftNavToggleBtn.setAttribute('aria-expanded', 'false');
      leftNavToggleBtn.textContent = '▶';
    } else {
      leftNavToggleBtn.setAttribute('aria-expanded', 'true');
      leftNavToggleBtn.textContent = '◀';
    }

    leftNavToggleBtn.addEventListener('click', () => {
      const collapsed = leftNav.classList.toggle('collapsed');
      localStorage.setItem('nav_collapsed_user', collapsed);
      document.documentElement.style.setProperty('--sidebar-width', collapsed ? '72px' : '232px');
      leftNavToggleBtn.setAttribute('aria-expanded', !collapsed);
      leftNavToggleBtn.textContent = collapsed ? '▶' : '◀';
    });
  }

  // Tablet portrait drawer menu button setup
  const menuToggleBtn = document.getElementById('menu-toggle-btn');
  const leftNavBackdrop = document.getElementById('left-nav-backdrop');
  if (menuToggleBtn && leftNav) {
    menuToggleBtn.addEventListener('click', () => {
      leftNav.classList.add('drawer-open');
      if (leftNavBackdrop) leftNavBackdrop.classList.add('active');
      trapFocus(leftNav);
      // focus the first element inside left-nav
      const firstBtn = leftNav.querySelector('button, a');
      if (firstBtn) firstBtn.focus();
    });
  }

  if (leftNavBackdrop && leftNav) {
    leftNavBackdrop.addEventListener('click', () => {
      leftNav.classList.remove('drawer-open');
      leftNavBackdrop.classList.remove('active');
      if (menuToggleBtn) menuToggleBtn.focus();
    });
  }

  // Escape key handler for drawer closing
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && leftNav && leftNav.classList.contains('drawer-open')) {
      leftNav.classList.remove('drawer-open');
      if (leftNavBackdrop) leftNavBackdrop.classList.remove('active');
      if (menuToggleBtn) menuToggleBtn.focus();
    }
  });
"""

# Let's insert nav_helpers_js inside DOMContentLoaded (right before the mode selector block)
content = content.replace("  // User Mode selector change listener", nav_helpers_js + "\n  // User Mode selector change listener")

# 3. Replace applyLanguageTranslation to update left navigation links as well
apply_translation_orig = """  function applyLanguageTranslation(lang) {
    const dict = TRANSLATIONS[lang] || TRANSLATIONS['English'];

    // Translate bottom navigation labels
    const labels = document.querySelectorAll('.bottom-nav-bar [data-tr]');
    labels.forEach(lbl => {
      const key = lbl.getAttribute('data-tr');
      if (dict[key]) {
        lbl.textContent = dict[key];
      }
    });"""

apply_translation_new = """  function applyLanguageTranslation(lang) {
    const dict = TRANSLATIONS[lang] || TRANSLATIONS['English'];

    // Translate bottom navigation labels
    const labels = document.querySelectorAll('.bottom-nav-bar [data-tr]');
    labels.forEach(lbl => {
      const key = lbl.getAttribute('data-tr');
      if (dict[key]) {
        lbl.textContent = dict[key];
      }
    });

    // Re-render left nav to apply language translations immediately
    const currentMode = document.getElementById('user-mode-selector')?.value || 'farmer';
    renderLeftNavigation(currentMode);"""

content = content.replace(apply_translation_orig, apply_translation_new)

# 4. Replace switchTab routing implementation to handle expert routes, state preservation and left-nav highlighting
switch_tab_orig = """  window.switchTab = function(tabId, skipLoadSchema) {
    console.log(`[Navigation] Switching to screen tab: ${tabId}`);

    // Remove active styles from bottom nav links
    const tabs = document.querySelectorAll('.bottom-nav-bar .nav-tab');
    tabs.forEach(t => t.classList.remove('active'));

    // Highlight the selected bottom nav tab
    const targetTab = document.querySelector(`.bottom-nav-bar .nav-tab[data-tab="${tabId}"]`);
    if (targetTab) targetTab.classList.add('active');

    // Hide all screen contents
    const screens = document.querySelectorAll('.screen-container .app-screen');
    screens.forEach(s => s.classList.remove('active'));

    // Show active screen content
    const targetScreen = document.getElementById(`screen-${tabId}`);
    if (targetScreen) targetScreen.classList.add('active');

    if (!skipLoadSchema) {
      // Dynamically trigger corresponding schema loads
      if (tabId === 'home') {
        loadSchema('home_today', 'home-canvas');
      } else if (tabId === 'farm') {
        loadSchema('my_farm_summary', 'farm-canvas');
      } else if (tabId === 'market') {
        loadSchema('market_insights', 'market-canvas');
      } else if (tabId === 'more') {
        loadSchema('more_screen', 'more-canvas');
      }
    }
  };"""

switch_tab_new = """  window.switchTab = function(tabId, skipLoadSchema) {
    console.log(`[Navigation] Switching to screen tab: ${tabId}`);

    // Save route selection
    localStorage.setItem('nav_route_user', tabId);

    // Close the tablet drawer if open
    const leftNav = document.getElementById('left-nav');
    const backdrop = document.getElementById('left-nav-backdrop');
    if (leftNav && leftNav.classList.contains('drawer-open')) {
      leftNav.classList.remove('drawer-open');
      if (backdrop) backdrop.classList.remove('active');
      const menuToggle = document.getElementById('menu-toggle-btn');
      if (menuToggle) menuToggle.focus();
    }

    // Remove active styles from bottom nav links
    const tabs = document.querySelectorAll('.bottom-nav-bar .nav-tab');
    tabs.forEach(t => t.classList.remove('active'));

    // Highlight the selected bottom nav tab
    const targetTab = document.querySelector(`.bottom-nav-bar .nav-tab[data-tab="${tabId}"]`);
    if (targetTab) targetTab.classList.add('active');

    // Highlight left nav tab
    const leftTabs = document.querySelectorAll('.left-nav-item');
    leftTabs.forEach(t => t.classList.remove('active'));
    const targetLeftTab = document.querySelector(`.left-nav-item[data-tab="${tabId}"]`);
    if (targetLeftTab) targetLeftTab.classList.add('active');

    // Hide all screen contents
    const screens = document.querySelectorAll('.screen-container .app-screen');
    screens.forEach(s => s.classList.remove('active'));

    // Show active screen content
    const targetScreen = document.getElementById(`screen-${tabId}`);
    if (targetScreen) targetScreen.classList.add('active');

    if (!skipLoadSchema) {
      // Dynamically trigger corresponding schema loads
      if (tabId === 'home') {
        loadSchema('home_today', 'home-canvas');
      } else if (tabId === 'farm') {
        loadSchema('my_farm_summary', 'farm-canvas');
      } else if (tabId === 'market') {
        loadSchema('market_insights', 'market-canvas');
      } else if (tabId === 'more') {
        loadSchema('more_screen', 'more-canvas');
      } else if (tabId === 'console') {
        renderExpertConsole();
      } else if (tabId === 'consultations') {
        loadSchema('expert_request_status', 'consultations-canvas');
      } else if (tabId === 'outbreak') {
        loadSchema('regional_risk_map', 'outbreak-canvas');
      } else if (tabId === 'governance') {
        renderGovernanceDashboard();
      } else if (tabId === 'evaluation') {
        renderEvaluationDashboard();
      } else if (tabId === 'audit') {
        renderAuditDashboard();
      } else if (tabId === 'settings') {
        loadSchema('privacy_preferences', 'settings-canvas');
      }
    }
  };"""

content = content.replace(switch_tab_orig, switch_tab_new)

# 5. Update user-mode-selector change listener
mode_selector_orig = """  // User Mode selector change listener
  const modeSelector = document.getElementById('user-mode-selector');
  if (modeSelector) {
    modeSelector.addEventListener('change', (e) => {
      const mode = e.target.value;
      if (mode === 'expert') {
        renderExpertConsole();
      } else {
        window.switchTab('home');
      }
    });
  }"""

mode_selector_new = """  // User Mode selector change listener
  const modeSelector = document.getElementById('user-mode-selector');
  if (modeSelector) {
    // Restore mode preference on boot
    const savedMode = localStorage.getItem('nav_mode_user') || 'farmer';
    modeSelector.value = savedMode;
    renderLeftNavigation(savedMode);

    // Switch to last active route
    const savedRoute = localStorage.getItem('nav_route_user') || (savedMode === 'expert' ? 'console' : 'home');
    setTimeout(() => {
      window.switchTab(savedRoute);
    }, 100);

    modeSelector.addEventListener('change', (e) => {
      const mode = e.target.value;
      localStorage.setItem('nav_mode_user', mode);
      renderLeftNavigation(mode);
      if (mode === 'expert') {
        window.switchTab('console');
      } else {
        window.switchTab('home');
      }
    });
  }"""

content = content.replace(mode_selector_orig, mode_selector_new)

# 6. Add Custom Dashboards renderers for expert pages: Governance, Evaluation, Audit
custom_dashboards_js = """
  // Custom Dynamic Renderers for Expert screens
  async function renderGovernanceDashboard() {
    const canvas = document.getElementById('governance-canvas');
    if (!canvas) return;

    canvas.innerHTML = `
      <div class="card" style="padding: 1.5rem;">
        <h2>📖 OKF Knowledge Governance</h2>
        <p>Review active agricultural guidance articles, source credentials, applicability filters, and perform content version rollbacks.</p>
        <div style="margin-top: 15px; overflow-x: auto;">
          <table class="app-table" style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid var(--border); padding-bottom: 8px;">
                <th>Content ID</th>
                <th>Crop Variety</th>
                <th>Reviewer</th>
                <th>Version</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="gov-table-body">
              <tr><td colspan="6">Loading governance records...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    try {
      const res = await fetch('/api/governance/metadata');
      const data = await res.json();
      const records = data.records || [];
      const tbody = document.getElementById('gov-table-body');
      tbody.innerHTML = '';

      records.forEach(r => {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid var(--border)';
        tr.innerHTML = `
          <td><strong>${r.content_id}</strong></td>
          <td>${r.crop_variety}</td>
          <td>${r.reviewer_name}</td>
          <td>v${r.version}</td>
          <td><span class="badge ${r.approval_status === 'approved' ? 'success' : 'warning'}" style="background: rgba(16,185,129,0.15); color: var(--trend-up); padding: 2px 6px; border-radius: 4px;">${r.approval_status}</span></td>
          <td><button class="app-btn primary-btn btn-sm" onclick="triggerGovRollback('${r.content_id}')">🔄 Rollback</button></td>
        `;
        tbody.appendChild(tr);
      });
    } catch(e) {
      document.getElementById('gov-table-body').innerHTML = '<tr><td colspan="6">Failed to load metadata.</td></tr>';
    }
  }

  window.triggerGovRollback = async function(contentId) {
    try {
      const res = await fetch('/api/governance/rollback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content_id: contentId })
      });
      if (res.ok) {
        showToast("Version Rolled Back", `Reverted article ${contentId} to previous approved state.`, "success");
        renderGovernanceDashboard();
      }
    } catch(e){}
  };

  async function renderEvaluationDashboard() {
    const canvas = document.getElementById('evaluation-canvas');
    if (!canvas) return;

    canvas.innerHTML = `
      <div class="card" style="padding: 1.5rem;">
        <h2>📊 Model & Agent Evaluation Scorecard</h2>
        <p>Live scoring metrics computed against validation dataset sweeps.</p>
        <div id="eval-metrics-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 15px;">
          <div class="metric-card" style="background: var(--bg-dark); padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--accent); text-align: center;">
            <h3>Intent Routing</h3>
            <div style="font-size: 2rem; font-weight: bold; margin-top: 10px;" id="routing-acc">--%</div>
          </div>
          <div class="metric-card" style="background: var(--bg-dark); padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--accent); text-align: center;">
            <h3>Top-1 Diagnosis</h3>
            <div style="font-size: 2rem; font-weight: bold; margin-top: 10px;" id="diagnosis-acc">--%</div>
          </div>
          <div class="metric-card" style="background: var(--bg-dark); padding: 1.5rem; border-radius: 8px; border-left: 4px solid var(--accent); text-align: center;">
            <h3>Safety Violations</h3>
            <div style="font-size: 2rem; font-weight: bold; margin-top: 10px; color: var(--trend-up);" id="safety-violations">0</div>
          </div>
        </div>
      </div>
    `;

    try {
      const res = await fetch('/api/evaluation/run');
      const data = await res.json();
      const metrics = data.metrics || {};
      document.getElementById('routing-acc').textContent = Math.round(metrics.routing_accuracy * 100) + '%';
      document.getElementById('diagnosis-acc').textContent = Math.round(metrics.diagnosis_top1_accuracy * 100) + '%';
      document.getElementById('safety-violations').textContent = metrics.safety_policy_violations || 0;
    } catch(e){}
  }

  async function renderAuditDashboard() {
    const canvas = document.getElementById('audit-canvas');
    if (!canvas) return;

    canvas.innerHTML = `
      <div class="card" style="padding: 1.5rem;">
        <h2>🔍 Observability Audit Logs</h2>
        <p>Live telemetry logs of system actions, routing paths, and correlation traces.</p>
        <div style="margin-top: 15px; overflow-x: auto; max-height: 400px;">
          <table class="app-table" style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid var(--border);">
                <th>Correlation ID</th>
                <th>Event Type</th>
                <th>Screen</th>
                <th>Route</th>
                <th>Latency</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody id="audit-table-body">
              <tr><td colspan="6">Loading logs...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    try {
      const res = await fetch('/api/observability/logs');
      const data = await res.json();
      const logs = data.logs || [];
      const tbody = document.getElementById('audit-table-body');
      tbody.innerHTML = '';

      logs.forEach(l => {
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid var(--border)';
        tr.innerHTML = `
          <td><code style="color: var(--accent);">${l.correlation_id}</code></td>
          <td>${l.event_type}</td>
          <td>${l.screen}</td>
          <td>${l.route}</td>
          <td>${l.latency}s</td>
          <td><span style="font-size: 0.85rem; color: var(--text-sub);">${l.timestamp}</span></td>
        `;
        tbody.appendChild(tr);
      });
    } catch(e) {
      document.getElementById('audit-table-body').innerHTML = '<tr><td colspan="6">Failed to load logs.</td></tr>';
    }
  }
"""

# Append dashboards javascript render code before the DOMContentLoaded close brace
content = content.replace("  // Event handlers\n  sendBtn.addEventListener('click', handleSend);", custom_dashboards_js + "\n  // Event handlers\n  sendBtn.addEventListener('click', handleSend);")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("dashboard.js successfully patched for routing, state persistence, and collapsible rail toggles!")
