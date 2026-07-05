# ADR-AAA-004: Edge-Cloud Advisor Routing

> **Status:** Accepted
> **Date:** 2026-07-04
> **Related Requirements:** REQ-AAA-011

---

## Context

Farmers have intermittent connectivity and varying device capabilities. A single routing strategy doesn't work:
- A simple greeting shouldn't cost an API call
- A complex disease diagnosis needs the full multi-agent system
- Offline queries need local knowledge and rule-based fallback
- Device capability varies from 2GB RAM budget phones to 8GB flagships

Approaches considered:
1. **Always cloud** — Requires connectivity, costs API budget per query
2. **Always local** — Can't handle complex queries, limited knowledge
3. **Automatic routing based on query complexity** — Opaque to user, hard to debug
4. **Explicit user-selected advisor mode + connectivity-aware routing** — Transparent, user-controlled

## Decision

Implement **explicit advisor mode selection** with two modes, combined with connectivity-aware routing:

### Two Advisor Modes

1. **Krishi Sastri (कृषि शास्त्री)** — Free, offline-capable local advisor
   - Online: Routes to cloud Gemini agent using OKF tools
   - Offline: Uses OKF knowledge cache (IndexedDB) + rule-based responses
   - Can escalate to Visheshagya when confidence is low

2. **Krishi Visheshagya (कृषि विशेषज्ञ)** — Cloud-based expert
   - Online: Full multi-agent specialist system with real-time APIs
   - Offline: Shows "Internet Required" + queues for when online

### Three-Tier Device Classification

| Tier | Detection | Classification | Routing |
|------|-----------|---------------|---------|
| Tier 1 | WebGPU + ≥4GB RAM | High-end | Full local models (Gemma 2B + TFLite) |
| Tier 2 | WebGL + ≥2GB RAM | Mid-range | TFLite + rule-based Gemma fallback |
| Tier 3 | No GPU or <2GB RAM | Budget | Rule-based only, cloud for everything else |

### Escalation Flow

When Krishi Sastri encounters low confidence:
1. Shows honesty statement: "मुझे इसकी पक्की जानकारी नहीं है।"
2. Offers escalation prompt with "हाँ/नहीं" buttons
3. If yes → Expert form opens (crop, symptom, photo, urgency)
4. Routes to full cloud multi-agent system
5. Safety kernel verifies all recommendations

## Rationale

- **Explicit choice:** Farmer knows what they're getting (free vs paid, simple vs expert)
- **Cost control:** Sastri mode is $0 per query; Visheshagya uses API budget only when needed
- **Offline resilience:** Sastri mode works with zero connectivity via OKF cache
- **Safety escalation:** Sastri can't handle complex diagnoses → escalates to Visheshagya → human agronomist
- **Device-aware:** Three-tier classification ensures budget devices don't crash on Gemma 2B

## Consequences

**Positive:**
- Farmer controls cost (Sastri is free)
- Offline queries work (OKF cache)
- Budget devices supported (rule-based fallback)
- Complex cases get full expert treatment

**Negative:**
- Two modes add UI complexity (mitigated by clear card-based selection)
- OKF cache must be populated on first online sync
- Gemma 2B not bundled yet (Tier 1 devices use rule-based until model downloaded)
- TFLite model not bundled yet (classification uses color heuristic fallback)

## Related Artifacts

- `ui/agui/dashboard.js` — Advisor selection flow, escalation prompts, expert form
- `ui/agui/device_capabilities.js` — WebGPU/WebGL/camera/voice detection
- `ui/agui/crop_classifier.js` — TFLite classifier with fallback
- `docs/02-architecture/edge-cloud-advisor-architecture.md`
- `docs/02-architecture/hybrid-intelligence-strategy.md`

## Validation Approach

```bash
# Manual: Select Sastri, ask "What is wheat rust?" → verify local response
# Manual: Select Visheshagya, ask complex question → verify multi-agent response
# Manual: Enable airplane mode, use Sastri → verify offline OKF cache response
# Manual: Trigger escalation in Sastri → verify expert form opens
# Manual: Test on budget device (2GB RAM) → verify rule-based fallback works
```