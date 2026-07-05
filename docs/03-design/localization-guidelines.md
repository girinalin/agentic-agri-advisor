# Localization Guidelines

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** UX / Engineering
> **Related ADR:** [ADR-AAA-001](../02-architecture/adr/ADR-AAA-001-multilingual-ui-architecture.md)

---

## Supported Languages

| Code | Language | Script | Locale |
|------|---------|--------|--------|
| `en` | English | Latin | en-US |
| `hi` | Hindi | Devanagari | hi-IN |
| `mr` | Marathi | Devanagari | mr-IN |
| `te` | Telugu | Telugu | te-IN |
| `sw` | Swahili | Latin | sw-KE |

## Translation Key System

All UI strings are defined in `ui/agui/translations.js` using a flat key-value dictionary:

```javascript
const TRANSLATIONS = {
  hi: {
    nav_home: "होम",
    nav_farm: "मेरा खेत",
    nav_soil: "मिट्टी जांच",
    // ...
  },
  te: {
    nav_home: "హోమ్",
    nav_soil: "మట్టి పరీక్ష",
    // ...
  },
};
```

## Rules

### 1. Every Key Must Exist in All 5 Languages
Missing keys show the raw key name (e.g., `nav_soil` instead of "मिट्टी जांच"), which is a UX defect.

**Validation:** `make validate-translations`

### 2. Script Purity
- Hindi mode (hi) must contain **zero Telugu** script characters
- Telugu mode (te) must contain **zero Devanagari** characters
- Hindi and Marathi share Devanagari script — both are valid in each mode
- English and Swahili share Latin script — both are valid

**Validation:** `make validate-translations` (detects mixed scripts)

### 3. Preserve Proper Nouns
Farmer names (e.g., "माधव जी", "మాధవ్ జీ") and regional locations must remain untranslated. These come from the farmer profile and are displayed as-is.

### 4. Voice Language Codes (BCP-47)

| Language | STT Code | TTS Voice Names |
|----------|---------|-----------------|
| Hindi | hi-IN | Madhur, Manohar, Mohan |
| Marathi | mr-IN | (browser default) |
| Telugu | te-IN | (browser default) |
| Swahili | sw-KE | Rafiki |
| English | en-US | (browser default) |

**File:** `ui/agui/voice.js` — `VOICE_MAP` handles both full language names and BCP-47 codes.

### 5. Cache-Busting
All script tags in `index.html` use `?v=N` query parameters to force browser cache invalidation on updates:
```html
<script src="translations.js?v=6"></script>
<script src="dashboard.js?v=15"></script>
<script src="voice.js?v=6"></script>
```

## Common Translation Pitfalls

| Pitfall | Solution |
|---------|----------|
| Raw key showing in UI | Key not added to all 5 language dictionaries |
| English leaking in Hindi mode | Technical term not translated (e.g., "NPK" should be "खाद") |
| Browser caches old translations | Bump `?v=N` in script tag |
| Voice reads English for Hindi | Language detection doesn't handle "Hindi" vs "hi" — `voice.js` v6 fixes this |
| Marathi field name mismatch | Check exact spelling (e.g., "माझा शेत" not "माझे खेत") |

## Related Documents

- [ADR-AAA-001: Multilingual UI Architecture](../02-architecture/adr/ADR-AAA-001-multilingual-ui-architecture.md)
- [Farmer UX Guidelines](farmer-ux-guidelines.md)
- [Accessibility Guidelines](accessibility-guidelines.md)