# Observability Guide

> **Status:** Draft — Not Yet Implemented
> **Last Updated:** 2026-07-04
> **Owner:** DevOps

---

## Current State

Observability is **not yet implemented**. This document describes the planned observability architecture for the production deployment.

## Planned Observability Stack

### 1. Cloud Trace (Agent Spans)

**Purpose:** Trace agent execution spans to understand routing decisions, tool call latency, and response quality.

| Span | Purpose |
|------|---------|
| Coordinator span | End-to-end query processing time |
| Sub-agent span | Per-specialist routing and processing |
| MCP tool span | Tool call latency (weather, market, OKF) |
| Safety kernel span | Pre/post validation time |

**Implementation:** ADK supports OpenTelemetry tracing. Setup must occur **before** importing ADK modules.

```python
# In app/fast_api_app.py — BEFORE importing ADK
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceExporter
# ... setup tracing
from google.adk.agents import Agent  # Import AFTER tracing setup
```

### 2. Prompt-Response Logging

**Purpose:** Log all agent prompts and responses for quality monitoring and debugging.

| Field | Type | Purpose |
|-------|------|---------|
| timestamp | datetime | When the query was processed |
| farmer_id | string | Which farmer asked |
| language | string | Response language |
| agent_name | string | Which agent handled it |
| tool_calls | list | Which tools were called |
| response_length | int | Response word count |
| safety_status | string | PASS / BLOCKED / ESCALATED |
| latency_ms | int | Processing time |
| confidence | float | Agent confidence score |

### 3. BigQuery Agent Analytics

**Purpose:** Aggregate metrics for trend analysis and drift detection.

**Planned Tables:**
- `agent_queries` — All farmer queries with metadata
- `agent_responses` — All agent responses with safety status
- `agent_tool_calls` — All MCP tool invocations with latency
- `agent_eval_results` — Evaluation flywheel results over time

**Planned Dashboards:**
- Response latency by agent
- Safety kernel block rate
- Language distribution
- Tool call frequency
- Escalation rate
- Eval score trend (drift detection)

### 4. Continuous Eval Flywheel

**Purpose:** Automatically re-run eval suite on schedule to detect quality degradation.

**Planned Schedule:**
- Run eval suite daily (29 cases × 4 metrics)
- Compare to baseline (4.34/5.0)
- Alert if overall score drops below 4.0
- Alert if any safety metric drops below 5.0

## Missing Observability Agent

The AI-SDLC framework needs an **Observability Agent** (`observability_agent.yaml`) for Phase 7.

**Recommended responsibilities:**
- Monitor deployed agent performance via Cloud Trace
- Review prompt-response logging quality
- Analyze BigQuery Agent Analytics for trends
- Detect production drift via continuous eval
- Trigger eval re-runs when drift is detected
- Alert on safety kernel block rate anomalies

## Related Documents

- [Runbook](runbook.md)
- [Known Limitations](known-limitations.md)
- [Lifecycle Mapping](../06-devsecops/lifecycle-mapping.md) (Phase 7 gap)
- [ADK Implementation Guide](../04-engineering/adk-implementation-guide.md)