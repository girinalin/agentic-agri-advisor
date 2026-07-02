(function() {
  async function renderExpertConsole() {
    const mainCanvas = document.getElementById('console-canvas');
    if (!mainCanvas) return;
    
    if (typeof window.logObservabilityEvent === 'function' && typeof window.generateCorrelationId === 'function') {
      window.logObservabilityEvent(window.generateCorrelationId(), 'screen_rendered', 'expert_console', '', '', 'local', '', 0);
    }

    mainCanvas.innerHTML = `
      <div class="expert-console-layout">
        <div class="expert-sidebar">
          <h3>📥 Consultation Triage Queue</h3>
          <div class="template-response-chips" style="margin-bottom: 10px;">
            <button class="template-chip filter-btn active" data-filter="all">All</button>
            <button class="template-chip filter-btn" data-filter="urgent">⚠️ Urgent</button>
            <button class="template-chip filter-btn" data-filter="open">Open</button>
            <button class="template-chip filter-btn" data-filter="closed">Closed</button>
          </div>
          <div id="expert-case-list">Loading queue...</div>
          
          <h3 style="margin-top: 20px;">🚨 Regional Outbreak Intel</h3>
          <div id="expert-outbreak-list">Loading outbreaks...</div>
        </div>
        <div class="expert-main-content" id="expert-detail-pane">
          <div class="empty-state" style="text-align: center; margin-top: 100px;">
            <h2>💻 Agronomist Operations Panel</h2>
            <p>Select a case or regional outbreak from the sidebar to review evidence, run image comparisons, and dispatch verified prescriptions.</p>
          </div>
        </div>
      </div>
    `;

    try {
      const res = await fetch('/api/expert/queue');
      const data = await res.json();
      const queue = data.queue || [];
      populateCaseList(queue);

      const outRes = await fetch('/api/outbreaks');
      const outData = await outRes.json();
      populateOutbreaks(outData.outbreaks || []);
    } catch (e) {
      document.getElementById('expert-case-list').innerText = "Failed to load expert queues.";
    }
  }

  function populateCaseList(cases, filter = 'all') {
    const list = document.getElementById('expert-case-list');
    if (!list) return;
    list.innerHTML = "";
    
    const filtered = cases.filter(c => {
      if (filter === 'urgent') return c.safety_flags && c.safety_flags !== 'none';
      if (filter === 'open') return c.state !== 'closed';
      if (filter === 'closed') return c.state === 'closed';
      return true;
    });

    if (filtered.length === 0) {
      list.innerHTML = `<div style="padding: 10px; color: var(--text-muted);">No cases found.</div>`;
      return;
    }

    filtered.forEach(c => {
      const div = document.createElement('div');
      div.className = `case-card ${c.safety_flags && c.safety_flags !== 'none' ? 'urgent' : ''}`;
      div.innerHTML = `
        <div style="font-weight: bold; display: flex; justify-content: space-between;">
          <span>👤 ID: ${c.escalation_id.substring(0,6)}</span>
          <span style="font-size: 0.8rem; background: var(--border); padding: 2px 6px; border-radius: 4px;">${c.state}</span>
        </div>
        <div style="font-size: 0.9rem; margin-top: 5px;">${c.farmer_question}</div>
        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 5px;">Crop: ${c.crop_context} · Lang: ${c.language}</div>
      `;
      div.addEventListener('click', () => {
        document.querySelectorAll('.case-card').forEach(el => el.classList.remove('active'));
        div.classList.add('active');
        showCaseDetails(c);
      });
      list.appendChild(div);
    });

    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.filter-btn').forEach(el => el.classList.remove('active'));
        btn.classList.add('active');
        populateCaseList(cases, btn.getAttribute('data-filter'));
      };
    });
  }

  function showCaseDetails(c) {
    const pane = document.getElementById('expert-detail-pane');
    if (!pane) return;

    pane.innerHTML = `
      <h2>📋 Review Escalation: ${c.escalation_id}</h2>
      <div class="expert-detail-grid">
        <div>
          <h3>🌾 Farmer Question & Context</h3>
          <p><strong>Original Lang:</strong> ${c.language}</p>
          <p><strong>Question:</strong> ${c.farmer_question}</p>
          <p><strong>Translated Summary:</strong> ${c.translated_summary}</p>
          <p><strong>Crop & Field:</strong> ${c.crop_context} (${c.field_context})</p>
          <p><strong>Diagnostic Inference:</strong> ${c.diagnosis_result} (${Math.round(c.confidence*100)}% Confidence)</p>
          <p><strong>Safety Flags:</strong> <span style="color: ${c.safety_flags !== 'none' ? 'var(--danger)' : 'var(--success)'}">${c.safety_flags}</span></p>
        </div>
        <div>
          <h3>🔍 Image Comparison & Reference</h3>
          <div class="image-comparison-frame">
            <div class="comparison-pane">
              <strong>Farmer Upload</strong>
              <div style="background: #2a2a2a; border-radius: 4px; padding: 20px; margin-top: 5px;">📸 Symptom Image</div>
            </div>
            <div class="comparison-pane">
              <strong>OKF Reference Library</strong>
              <div style="background: #2a2a2a; border-radius: 4px; padding: 20px; margin-top: 5px;">📖 Deficiency Reference</div>
            </div>
          </div>
          <h3 style="margin-top: 15px;">📊 Recent Activities</h3>
          <p>${c.recent_activities || 'No activities logged recently.'}</p>
        </div>
      </div>
      
      <hr style="border: 0; border-top: 1px solid var(--border); margin: 20px 0;">

      <h3>✍️ Formulate Expert Prescription</h3>
      <div class="template-response-chips">
        <button class="template-chip" onclick="applyResponseTemplate('Apply nitrogen-rich compost (2 bags) to soil base.')">Nitrogen Deficiency</button>
        <button class="template-chip" onclick="applyResponseTemplate('Spray neem oil dilution to combat aphid clusters.')">Aphid Treatment</button>
        <button class="template-chip" onclick="applyResponseTemplate('पोस्टपोन फर्टिलाइज़र: हवा की गति अधिक होने के कारण छिड़काव न करें।')">Wind Spray Block</button>
      </div>

      <textarea id="expert-response-input" rows="5" class="app-input" style="width: 100%;" placeholder="Type recommendation details here...">${c.expert_response || ''}</textarea>

      <div style="display: flex; gap: 10px; margin-top: 15px;">
        <button class="app-btn primary-btn" id="btn-expert-send">📤 Send Expert Response</button>
        <button class="app-btn danger-btn" id="btn-expert-close">🔒 Close Ticket</button>
      </div>
    `;

    document.getElementById('btn-expert-send').onclick = async () => {
      const resp = document.getElementById('expert-response-input').value;
      const res = await fetch('/api/expert/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          escalation_id: c.escalation_id,
          state: 'expert_replied',
          expert_response: resp
        })
      });
      if (res.ok) {
        if (typeof window.showToast === 'function') {
          window.showToast("Response Dispatched", "Expert solution successfully synced with farmer dashboard.", "success");
        }
        renderExpertConsole();
      }
    };

    document.getElementById('btn-expert-close').onclick = async () => {
      const res = await fetch('/api/expert/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          escalation_id: c.escalation_id,
          state: 'closed'
        })
      });
      if (res.ok) {
        if (typeof window.showToast === 'function') {
          window.showToast("Ticket Closed", "Consultation ticket closed successfully.", "success");
        }
        renderExpertConsole();
      }
    };
  }

  window.applyResponseTemplate = function(text) {
    const input = document.getElementById('expert-response-input');
    if (input) input.value = text;
  };

  function populateOutbreaks(outbreaks) {
    const list = document.getElementById('expert-outbreak-list');
    if (!list) return;
    list.innerHTML = "";
    
    outbreaks.forEach(o => {
      const div = document.createElement('div');
      div.className = "case-card";
      div.innerHTML = `
        <div style="font-weight: bold;">📍 Area: ${o.region}</div>
        <p style="margin: 5px 0;">Symptom: ${o.pest_symptom} (${o.case_count} reports)</p>
        <span style="font-size: 0.8rem; background: var(--border); padding: 2px 6px; border-radius: 4px;">Status: ${o.status}</span>
      `;
      list.appendChild(div);
    });
  }

  async function renderGovernanceDashboard() {
    const mainCanvas = document.getElementById('governance-canvas');
    if (!mainCanvas) return;

    if (typeof window.logObservabilityEvent === 'function' && typeof window.generateCorrelationId === 'function') {
      window.logObservabilityEvent(window.generateCorrelationId(), 'screen_rendered', 'knowledge_governance', '', '', 'local', '', 0);
    }

    mainCanvas.innerHTML = `
      <div class="card" style="padding: 1.5rem;">
        <h2>📖 Knowledge Governance & Policy Dashboard</h2>
        <p>Manage model knowledge overrides, view verification history, and rollback changes.</p>
        <div style="margin-top: 15px; overflow-x: auto;">
          <table class="app-table" style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid var(--border);">
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
      const res = await fetch('/api/governance');
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
          <td><span style="font-size: 0.85rem; padding: 2px 6px; border-radius: 4px; background: ${r.status === 'published' ? 'var(--success)' : 'var(--border)'}">${r.status}</span></td>
          <td>
            <button class="app-btn danger-btn" style="padding: 2px 8px; font-size: 0.8rem;" onclick="rollbackGovernance('${r.content_id}')">Rollback</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    } catch (e) {
      document.getElementById('gov-table-body').innerHTML = '<tr><td colspan="6">Failed to load governance records.</td></tr>';
    }
  }

  window.rollbackGovernance = async function(contentId) {
    try {
      const res = await fetch('/api/governance/rollback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content_id: contentId })
      });
      if (res.ok) {
        if (typeof window.showToast === 'function') {
          window.showToast("Version Rolled Back", `Governance entry ${contentId} successfully reverted.`, "success");
        }
        renderGovernanceDashboard();
      }
    } catch(err) {
      console.warn("Rollback failed:", err);
    }
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

  // Export to global scope
  window.renderExpertConsole = renderExpertConsole;
  window.renderGovernanceDashboard = renderGovernanceDashboard;
  window.renderEvaluationDashboard = renderEvaluationDashboard;
  window.renderAuditDashboard = renderAuditDashboard;
})();
