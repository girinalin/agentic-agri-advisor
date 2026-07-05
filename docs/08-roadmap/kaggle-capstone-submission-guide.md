# Kaggle Capstone Submission Guide

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Product / Capstone Team
> **Source:** Consolidated from `KAGGLE_&_LEADERSHIP_GUIDE.md`

---

## Executive Overview

Krishi Sampark is an enterprise-grade multi-agent agricultural intelligence platform designed for smallholders in India and Sub-Saharan Africa. It solves the critical bottleneck of **delivering personalized, highly technical scientific advice to low-connectivity, low-literacy farmers at zero ongoing API cost**.

### Key Business Metrics

| Metric | Value |
|--------|-------|
| Voice API cost | $0.00 (browser-native STT/TTS) |
| Offline capability | ✅ Full PWA with IndexedDB sync |
| Languages | 5 (English, Hindi, Marathi, Telugu, Swahili) |
| Agents | 10 (coordinator + 9 specialists) |
| MCP Servers | 8 (weather, market, OKF, RAG, image_analysis, TTS, STT, translation) |
| Safety tests | 19/19 pass |
| Eval cases | 29 across 10 categories |
| Eval score | 4.34/5.0 average |

## Slide-by-Slide Presentation Outline

### Slide 1: Title & The Smallholder Challenge
- 500+ Million smallholders face volatile climates, shifting diseases, fluctuating prices
- Traditional solution: Village elders and agricultural scholars (Krishi Sastri)
- Modern challenge: High literacy barriers, poor internet, prohibitive cloud API costs

### Slide 2: Platform Architecture
- Router-Specialist multi-agent pattern built on Google ADK
- 9 specialist agents coordinated by Krishi Sastri
- MCP servers decouple data access from agent logic

### Slide 3: Model Context Protocol (MCP) Integration
- OKF knowledge graph, RAG embeddings, Open-Meteo weather, Yahoo Finance market
- Decoupled architecture allows swapping APIs without touching agent code

### Slide 4: Farmer Digital Twin Database
- SQLite twin: farmers → fields → plantings → telemetry
- Every agent prompt enriched with farmer's specific land context
- Personalized advice, not generic AI responses

### Slide 5: Zero-Cost Voice Engine
- Browser-native STT (webkitSpeechRecognition) — $0 cost, <100ms latency
- Backend neural TTS (edge-tts) — male voices (Madhur, Manohar, Mohan, Rafiki)
- No cloud speech API costs, no network overhead for voice

### Slide 6: Dynamic Visual Workspace & Multilingualism
- A2UI declarative JSON schemas rendered as interactive cards
- Instant 5-language switching without page reload
- Script purity enforced (no Devanagari in Telugu mode)

### Slide 7: Crop Growth Simulator Sandbox
- Mathematical modeling of crop age, moisture depletion, evapotranspiration
- Risk-free training: farmers test watering schedules before committing
- Updates SQLite twin, prompting agent to suggest next steps

### Slide 8: The Evaluation Quality Flywheel
- 29 eval cases across 10 categories
- 4 metrics: response quality, safety, language, tool usage
- LLM-as-judge grading with category breakdown
- Regression detection before deployment

### Slide 9: Agricultural Safety Kernel
- Banned chemicals (5) blocked with safe alternatives
- Dosage limits (10 pesticides) enforced programmatically
- Pre-harvest interval (PHI) violations flagged
- Expert escalation queue for human agronomist review
- 19 adversarial tests confirm resistance to prompt injection

### Slide 10: Scalability & Future Roadmap
- Cloud Run deployment (planned)
- WhatsApp voice-note integration (planned)
- IoT soil moisture sensor telemetry (planned)
- Comprehensive pesticide registry expansion (planned)

## Repository Structure for Judges

```
agentic-agri-advisor/
├── agents/                  # 10 ADK agents (coordinator + 9 specialists)
├── app/                     # FastAPI server
├── ui/agui/                 # PWA frontend
├── mcp_servers/             # 8 MCP servers
├── safety_kernel/           # Agricultural Safety Kernel
├── okf-knowledge-graph/     # 22 OKF entities
├── rag_pipeline/            # RAG pipeline (documents not yet ingested)
├── simulation/              # Farm simulation sandbox
├── data/                    # SQLite farm twin database
├── tests/                   # Unit, integration, eval tests
├── .ai-sdlc/                # AI-SDLC framework (10 agents, 29 skills)
├── tools/ai_sdlc/           # 13 validation CLI scripts
└── docs/                    # 8-section consolidated documentation
```

## Demo Script

1. **Home Dashboard** — Show greeting in Hindi, weather card, moisture warning
2. **Voice Query** — Tap mic, speak: "मेरे भुट्टे की पत्तियों पर धब्बे हैं" → show response
3. **Photo Diagnosis** — Open camera, capture leaf → show classification
4. **Market Prices** — Show 6 crops with live Yahoo Finance data in ₹
5. **Soil Test** — Nav → मिट्टी जांच → manual entry → fill values → save → show summary
6. **Safety Test** — Ask "Can I use endosulfan?" → show it's blocked with alternative
7. **Offline Mode** — Enable airplane mode → ask question → show OKF cache response
8. **Language Switch** — Switch to Telugu → show all UI in Telugu script
9. **Escalation** — Ask complex question in Sastri → show escalation prompt → open expert form

## Related Documents

- [Product Vision](../01-product/product-vision.md)
- [Current Status & Roadmap](current-status-and-roadmap.md)
- [Evaluation & Safety Report](../05-testing/evaluation-and-safety-report.md)