# Lifecycle Mapping

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Architecture / DevSecOps

---

## Two Lifecycle Frameworks Reconciled

The project has two lifecycle models that serve different purposes but overlap in Build/Test/Deploy phases. This document maps them.

### 1. Google ADK Lifecycle (Agent Development Workflow)

| Phase | Name | Status | AI-SDLC Agents Involved |
|-------|------|--------|-------------------------|
| 0 | Understand | ✅ Complete | Requirements Agent |
| 1 | Study Samples | ✅ Complete | Architecture Agent |
| 2 | Scaffold | ✅ Complete | DevOps Agent |
| 3 | Build | ✅ Complete | Developer Agent, UX Agent |
| 3.5 | Datastore | ⚠️ Custom RAG | Architecture Agent |
| 4 | Evaluate | ✅ Complete | Test Agent, Safety Agent |
| 5 | Deploy | ❌ Not started | DevOps Agent, Security Agent |
| 6 | Publish | ❌ N/A | (optional — Gemini Enterprise) |
| 7 | Observe | ❌ Not started | Observability Agent (YAML created, implementation pending) |

### 2. AI-SDLC Lifecycle (Software Engineering Governance)

| Stage | Agent | Evidence | ADK Phase Equivalent |
|-------|-------|----------|---------------------|
| Requirements | Requirements Agent | `requirement-analysis-report.json` | Phase 0 |
| Architecture | Architecture Agent | `architectural-impact-evidence.json` | Phase 0-1 |
| Implementation | Developer Agent | `developer-selfcheck.json` | Phase 3 |
| UX Review | UX/Accessibility Agent | `ux-accessibility-evidence.json` | Phase 3 |
| Testing | Test Agent | `test-run-evidence.json` | Phase 4 |
| Security | Security Agent | `security-audit-evidence.json` | Phase 4-5 |
| Safety Review | Safety Review Agent | `agricultural-safety-evidence.json` | Phase 4 |
| DevOps | DevOps Agent | `devops-build-evidence.json` | Phase 5 |
| Release | Release Agent | `release-summary.json` | Phase 5-6 |
| Documentation | Documentation Agent | `documentation-update-evidence.json` | All phases |
| **Observe** | **Observability Agent** | `observability-health-evidence.json` | **Phase 7** |

## ~~Gap: Phase 7 Observability Agent~~ ✅ Resolved

The AI-SDLC framework now includes an **Observability Agent** (`observability_agent.yaml`) for Phase 7.

**Responsibilities:**
- Monitor Cloud Trace spans for agent routing decisions and tool call latency
- Review prompt-response logging for safety status and language correctness
- Analyze BigQuery Agent Analytics for trends and drift detection
- Trigger continuous eval re-runs when drift is detected
- Alert on safety kernel block rate anomalies

## Evidence Flow

```
ADK Phase 0          → Requirements Agent → requirement-analysis-report.json
    ↓
ADK Phase 1-2        → Architecture Agent → architectural-impact-evidence.json
    ↓
ADK Phase 3          → Developer Agent → developer-selfcheck.json
                       UX Agent → ux-accessibility-evidence.json
    ↓
ADK Phase 4          → Test Agent → test-run-evidence.json
                       Safety Agent → agricultural-safety-evidence.json
                       (eval flywheel → grade_results)
    ↓
ADK Phase 5          → Security Agent → security-audit-evidence.json
                       DevOps Agent → devops-build-evidence.json
    ↓
Release Agent         → release-summary.json
                       (aggregates all evidence → readiness scorecard)
    ↓
[HUMAN GATE]          → approvals.json
    ↓
ADK Phase 7          → (Missing: Observability Agent)
```

## Per-Feature Document Set

Every feature should produce:

```
specs/{NNN}-{feature-name}/
├── spec.md                 # Business goal, scope, personas, constraints
├── plan.md                 # Implementation sequence, repository boundaries
├── tasks.md                # Checklist of small changes
├── acceptance-criteria.md  # Observable pass/fail behavior
├── test-plan.md            # Unit, API, browser, eval, release checks
└── evidence.md             # Command output, API samples, eval results
```

## Related Documents

- [AI-SDLC Operating Model](ai-sdlc-operating-model.md)
- [Agent Skills Operating Model](agent-skills-operating-model.md)
- [ADR-AAA-003: Agent-Skills-Based AI-SDLC](../02-architecture/adr/ADR-AAA-003-agent-skills-based-ai-sdlc.md)
- [Current Status & Roadmap](../08-roadmap/current-status-and-roadmap.md)