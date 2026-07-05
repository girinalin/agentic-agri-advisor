# Functional Requirements

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Product / Engineering
> **Requirements ID format:** REQ-AAA-XXX

---

## REQ-AAA-001: Multilingual User Interface

**Priority:** P0 — Critical

The system shall provide a fully translated user interface in 5 languages: English (en), Hindi (hi), Marathi (mr), Telugu (te), and Swahili (sw).

- All navigation labels, button text, headings, and system messages must be translated
- Language switching must be instant (no page reload) via a dropdown selector
- Translation keys must follow a consistent naming convention (e.g., `nav_home`, `nav_soil`)
- Script purity must be enforced: Hindi mode contains zero Telugu characters and vice versa
- Farmer names and regional locations must remain untranslated (e.g., "माधव जी" stays in Devanagari)

**Acceptance:** `make validate-translations` passes; manual browser testing confirms all 5 languages render correctly.

---

## REQ-AAA-002: Offline-First PWA Operation

**Priority:** P0 — Critical

The system shall function as an installable Progressive Web App with full offline capability.

- Service worker caches all static assets (HTML, CSS, JS, fonts) for instant offline load
- IndexedDB stores farmer profile, chat history, OKF knowledge cache, telemetry queue, farm activities, escalations, reminders, feedback
- When offline, the app routes simple queries to local OKF cache or rule-based responses
- When connectivity returns, queued telemetry and activities sync to the backend SQLite database
- The app must remain usable on devices with 2GB RAM and no WebGPU support

**Acceptance:** App loads and responds to queries with airplane mode enabled; sync completes when connectivity returns.

---

## REQ-AAA-003: Voice-First Interaction (STT/TTS)

**Priority:** P0 — Critical

The system shall provide zero-cost voice interaction using browser-native APIs.

- Speech-to-Text via `webkitSpeechRecognition` with BCP-47 language codes (hi-IN, mr-IN, te-IN, sw-KE, en-US)
- Text-to-Speech via `speechSynthesis` with automatic neural male voice selection for Hindi (Madhur, Manohar, Mohan) and Swahili (Rafiki)
- Backend TTS fallback via edge-tts for browsers lacking regional voices
- Voice must auto-enable when the user taps the microphone button
- Mic indicator must show active/inactive state; must not stay always-on

**Acceptance:** Farmer can complete a full query-answer cycle using only voice (no typing); TTS reads responses in the correct language.

---

## REQ-AAA-004: Multi-Agent Advisory System

**Priority:** P0 — Critical

The system shall route farmer queries to specialized sub-agents via a coordinator agent (Krishi Sastri).

- 9 specialist agents: Crop Analyst, Weather Advisor, Market Advisor, Pest Detector, Irrigation Advisor, Farmer Interaction, Knowledge Retriever, Simulation Agent, Dashboard Agent
- Coordinator uses ADK sub-agent routing to direct queries to the appropriate specialist
- All agents use MCP tools for real-time data access (weather, market, OKF, image analysis)
- Agent responses in Farmer Mode must use the warm village-scholar persona, stay under 80 words, avoid markdown, and hide internal agent names

**Acceptance:** 29-case evaluation suite passes with ≥4.0/5.0 average; routing is correct for all categories.

---

## REQ-AAA-005: Agricultural Safety Kernel

**Priority:** P0 — Critical

All prescriptive recommendations (chemical dosages, pesticide advice, irrigation thresholds) must pass through the Agricultural Safety Kernel.

- Banned chemicals (endosulfan, monocrotophos, etc.) must be blocked with a safe alternative suggested
- Dosage limits enforced for 10 registered pesticides (max concentration, max application rate)
- Pre-harvest interval (PHI) must be checked and violations flagged
- Low-confidence diagnoses must trigger expert escalation prompts
- Escalation queue must persist pending escalations for human agronomist review

**Acceptance:** 19 adversarial safety tests pass; `python -m tools.ai_sdlc.validate_safety_policies` returns PASS.

---

## REQ-AAA-006: Camera & Image-Based Pest Detection

**Priority:** P1 — High

The system shall allow farmers to capture or upload crop photos for disease/pest diagnosis.

- Rear camera prioritized via `getUserMedia({ facingMode: "environment" })`
- File upload fallback when camera is unavailable
- TFLite crop disease classifier (38 disease labels) for offline diagnosis
- Cloud Gemini Vision analysis for online complex cases
- Color heuristic fallback for devices without WebGPU/WebGL
- Photos can be routed to expert mode for deeper analysis

