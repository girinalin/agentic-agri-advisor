# Requirements Traceability Matrix

| Req ID | Title | ADR | Source Files | Tests | Security & Safety Controls |
| --- | --- | --- | --- | --- | --- |
| REQ-AAA-001 | Multilingual UI (English, Hindi, Marathi, Telugu, Swahili) | ADR-AAA-001 | ui/agui/translations.js, ui/agui/index.html | tests/integration/test_localization.py | UX-Localization-Verification |
| REQ-AAA-002 | Offline-First Operation & Storage | ADR-AAA-002 | ui/sw.js, ui/agui/local_db.js | tests/integration/test_phase4.py | Service-Worker-Verification |
| REQ-AAA-003 | Voice-First Interaction & STT/TTS | ADR-AAA-003 | ui/agui/voice.js | tests/integration/test_phase4.py | Voice-AutoSpeak-Verification |
| REQ-AAA-004 | Farmer Mode Dynamic Advisor & AI-Twin Profile | ADR-AAA-004 | agents/coordinator/agent.py, ui/agui/dashboard.js | tests/integration/test_agent.py | Ask-Prompt-Enforcement |
| REQ-AAA-005 | Agricultural Safety Kernel Advice Audit | ADR-AAA-005 | app/fast_api_app.py | tests/integration/test_server_e2e.py | Safety-Kernel-Escalation |
| REQ-AAA-006 | Regional Outbreak Intel Map Tracking | ADR-AAA-006 | ui/schemas/regional_risk_map.json, ui/agui/expert_dashboards.js | tests/integration/test_collapsible_nav.py | Outbreak-Triage-Queue |
| REQ-AAA-007 | Reliable DLQ & Synchronization Queue | ADR-AAA-007 | ui/agui/local_db.js, ui/agui/dashboard.js | tests/integration/test_phase5.py | Sync-Retry-DLQ |
| REQ-AAA-008 | observability Log Audit Trails | ADR-AAA-008 | app/fast_api_app.py, ui/agui/dashboard.js | tests/integration/test_phase5.py | Log-Audit-Correlation |
| REQ-AAA-009 | Collapsible Left Navigation Layout | ADR-AAA-009 | ui/agui/index.html, ui/agui/dashboard.js | tests/integration/test_collapsible_nav.py | Layout-Responsive-Checks |
