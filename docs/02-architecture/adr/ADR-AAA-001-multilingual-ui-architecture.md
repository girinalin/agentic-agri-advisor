# ADR-AAA-001: Multilingual UI Architecture

> **Status:** Accepted
> **Date:** 2026-07-04
> **Related Requirements:** REQ-AAA-001

---

## Context

Krishi Sampark serves farmers across India (Hindi, Marathi, Telugu) and Sub-Saharan Africa (Swahili), plus English as a fallback. The UI must support 5 languages with instant switching, script purity (no Devanagari in Telugu mode), and translated farmer-facing content while preserving proper nouns.

Existing approaches considered:
1. **Server-side rendering** with per-language templates — requires page reload, high latency
2. **i18n library** (e.g., i18next) — adds dependency, over-engineered for 5 languages
3. **Custom translation key map** — lightweight, instant, full control over script purity

## Decision

Implement a **custom translation key system** in vanilla JavaScript with a `TRANSLATIONS` dictionary per language and a `NAV_SECTIONS` array for navigation items.

**File:** `ui/agui/translations.js`

**Structure:**
```javascript
const NAV_SECTIONS = [
  { id: 'home', icon: '🏠', trKey: 'nav_home' },
  { id: 'farm', icon: '🌱', trKey: 'nav_farm' },
  { id: 'soil', icon: '🧪', trKey: 'nav_soil' },
  ...
];

const TRANSLATIONS = {
  en: { nav_home: "Home", nav_soil: "Soil Test", ... },
  hi: { nav_home: "होम", nav_soil: "मिट्टी जांच", ... },
  mr: { nav_home: "होम", nav_soil: "माती तपासणी", ... },
  te: { nav_home: "హోమ్", nav_soil: "మట్టి పరీక్ష", ... },
  sw: { nav_home: "Nyumbani", nav_soil: "Upimaji Udongo", ... },
};
```

**Cache-busting:** All script tags use `?v=N` query parameters to force browser reload on updates.

## Rationale

- **Instant switching:** Dictionary lookup is O(1), no server round-trip, no page reload
- **Zero dependencies:** Vanilla JS, no npm packages needed for the PWA
- **Script purity control:** Custom validation (`make validate-translations`) checks for cross-script contamination
- **Farmer names preserved:** Names like "माधव जी" are stored in the profile and displayed as-is regardless of UI language
- **Developer clarity:** Every UI string has a key, making it obvious when a translation is missing

## Consequences

**Positive:**
- Language switching is instant (<100ms)
- All 5 languages are complete and validated
- Adding a 6th language requires only adding a new dictionary
- Script purity is enforceable via CLI validation

**Negative:**
- Every new UI string requires manual translation in all 5 languages
- No automatic fallback to English for missing keys (shows raw key name)
- Translation file grows linearly with UI complexity

## Related Artifacts

- `ui/agui/translations.js` — Translation dictionary (5 languages)
- `ui/agui/dashboard.js` — Language switching logic
- `tools/ai_sdlc/validate_translations.py` — Validation script
- `Makefile` — `make validate-translations` target
- `.ai-sdlc/skills/localization-validation/SKILL.md`

## Validation Approach

```bash
make validate-translations  # Checks all keys present in all 5 languages
# Manual: Switch languages in browser, verify no raw keys visible
# Manual: Verify Hindi mode has zero Telugu characters and vice versa
```