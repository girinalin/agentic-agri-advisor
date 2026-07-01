# Agentic Agriculture Advisor (AAA)

Agentic Agriculture Advisor (AAA) is a multi-agent agriculture intelligence project built using the Google ADK and Antigravity SDK conventions. 

It coordinates multiple specialized agents, MCP servers, a knowledge graph (OKF), a RAG document search pipeline, and a simulation environment, and exposes both standard agent interfaces and web-based UI tools.

## Project Structure

```
agentic-agri-advisor/
├── agents/                  # Python ADK agents
│   ├── coordinator/         # Orchestrates task routing to specialists
│   ├── crop_analyst/        # Soil chemistry and crop health analysis
│   ├── weather_advisor/     # Weather impact modeling
│   ├── market_advisor/      # Commodity price trends and advisory
│   └── agent_registry.yaml   # Registry mapping Python agent details
├── ui_agents/               # JS/TS ADK UI agents
│   ├── package.json
│   ├── tsconfig.json
│   └── src/                 # JS/TS agent source code
├── mcp_servers/             # Model Context Protocol (MCP) servers
│   ├── okf/                 # Open Knowledge Graph database interface
│   ├── rag/                 # RAG document search index
│   ├── weather/             # Weather API connector
│   ├── market/              # Commodity market API connector
│   ├── image_analysis/      # Multi-modal crop photo analyzer
│   ├── tts/                 # Text-To-Speech for farmer audio feedback
│   ├── stt/                 # Speech-To-Text for farmer voice queries
│   └── mcp_registry.json    # MCP server configuration and definitions
├── okf-knowledge-graph/     # OKF knowledge graph assets & ingestion
│   ├── schema/              # Ontology definitions (Turtle, JSON-LD)
│   ├── data/                # Entity/relation files
│   └── scripts/             # Ingestion and query scripts
├── rag-pipeline/            # RAG data retrieval pipeline
│   ├── config.yaml          # Chunking & model settings
│   ├── documents/           # Source agronomy manuals
│   ├── embeddings/          # Vector index and generator script
│   └── retriever/           # Retrieval & search script
├── ui/                      # A2UI & AGUI UI components
│   ├── a2ui/                # Agent-to-User Interface (declarative layout parser)
│   └── agui/                # Antigravity visual client dashboard
├── simulation/              # Farm simulation sandbox environment
│   ├── config.yaml          # Simulated weather & crop dynamics parameters
│   ├── env.py               # Sandbox environment logic
│   └── run_simulation.py    # Main script to run simulator steps
├── config/                  # Configuration files
│   ├── dev.yaml
│   ├── prod.yaml
│   └── secrets.template.env
├── pyproject.toml           # Python dependencies
├── agents-cli-manifest.yaml # agents-cli manifest
└── GEMINI.md                # AI-assisted development instructions
```

## Quick Start (Prototype Mode)

Install `agents-cli` and setup skills:
```bash
uvx google-agents-cli setup
```

Install local project dependencies:
```bash
agents-cli install
```

Launch the local web environment / playground:
```bash
agents-cli playground
```

## 🌾 Running the Krishi Sampark Frontend Dashboard

To launch the web interface and converse with the **Krishi Sastri** advisor agent:

1. **Start the backend agent playground (port 8080)**:
   ```bash
   uv run agents-cli playground
   ```
2. **Start the FastAPI web app server (port 8000)**:
   ```bash
   uv run python -m app.fast_api_app
   ```
3. **Access the Interface**:
   Open your browser and navigate to:
   *   **Krishi Sampark Dashboard (Recommended):** `http://localhost:8000/agui/index.html`
   *   **Standard A2UI Client:** `http://localhost:8000/a2ui/index.html`

