# Agent Architecture

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Architecture
> **Related ADR:** [ADR-AAA-003](adr/ADR-AAA-003-agent-skills-based-ai-sdlc.md)

---

## Router-Specialist Pattern

The system implements a decoupled, hierarchical multi-agent team using Google ADK:

```
Farmer's Query / Photo
       │
       ▼
┌─────────────────────────────────────────────────────┐
│        Krishi Sastri (Coordinator Agent)              │
│  • Parses intent, language, farm context              │
│  • Routes to specialist sub-agents                    │
│  • Translates and formats response                   │
│  • Emits A2UI JSON schemas for UI cards              │
│  • Enforces safety kernel on all prescriptions       │
└───────────────────────┬─────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Crop        │ │ Weather     │ │ Market      │
│ Analyst     │ │ Advisor     │ │ Advisor     │
│             │ │             │ │             │
│ Soil NPK,   │ │ 7-day       │ │ 6 crops,    │
│ health      │ │ forecast,   │ │ Yahoo Fin., │
│ checks      │ │ frost alert │ │ INR/KES    │
└─────────────┘ └─────────────┘ └─────────────┘
        ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Pest        │ │ Irrigation  │ │ Knowledge   │
│ Detector    │ │ Advisor     │ │ Retriever   │
│             │ │             │ │             │
│ Gemini Vis.,│ │ Water req., │ │ OKF SPARQL, │
│ OKF disease │ │ moisture %  │ │ RAG search  │
└─────────────┘ └─────────────┘ └─────────────┘
        ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Simulation  │ │ Dashboard   │ │ Farmer      │
│ Agent       │ │ Agent       │ │ Interaction │
│             │ │             │ │             │
│ Sandbox     │ │ UI schema   │ │ Voice/chat  │
│ step/run    │ │ config      │ │ translation │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Agent Registry

| Agent | Role | Model | MCP Tools | Status |
|-------|------|-------|-----------|--------|
| `coordinator_agent` | Orchestrator | Gemini 3.5 Flash | `get_ui_schema` | ✅ Active |
| `crop_analyst_agent` | Specialist | Gemini 3.5 Flash | OKF, RAG | ✅ Active |
| `weather_advisor_agent` | Specialist | Gemini 3.5 Flash | weather (Open-Meteo) | ✅ Active |
| `market_advisor_agent` | Specialist | Gemini 3.5 Flash | market (Yahoo Finance) | ✅ Active |
| `irrigation_advisor_agent` | Specialist | Gemini 3.5 Flash | OKF, weather | ✅ Active |
| `pest_detector_agent` | Specialist | Gemini 3.5 Flash | OKF, image_analysis, safety | ✅ Active |
| `knowledge_retriever_agent` | Retriever | Gemini 3.5 Flash | OKF, RAG | ✅ Active |
| `simulation_agent` | Simulator | Gemini 3.5 Flash | simulation tools | ✅ Active |
| `dashboard_agent` | Interface | Gemini 3.5 Flash | schema tools | ✅ Active |
| `farmer_interaction_agent` | Interface | Gemini 3.5 Flash | TTS, STT, translation | ✅ Active |

Registry file: `agents/agent_registry.yaml`

## Four Intelligence Layers

| Layer | Type | Example | Source | Runtime |
|-------|------|---------|--------|---------|
| **OKF** | Static, curated reference | "Wheat rust: symptoms, treatment, dosage limits" | `okf-knowledge-graph/data/` | File read |
| **Dynamic** | Real-time, fresh data | "Wheat price today: ₹2,200/quintal" | MCP servers (APIs) | HTTP fetch |
| **RAG** | Document search | "Follow IPM guidelines for bollworm..." | `rag_pipeline/` embeddings | Vector search |
| **Edge** | Offline models | TFLite pest ID, Gemma explanations | Local models + IndexedDB | In-browser |

## MCP Server Integration

| Server | Data Source | Status | Crops/Features |
|--------|-------------|--------|----------------|
| `weather` | Open-Meteo API | ✅ Live | 7-day forecast, frost alerts |
| `market` | Yahoo Finance API | ✅ Live | 6 crops (corn, wheat, soybeans, cotton, rice, sugarcane) |
| `okf` | OKF knowledge graph files | ✅ Working | 22 entities, search across crops/diseases/pests/soil/safety |
| `rag` | RAG pipeline embeddings | ⚠️ No documents ingested | Pipeline ready, zero documents |
| `image_analysis` | Gemini Vision API | ✅ Working | Pest/disease photo analysis |
| `tts` | edge-tts | ✅ Working | Neural male voices (Madhur, Manohar, Mohan, Rafiki) |
| `stt` | Browser Web Speech | ✅ Working | BCP-47 language codes |
| `translation` | Backend translation | ✅ Working | 5 languages |

## Safety Kernel Integration

The Safety Kernel implements two ADK callback functions:

- **`safety_before_agent`** — Inspects pending tool outputs for chemical/pesticide mentions; checks against `pesticide_limits.md`
- **`safety_after_agent`** — Validates final response for banned chemicals, dosage violations, PHI breaches; blocks or flags

Safety data sources:
- `okf-knowledge-graph/data/safety/pesticide_limits.md` — 10 pesticides with max concentration, max rate, PHI
- `okf-knowledge-graph/data/safety/pre_harvest_intervals.md` — Typical PHI by pesticide type
- `okf-knowledge-graph/data/safety/organic_standards.md` — Organic certification requirements

## Related Documents

- [Architecture Overview](architecture-overview.md)
- [Data & Farm Twin Architecture](data-and-farm-twin-architecture.md)
- [ADR-AAA-003: Agent-Skills-Based AI-SDLC](adr/ADR-AAA-003-agent-skills-based-ai-sdlc.md)
- [ADR-AAA-005: Safety Kernel](adr/ADR-AAA-005-agricultural-safety-kernel.md)