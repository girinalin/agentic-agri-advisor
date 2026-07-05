# Accessibility Guidelines

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** UX

---

## Target Users

Our farmers may have:
- Limited literacy (visual and textual)
- Vision impairments (uncorrected presbyopia common in 40+ age group)
- Limited smartphone experience
- Slow 2G/3G connections (no heavy assets)

## WCAG 2.1 AA Compliance Targets

### Perceivable

| Guideline | Requirement | Implementation |
|-----------|-------------|-----------------|
| 1.1.1 Non-text content | All images have alt text | Icons have `aria-label` attributes |
| 1.3.1 Info and relationships | Semantic HTML | Use `<nav>`, `<main>`, `<section>`, `<button>` |
| 1.4.3 Contrast (minimum) | 4.5:1 for normal text | Brand green `#2C6B37` on white = 5.2:1 ✅ |
| 1.4.4 Resize text | 200% zoom without loss | Responsive layout, rem-based sizing |

### Operable

| Guideline | Requirement | Implementation |
|-----------|-------------|-----------------|
| 2.1.1 Keyboard accessible | All actions via keyboard | All buttons and links are focusable |
| 2.4.1 Bypass blocks | Skip to main content | (TODO: Add skip-link) |
| 2.4.6 Headings and labels | Descriptive labels | All form fields have `<label>` elements |
| 2.5.5 Target size | ≥44×44px touch targets | Nav links and action buttons meet minimum |

### Understandable

| Guideline | Requirement | Implementation |
|-----------|-------------|-----------------|
| 3.1.1 Language of page | `<html lang="hi">` | Updated dynamically on language switch |
| 3.2.3 Consistent navigation | Same nav across screens | Left sidebar is persistent |
| 3.3.2 Labels or instructions | Form fields labeled | All soil test fields have labels |

### Robust

| Guideline | Requirement | Implementation |
|-----------|-------------|-----------------|
| 4.1.2 Name, role, value | ARIA attributes | Buttons have `role="button"`, nav has `aria-label` |
| 4.1.3 Status messages | ARIA live regions | Toast notifications use `role="alert"` |

## Voice-First Accessibility

Voice is the primary accessibility feature for low-literacy users:

- **STT:** Tap 🎙️ and speak — no typing needed
- **TTS:** Auto-reads agent responses aloud in farmer's language
- **Backend neural voices:** Male voices (Madhur, Manohar, Mohan, Rafiki) for cultural preference
- **Language detection:** Handles both "Hindi" and "hi-IN" format automatically

## Color-Blind Friendly Design

- Status indicators use both **color AND emoji**: 🟢 (good), 🟡 (warning), 🔴 (critical)
- Charts use patterns/labels, not color alone
- Dark mode maintains contrast ratios

## Mobile-Specific Guidelines

- No hover-only interactions (touch devices have no hover)
- Pull-to-refresh disabled (prevents accidental refresh losing chat history)
- Bottom nav bar on mobile (thumb-reachable zone)
- Camera opens rear lens by default (`facingMode: "environment"`)

## Known Gaps

- [ ] Skip-to-main-content link not implemented
- [ ] Screen reader testing not performed
- [ ] ARIA live regions for chat updates need improvement
- [ ] High contrast mode not tested

## Related Documents

- [Farmer UX Guidelines](farmer-ux-guidelines.md)
- [Navigation & Screen Flow](navigation-and-screen-flow.md)
- [Localization Guidelines](localization-guidelines.md)