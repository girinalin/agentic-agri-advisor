# Product Vision

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Product / Lead AI Solutions Architect

---

## Vision Statement

**Krishi Sampark** (कृषि संपर्क — "Agricultural Connection") is an offline-first, voice-first multi-agent agricultural intelligence platform for **smallholder farmers in India and Sub-Saharan Africa**.

The vision is to digitally bring the traditional village agriculture advisor — the **Krishi Sastri** (कृषि शास्त्री) — to every farmer's pocket, delivering personalized, scientifically-grounded advice at zero ongoing API cost.

---

## The Opportunity

- **500M+ smallholders** across India and Sub-Saharan Africa face volatile climates, crop diseases, and fluctuating market prices.
- Traditional solutions rely on village elders and agricultural extension officers who are overwhelmed and geographically sparse.
- Generic AI advice fails because it doesn't account for the farmer's specific soil, crop stage, irrigation setup, or local market conditions.
- Cloud API costs make per-query pricing models prohibitive for the target demographic.

## What We Built

A multi-agent system (coordinator + 9 specialists) with:

1. **Four intelligence layers** — OKF knowledge graph → Dynamic MCP APIs → RAG document search → Edge PWA offline models
2. **Hybrid edge-cloud routing** — simple queries handled locally, complex queries routed to cloud specialists
3. **Offline-first PWA** — IndexedDB sync queue, service worker caching, installable on any smartphone
4. **Zero-cost voice** — Browser-native STT/TTS at $0 API cost, with backend neural voice fallback
5. **Multi-language support** — English, Hindi, Marathi, Telugu, Swahili
6. **Agricultural Safety Kernel** — Banned chemical enforcement, dosage limits, pre-harvest interval checks, escalation queue

## Value Proposition

| Stakeholder | Value |
|-------------|-------|
| **Farmer** | Personalized advice in their language, available offline, via voice — no technical knowledge needed |
| **Agronomist** | Escalation queue for complex cases, confidence-scored diagnoses, safety-compliant recommendations |
| **Government/NGO** | Scalable advisory platform reaching millions at near-zero marginal cost |
| **Platform Operator** | Google ADK-native, MCP-decoupled, eval-flywheel-validated, deployment-ready |

## Guiding Principles

1. **Farmer-first UX** — No technical terms in farmer mode. Warm village-scholar persona. Under 80 words per response.
2. **Offline-first** — The app must work with zero connectivity for core functionality.
3. **Safety by design** — Every prescriptive recommendation passes through the Agricultural Safety Kernel.
4. **Evidence-driven** — AI-SDLC lifecycle with command-backed evidence, traceability matrix, and human approval gates.
5. **Zero marginal cost** — Browser-native voice, local models, and rule-based fallbacks eliminate per-query API costs.

## Success Criteria

- Farmer can complete a full advisory session (ask question → get answer → log activity) entirely offline
- All chemical/pesticide recommendations pass through the Safety Kernel with 100% compliance
- Evaluation flywheel achieves ≥4.0/5.0 across all metrics
- App installs on any Android smartphone with <2GB RAM and remains functional
- Supports 5 languages with zero script contamination (no Devanagari in Telugu mode, etc.)

## Related Documents

- [Problem Statement](problem-statement.md)
- [Personas & User Journeys](personas-and-user-journeys.md)
- [Functional Requirements](functional-requirements.md)
- [Non-Functional Requirements](non-functional-requirements.md)