**Acceptance:** Photo capture works on Android Chrome; classification returns a result within 3 seconds.

---

## REQ-AAA-007: Market Price Advisory

**Priority:** P1 — High

The system shall provide real-time commodity prices for 6 crops.

- Crops: Corn, Wheat, Soybeans, Cotton, Rice, Sugarcane
- Yahoo Finance API for real-time futures data
- Unit conversions: cents/bushel → USD/quintal → INR/KES
- Display in farmer's local currency (₹ for India, KSh for Kenya)
- Historical trend visualization in the dashboard

**Acceptance:** `curl localhost:8000/api/market/price/corn` returns live price data.

---

## REQ-AAA-008: Weather Advisory

**Priority:** P1 — High

The system shall provide location-based weather forecasts and hazard alerts.

- Open-Meteo API for 7-day forecasts (temperature, precipitation, wind)
- Frost alerts, heat wave warnings, rain probability
- Evapotranspiration calculations for irrigation planning
- Weather data injected into agent context for personalized advice

**Acceptance:** `curl localhost:8000/api/weather?lat=21.15&lon=79.09` returns current weather data.

---

## REQ-AAA-009: Soil Test Report Workflow

**Priority:** P1 — High

The system shall allow farmers to input, upload, or photograph soil test reports.

- 3 input methods: PDF/photo upload, camera capture, manual entry
- Soil parameters: pH, EC, organic carbon, N, P, K, S, Zn, B, Fe
- Metadata: field selection, report date, lab name, soil type
- Automatic interpretation with color-coded status (🟢 good, 🟡 low, 🔴 critical)
- Fertilizer and soil amendment recommendation buttons
- Reports saved to SQLite `soil_reports` and `soil_test_values` tables

**Acceptance:** Manual entry → save → summary screen shows interpretations; API returns saved report.

---

## REQ-AAA-010: Farm Digital Twin

**Priority:** P1 — High

The system shall maintain a SQLite digital twin of each farmer's fields.

- Tables: farmers, fields, plantings, telemetry, soil_reports, soil_test_values
- Profile data injected into every agent prompt for personalized advice
- Telemetry updates (moisture %, nitrogen PPM, health %) from simulation and activity logs
- Farm activities (irrigation, fertilization, treatment) logged with timestamps

**Acceptance:** `curl localhost:8000/api/profile/user` returns farmer with fields and plantings.

---

## REQ-AAA-011: Two Advisor Modes

**Priority:** P1 — High

The system shall offer two explicit advisor modes selected by the farmer.

- **Krishi Sastri (कृषि शास्त्री)** — Free, offline-capable, OKF knowledge + rule-based, voice + camera
- **Krishi Visheshagya (कृषि विशेषज्ञ)** — Cloud-based, multi-agent specialist system, real-time APIs, expert escalation
- Mode selection is explicit (user taps a card), not automatic
- Sastri can escalate to Visheshagya when confidence is low

**Acceptance:** Both advisor cards display on the "पूछें" screen; selecting each routes to the correct backend.

---

## REQ-AAA-012: Evaluation Flywheel

**Priority:** P2 — Medium

The system shall include an evaluation pipeline for agent quality assurance.

- 29 eval cases across 10 categories (greeting, weather, market, crop, pest, irrigation, safety, adversarial, escalation, UI)
- 4 metrics: hallucination, safety compliance, tool-use quality, response quality
- Local eval runner using Gemini API key (bypasses agents-cli ADC requirement)
- LLM-as-judge grading with category breakdown and failure analysis

**Acceptance:** `uv run python tests/eval/run_local_eval.py` produces grade report with ≥4.0/5.0 average.

---

## Related Documents

- [Non-Functional Requirements](non-functional-requirements.md)
- [Architecture Overview](../02-architecture/architecture-overview.md)
- [ADR-AAA-001: Multilingual UI](../02-architecture/adr/ADR-AAA-001-multilingual-ui-architecture.md)
- [ADR-AAA-002: Offline-First PWA](../02-architecture/adr/ADR-AAA-002-offline-first-pwa-indexeddb-sync.md)
- [ADR-AAA-005: Safety Kernel](../02-architecture/adr/ADR-AAA-005-agricultural-safety-kernel.md)