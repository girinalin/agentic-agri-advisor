# Current Status & Roadmap

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Product / Architecture

---

## ADK Lifecycle Status

| Phase | Name | Status | Notes |
|-------|------|--------|-------|
| 0 | Understand | ✅ Complete | AGENTS.md, functional requirements, architecture docs |
| 1 | Study Samples | ✅ Complete | ADK_SAMPLES_SUMMARY.md (ambient-expense, data-science, safety-plugins) |
| 2 | Scaffold | ✅ Complete | `agents-cli-manifest.yaml` |
| 3 | Build | ✅ Complete | All 9 agents wired with MCP tools |
| 3.5 | Datastore | ⚠️ Custom | Custom RAG pipeline (no documents ingested yet) |
| 4 | Evaluate | ✅ Complete | 29 cases, 4 metrics, local runner, 4.34/5.0 |
| 5 | Deploy | ❌ Not started | Cloud Run target configured, not deployed |
| 6 | Publish | ❌ N/A | Optional (Gemini Enterprise) |
| 7 | Observe | ❌ Not started | Cloud Trace, BigQuery Analytics planned |

## Feature Completion

| Feature | Status | Details |
|---------|--------|---------|
| 9 critical bug fixes | ✅ Complete | All 9 agents wired with MCP tools |
| Market API (6 crops) | ✅ Complete | Yahoo Finance: corn, wheat, soybeans, cotton, rice, sugarcane |
| Weather API | ✅ Complete | Open-Meteo real data |
| OKF knowledge graph | ✅ Complete | 22 entities, search working |
| Safety kernel | ✅ Complete | 19/19 tests pass, validate_recommendation working |
| Eval flywheel | ✅ Complete | 29/29 generate, grading 4.34/5.0 |
| PWA | ✅ Complete | Service worker, install prompt, background sync, push, OKF sync |
| Voice STT/TTS | ✅ Complete | Backend male neural voices, language detection |
| Advisor flow | ✅ Complete | Two cards (Sastri + Visheshagya), escalation, expert form |
| Ask Image | ✅ Complete | Upload/camera + local analysis + expert delegation |
| Security hardening | ✅ Complete | Pre-commit, semgrep, threat model, tool validation |
| Soil test workflow | ✅ Complete | Database, API, UI screens, JS logic |
| Multilingual UI | ✅ Complete | 5 languages, script purity validated |
| Navigation redesign | ✅ Complete | 7 sections: Home, Farm, Soil, Ask, Photo, Market, More |

## What's Not Done

| Item | Priority | Effort |
|------|----------|--------|
| TFLite model not bundled | P1 | Download ~15MB model, wire real inference |
| Gemma 2B not bundled | P2 | Host ~1.4GB model on CDN, wire real inference |
| RAG pipeline has no documents | P2 | Collect agronomy manuals, generate embeddings |
| Deployment to Cloud Run | P1 | `agents-cli deploy` |
| Observability (Cloud Trace, BigQuery) | P2 | Set up tracing and analytics |
| data.gov.in API key for real mandi prices | P2 | Integrate with Indian government data portal |
| Evidence regeneration | P1 | `make ai-sdlc-check` |
| Observability Agent YAML | P2 | Fill Phase 7 gap in AI-SDLC framework |
| ADR traceability update | P1 | ADRs now created; update traceability matrix |

## Related Documents

- [Future Roadmap](future-roadmap.md)
- [Known Limitations](../07-operations/known-limitations.md)
- [Lifecycle Mapping](../06-devsecops/lifecycle-mapping.md)
- [Release Readiness](../06-devsecops/release-readiness.md)