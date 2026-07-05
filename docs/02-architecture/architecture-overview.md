# Architecture Overview

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Architecture

---

## System Architecture

Krishi Sampark uses a **Router-Specialist multi-agent pattern** built on the Google Agent Development Kit (ADK), with a decoupled edge-cloud architecture designed for intermittent connectivity.

```
┌─────────────────────────────────────────────────────────────┐
│                    EDGE LAYER (PWA)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Local Gemma  │  │ TFLite       │  │ IndexedDB        │  │
│  │ 2B (WebGPU)  │  │ Classifier   │  │ (11 stores)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Service Worker│  │ Voice STT/TTS│  │ Camera (getUserMedia)│
│  │ (Cache API)  │  │ (Web Speech)  │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ (online/offline routing)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   CLOUD LAYER (FastAPI)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Krishi Sastri (Coordinator Agent)           │   │
│  │  ┌─────────┬─────────┬─────────┬─────────┬──────────┐ │   │
│  │  │Crop     │Weather  │Market   │Pest     │Irrigation│ │   │
│  │  │Analyst  │Advisor  │Advisor  │Detector │Advisor   │ │   │
│  │  └─────────┴─────────┴─────────┴─────────┴──────────┘ │   │
│  │  ┌─────────┬─────────┬─────────┬─────────┐             │   │
│  │  │Knowledge│Simul-   │Dashboard│Farmer   │             │   │
│  │  │Retriever│ation    │Agent    │Interact.│             │   │
│  │  └─────────┴─────────┴─────────┴─────────┘             │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              MCP Servers (8)                          │   │
│  │  weather │ market │ okf │ rag │ image_analysis        │   │
│  │  tts     │ stt    │ translation                       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  OKF Knowledge Graph │ RAG Pipeline │ Safety Kernel   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SQLite Farm Twin (farm_twin.db)                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Key Architectural Decisions

| Decision | ADR | Rationale |
|----------|-----|-----------|
| Multilingual UI with translation keys | [ADR-AAA-001](adr/ADR-AAA-001-multilingual-ui-architecture.md) | 5 languages, instant switching, script purity |
| Offline-first PWA with IndexedDB | [ADR-AAA-002](adr/ADR-AAA-002-offline-first-pwa-indexeddb-sync.md) | Rural connectivity is intermittent |
| Agent-skills-based AI-SDLC | [ADR-AAA-003](adr/ADR-AAA-003-agent-skills-based-ai-sdlc.md) | 10 lifecycle agents, 29 skills, evidence-driven |
| Edge-cloud advisor routing | [ADR-AAA-004](adr/ADR-AAA-004-edge-cloud-advisor-routing.md) | Simple queries local, complex queries cloud |
| Agricultural Safety Kernel | [ADR-AAA-005](adr/ADR-AAA-005-agricultural-safety-kernel.md) | Banned chemicals, dosage limits, PHI |

## Technology Stack

| Layer | Technology | Version/Config |
|-------|-----------|----------------|
| Agent Framework | Google ADK | `google-adk>=2.0.0` |
| LLM | Gemini 3.5 Flash | Retry options, temperature-tuned per agent |
| Backend | FastAPI | Port 8000, SSE streaming |
| Agent Playground | ADK Playground | Port 8080, `/run_sse` endpoint |
| Frontend | Vanilla JS PWA | Service worker v3, IndexedDB (11 stores) |
| Database | SQLite | `farm_twin.db` — farmers, fields, plantings, soil_reports |
| MCP Servers | Python | 8 servers (weather, market, okf, rag, image_analysis, tts, stt, translation) |
| Voice | Web Speech API + edge-tts | Browser-native STT, backend neural TTS fallback |
| Local Models | MediaPipe WebGenAI + TFLite | Gemma 2B (WebGPU), PlantVillage classifier (38 labels) |

## Folder Structure

```
agentic-agri-advisor/
├── agents/                  # Python ADK agents (coordinator + 9 specialists)
├── app/                     # FastAPI server & endpoints
├── ui/agui/                 # PWA frontend (dashboard, voice, camera, translations)
├── ui/a2ui/                 # A2UI declarative UI rendering engine
├── mcp_servers/             # 8 MCP servers
├── okf-knowledge-graph/     # OKF knowledge graph data & schema
├── rag_pipeline/            # RAG document search pipeline
├── safety_kernel/           # Agricultural Safety Kernel
├── simulation/              # Farm simulation sandbox
├── data/                    # SQLite database manager
├── tests/                   # Unit, integration, eval tests
├── .ai-sdlc/                # AI-SDLC framework (agents, skills, workflows, evidence)
├── tools/ai_sdlc/           # AI-SDLC validation CLI scripts
└── docs/                    # This documentation
```

## Related Documents

- [Edge-Cloud Advisor Architecture](edge-cloud-advisor-architecture.md)
- [Agent Architecture](agent-architecture.md)
- [Data & Farm Twin Architecture](data-and-farm-twin-architecture.md)
- [Hybrid Intelligence Strategy](hybrid-intelligence-strategy.md)