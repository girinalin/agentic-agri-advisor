# Farmer UX Guidelines

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** UX / Product

---

## Design Philosophy

Krishi Sampark is designed for **smallholder farmers with limited technical literacy**. The UX must be:

1. **Voice-first** — The primary interaction mode is speaking, not typing
2. **Visual** — Cards, icons, and color-coded indicators replace text-heavy UI
3. **Warm** — The Krishi Sastri persona is a wise village scholar, not a chatbot
4. **Language-pure** — No technical terms, no English leaks in non-English modes
5. **Offline-resilient** — UX must gracefully handle zero connectivity

## Farmer Mode Persona: Krishi Sastri

| Attribute | Rule |
|-----------|------|
| Persona | Warm village agriculture scholar (कृषि शास्त्री) |
| Response length | Under 80 words |
| Markdown | No markdown symbols (`**`, `#`, `---`) in farmer-facing responses |
| Bullet lists | Max 4 bullets, each with a reason or action |
| Internal agent names | Hidden — never mention "Crop Analyst", "Irrigation Planner", "pathologist" |
| Technical terms | Translate to farmer-friendly terms (NPK → खाद, evapotranspiration → पानी की जरूरत) |
| Greeting | Use farmer's name from profile (e.g., "नमस्ते माधव जी") |
| Uncertainty | Honest admission: "मुझे इसकी पक्की जानकारी नहीं है" + offer escalation |

## Color System

| Color | Usage | Hex |
|-------|-------|-----|
| Brand Green | Primary actions, header gradient | `#2C6B37` / `#4CAF50` |
| Light Green | Backgrounds, cards | `#E8F5E9` |
| Cream | Page background (light theme) | `#F5F7F4` |
| White | Cards, panels | `#FFFFFF` |
| Warning Yellow | Medium-priority alerts | `#F9A825` |
| Error Red | Critical alerts, banned chemicals | `#D32F2F` |
| Success Green | Good status indicators | `#43A047` |

### Theme Modes

- **Light theme** (default): Warm cream background, white cards, green gradient header
- **Dark theme** (toggle via 🌙): Dark background, dark panels, green accents
- Header uses `linear-gradient(135deg, #2C6B37, #4CAF50)` in light mode

## Touch Targets

- Minimum touch target: **44×44 pixels** (WCAG recommendation)
- Enforced via `@media (pointer: coarse)` on all interactive elements
- Buttons in nav bar: full-width with icon + text
- Quick action cards: large tappable areas, no hover-only interactions
- `touch-action: manipulation` removes 300ms tap delay
- `-webkit-tap-highlight-color: transparent` removes gray flash on tap

## Typography

- Primary font: Outfit (Google Web Font), loaded via service worker cache
- Body text size: 16px minimum (farmers may have vision issues)
- Heading sizes: Fluid via `clamp()` — H1 scales from 28px to 68px based on viewport
- Line height: 1.5 for readability

## Voice UX

- Microphone button is always visible (🎙️ icon)
- TTS auto-enables when response arrives
- Language detection handles both full names ("Hindi") and BCP-47 codes ("hi")
- Backend neural male voices preferred for Hindi (Madhur, Manohar, Mohan)
- Mic indicator shows active state (pulsing) and inactive state (static)

## Offline UX

- Header shows "ऑफलाइन एज AI" (Offline Edge AI) badge when disconnected
- Failed API calls show friendly fallback, not error pages
- Activities are queued silently and synced when connectivity returns
- No "Loading..." spinners for cached data — show immediately

## Related Documents

- [Responsive Design](responsive-design.md)
- [Navigation & Screen Flow](navigation-and-screen-flow.md)
- [Localization Guidelines](localization-guidelines.md)
- [Accessibility Guidelines](accessibility-guidelines.md)
- [Personas & User Journeys](../01-product/personas-and-user-journeys.md)