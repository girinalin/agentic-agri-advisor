# Future Roadmap

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Product / Architecture

---

## Short-term (Next 2 Weeks)

| Item | Description | Effort |
|------|-------------|--------|
| Bundle TFLite model | Download PlantVillage TFLite model (~15MB), wire real inference in `crop_classifier.js` | 2 hours |
| Regenerate evidence | Run `make ai-sdlc-check` to update all evidence against current commit | 30 min |
| Update traceability matrix | Link new ADRs to requirements in `.ai-sdlc/reports/traceability-matrix.json` | 30 min |
| Deploy to Cloud Run | `agents-cli deploy` after human approval | 2 hours |
| Add Observability Agent | Create `observability_agent.yaml` in `.ai-sdlc/agents/` for Phase 7 | 1 hour |

## Medium-term (Next 1-2 Months)

| Item | Description | Effort |
|------|-------------|--------|
| Real Gemma 2B loader | Host model on CDN, implement real `@mediapipe/tasks-genai` inference | 1 day |
| RAG document ingestion | Collect agronomy manuals, generate embeddings, populate vector index | 2 days |
| data.gov.in integration | Get API key, integrate real mandi prices for Indian farmers | 1 day |
| Soil test OCR extraction | Use Gemini Vision to extract values from uploaded PDF/photo soil reports | 1 day |
| Authentication | Add session-based authentication for farmer profiles | 2 days |
| Rate limiting | Add rate limits to SSE and API endpoints | 4 hours |
| Escalation queue persistence | Move from in-memory to SQLite for durability | 4 hours |
| EXIF stripping | Strip EXIF metadata from uploaded photos | 2 hours |
| Audit logging | Log all safety kernel decisions (block, escalate, pass) | 4 hours |
| Observability setup | Cloud Trace spans, prompt-response logging, BigQuery analytics | 3 days |

## Long-term (3-6 Months)

| Item | Description |
|------|-------------|
| WhatsApp voice-note integration | Farmers send voice notes via WhatsApp, routed to agent system |
| IoT soil moisture sensor telemetry | Low-cost IoT probes report moisture to farm twin |
| Comprehensive pesticide registry | Expand from 10 to 100+ pesticides with full regulatory data |
| Conflict resolution for offline sync | Implement merge strategies for concurrent edits |
| iOS push notifications | Native iOS app or PWA push for crop alerts |
| Multi-farm management | Support farmers with multiple fields across different locations |
| Community knowledge sharing | Farmers share successful treatments with nearby farmers |
| Government scheme integration | Link to PM-Kisan, crop insurance, and subsidy schemes |
| Offline model fine-tuning | Fine-tune Gemma 2B on agricultural data for better local responses |
| Continuous eval automation | Scheduled eval runs with drift detection and alerting |

## Architecture Evolution

```
Current State → Near-term → Long-term
─────────────────────────────────────────
Manual entry → OCR extraction → IoT sensor auto-ingest
Yahoo Finance → data.gov.in → Real-time mandi WebSocket
Rule-based offline → Gemma 2B offline → Fine-tuned Gemma agri
In-memory escalation → SQLite escalation → Human agronomist dashboard
No auth → Session auth → JWT + biometric
Single region → Multi-region → Edge CDN caching
```

## Related Documents

- [Current Status & Roadmap](current-status-and-roadmap.md)
- [Known Limitations](../07-operations/known-limitations.md)
- [Kaggle Capstone Submission Guide](kaggle-capstone-submission-guide.md)