# Problem Statement

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Product

---

## The Core Problem

Smallholder farmers in India and Sub-Saharan Africa lack access to timely, personalized, scientifically-grounded agricultural advice. The result is crop loss, over-application of chemicals, and economic vulnerability.

## Problem Breakdown

### 1. Advisory Scarcity

| Factor | Reality |
|--------|---------|
| Farmer-to-extension-officer ratio | ~1:1000+ in India |
| Geographic coverage | Extension officers cover multiple villages, visit infrequently |
| Knowledge currency | Officers may not have latest disease outbreak or market data |
| Language coverage | Advisory materials often only in English or Hindi, not regional languages |

### 2. Connectivity Constraints

- Rural internet is intermittent — 2G/3G with frequent outages
- Cloud-based AI services require persistent connectivity
- Per-query API costs ($0.01–0.05) are prohibitive at scale (500M farmers × daily queries)
- Voice is the natural interface but cloud STT/TTS adds cost and latency (1.5–3.0s)

### 3. Literacy & Language Barriers

- 40%+ of target farmers cannot read complex text in any language
- India has 22 scheduled languages; Sub-Saharan Africa has 100+
- Existing agriculture apps are text-heavy and English/Hindi-only
- Technical terminology (NPK, evapotranspiration, PHI) is meaningless to farmers

### 4. Generic Advice Fails

Generic AI advice doesn't work because:
- A farmer with 2 acres of sandy soil in Nagpur needs different irrigation advice than a farmer with 10 acres of clay soil in Punjab
- Crop stage matters — nitrogen recommendations for germination differ from vegetative stage
- Local market prices vary by mandi (market yard), not just national averages
- Disease outbreaks are hyper-local and seasonal

### 5. Safety Risks

Without guardrails, AI can recommend:
- **Banned chemicals** (e.g., endosulfan — prohibited in India since 2011)
- **Excessive dosages** that harm crops, soil, and human health
- **Violations of pre-harvest intervals** — chemicals applied too close to harvest
- **Off-label pesticide use** — chemicals applied to crops they're not approved for

## Current Alternatives & Their Limitations

| Alternative | Limitation |
|-------------|------------|
| Government extension officers | Too few, too slow, too generic |
| Agri-input dealers (shops) | Biased toward selling products, not agronomy |
- WhatsApp groups | Unverified information, rumor propagation |
| Existing agri-apps (e.g., Kisan Suvidha) | Text-heavy, English/Hindi only, no offline, no safety kernel |
| Generic LLM chatbots | No farm context, no safety guardrails, no local language, requires internet |

## The Krishi Sampark Solution

Krishi Sampark addresses each problem:

| Problem | Solution |
|---------|----------|
| Advisory scarcity | 9 specialist agents + coordinator, available 24/7 |
| Connectivity | Offline-first PWA with local models and IndexedDB cache |
| API cost | Browser-native STT/TTS ($0), rule-based offline fallback ($0), Edge TTS backend ($0) |
| Literacy | Voice-first interface, visual A2UI cards, 5 languages, no technical terms |
| Generic advice | Farmer Digital Twin (SQLite) — soil type, crop stage, irrigation, field size injected into every prompt |
| Safety | Agricultural Safety Kernel — banned chemicals, dosage limits, PHI, escalation queue |

## Related Documents

- [Product Vision](product-vision.md)
- [Personas & User Journeys](personas-and-user-journeys.md)