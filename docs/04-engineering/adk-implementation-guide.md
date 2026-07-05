# ADK Implementation Guide

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Engineering

---

## Google ADK (Agent Development Kit)

The project uses Google ADK (`google-adk>=2.0.0`) for multi-agent orchestration.

### ADK Lifecycle Alignment

| Phase | Status | Notes |
|-------|--------|-------|
| 0 — Understand | ✅ Complete | AGENTS.md, functional requirements, architecture docs |
| 1 — Study Samples | ✅ Complete | ADK_SAMPLES_SUMMARY.md (ambient-expense, data-science, safety-plugins) |
| 2 — Scaffold | ✅ Complete | `agents-cli-manifest.yaml` |
| 3 — Build | ✅ Complete | All 9 agents wired with MCP tools |
| 3.5 — Datastore | ⚠️ Custom | Custom RAG pipeline (no documents ingested yet) |
| 4 — Evaluate | ✅ Complete | 29 cases, 4 metrics, local runner, 4.34/5.0 |
| 5 — Deploy | ❌ Not started | Cloud Run target configured, not deployed |
| 6 — Publish | ❌ N/A | Optional (Gemini Enterprise) |
| 7 — Observe | ❌ Not started | Cloud Trace, BigQuery Analytics planned |

### Agent Construction

Each agent is defined in `agents/{name}/agent.py`:

```python
from google.adk.agents import Agent

crop_analyst_agent = Agent(
    name="crop_analyst",
    model="gemini-2.5-flash",
    instruction="...detailed system prompt...",
    tools=[...MCP tools...],
    sub_agents=[...optional sub-agents...],
)
```

### Coordinator Pattern

The coordinator (`agents/coordinator/agent.py`) is the root agent that routes to 9 specialists:

```python
coordinator_agent = Agent(
    name="krishi_sastri",
    model="gemini-2.5-flash",
    instruction="...coordinator system prompt...",
    sub_agents=[
        crop_analyst_agent, weather_advisor_agent, market_advisor_agent,
        pest_detector_agent, irrigation_advisor_agent, farmer_interaction_agent,
        knowledge_retriever_agent, simulation_agent, dashboard_agent,
    ],
    before_agent_callback=safety_before_agent,
    after_agent_callback=safety_after_agent,
)
```

### MCP Tool Wiring

MCP servers are registered in `mcp_servers/mcp_registry.json` and imported by agents:

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

weather_tools = MCPToolset(
    transport="stdio",
    command="python",
    args=["-m", "mcp_servers.weather.server"],
)
```

### Running the Agent

```bash
# Via ADK playground (port 8080)
uv run python -m app.agent

# Via FastAPI (port 8000) — UI + SSE
uv run uvicorn app.fast_api_app:app --port 8000

# Via agents-cli playground
agents-cli playground
```

### Model Configuration

- **Model:** `gemini-2.5-flash` (via Gemini API key, not ADC)
- **Note:** The local eval runner uses the Gemini API key directly via `Runner.run_async()` to bypass the agents-cli ADC requirement
- **Retry:** Configured via `retry_options` in agent definitions
- **Never change the model** unless explicitly asked

### Common ADK Gotchas

| Issue | Solution |
|-------|----------|
| Model 404 error | Fix `GOOGLE_CLOUD_LOCATION` (use `global` instead of `us-east1`), not the model name |
| ADK tool imports | Import the tool instance, not the module: `from google.adk.tools.load_web_page import load_web_page` |
| Eval requires ADC | Use the local eval runner (`tests/eval/run_local_eval.py`) with Gemini API key |
| Run Python with `uv` | `uv run python script.py` |

## Related Documents

- [Development Guide](development-guide.md)
- [Agent Architecture](../02-architecture/agent-architecture.md)
- [GEMINI.md](../../GEMINI.md) — ADK development commands
- [ADK Lifecycle Alignment Plan](../08-roadmap/current-status-and-roadmap.md)