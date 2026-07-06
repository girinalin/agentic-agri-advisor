# Responsive Design & Device Adaptation

> **Status:** Active
> **Last Updated:** 2026-07-06
> **Owner:** UX / Engineering

---

## Overview

Krishi Sampark is a PWA that must work seamlessly across **mobile phones**, **tablets**, and **desktops**. This document describes the device detection system, responsive breakpoints, layout strategy, and touch optimizations that enable a single codebase to adapt to any screen size.

---

## Device Detection (`ui/device.js`)

A shared utility loaded on both the landing page and the internal app. It classifies the viewport and exposes `window.DeviceInfo`.

### Classification

| Device Type | Viewport Width | Typical Devices |
|-------------|---------------|-----------------|
| `mobile` | < 768px | Phones (iPhone, Android) |
| `tablet` | 768px – 1023px | iPads, Android tablets |
| `desktop` | ≥ 1024px | Laptops, desktops, large tablets |

### Detection Signals

| Signal | Source | Usage |
|--------|--------|-------|
| Viewport width | `window.innerWidth` | Primary classification |
| Orientation | width vs height | `portrait` / `landscape` |
| Touch | `matchMedia('(pointer: coarse)')` | Touch target sizing |
| User Agent | `navigator.userAgent` | Mobile/tablet override |
| Connection | `navigator.connection.effectiveType` | Data-saving mode |
| Device Pixel Ratio | `window.devicePixelRatio` | Image quality |

### HTML Data Attributes

The utility sets these attributes on `<html>` for CSS targeting:

```html
<html data-device="desktop" data-orientation="landscape" data-touch="false">
```

### Events

- `device:change` — Fired when the viewport crosses a breakpoint boundary (e.g., tablet → desktop). Other modules can listen and adapt.

### localStorage Keys

| Key | Value |
|-----|-------|
| `device_type` | `mobile` / `tablet` / `desktop` |
| `device_orientation` | `portrait` / `landscape` |
| `device_touch` | `true` / `false` |

---

## Breakpoint Strategy

### Landing Page (`ui/landing.css`)

| Breakpoint | Target | Key Changes |
|------------|--------|-------------|
| ≥ 1400px | Large desktop | Wider max-width (1320px) |
| ≥ 1024px | Desktop | 2-column hero, nav links visible, overlay panel |
| ≤ 1024px | Tablet | Hero stacks to 1-column, panel becomes inline card |
| ≤ 900px | Tablet/Mobile | Hamburger menu appears, nav links hidden |
| ≤ 680px | Mobile | Full-width buttons, compact hero, fluid typography |

### Internal App (`ui/agui/styles.css`)

| Breakpoint | Target | Key Changes |
|------------|--------|-------------|
| ≥ 1400px | Large desktop | More padding (2rem), wider chat pane (460px max) |
| ≥ 1024px | Desktop | Grid layout: sidebar + header + content + chat |
| 768–1023px | Tablet | Drawer sidebar (slides in), bottom nav hidden |
| ≤ 767px | Mobile | Bottom nav bar, chat pane slides as overlay, 💬 toggle button |

---

## Fluid Design Patterns

### Fluid Typography

All headings use `clamp()` to scale smoothly between minimum and maximum sizes:

```css
.hero-copy h1     { font-size: clamp(28px, 8vw, 68px); }
.brand-title      { font-size: clamp(18px, 2.2vw, 24px); }
.feature-card h4  { font-size: clamp(16px, 1.4vw, 20px); }
.how-section h3   { font-size: clamp(24px, 6vw, 42px); }
```

### Fluid Spacing

Padding and gaps use `clamp()` instead of fixed values:

```css
.topbar padding       { clamp(10px, 2vw, 14px) clamp(12px, 3vw, 24px); }
.hero padding         { clamp(14px, 2vw, 20px); }
.content-pane padding { clamp(0.75rem, 2vw, 1.5rem); }
```

### Fluid Chat Pane (Internal App)

The chat pane width scales with viewport:

```css
.chat-pane { flex: 0 0 clamp(300px, 32vw, 420px); }
```

- **300px minimum**: Readable on small tablets
- **32vw**: Scales proportionally with viewport
- **420px maximum**: Doesn't waste space on large desktops

### Auto-Fit Grids

Feature cards and trust strip use CSS auto-fit instead of fixed column counts:

```css
.cards-section    { grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); }
.conditions-grid  { grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr)); }
```

This means cards automatically arrange into 6 columns on desktop, 3 on tablet, 2 on small tablet, and 1 on mobile — without explicit breakpoints.

---

## Landing Page Layout

### Desktop (≥ 1024px)

```
┌─────────────────────────────────────────────────────────────┐
│  🌿 Krishi Sampark    About Features How It Works  [Lang] [Guest] │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────────────────────┐ │
│  │  Hero Copy        │  │  Hero Image                      │ │
│  │  "Your farming    │  │  ┌─────────────────────┐        │ │
│  │   companion..."   │  │  │ Works even with     │        │ │
│  │  [Guest] [Google] │  │  │ limited internet    │        │ │
│  │  🎙️ Voice Assist  │  │  │ (semi-transparent)  │        │ │
│  └──────────────────┘  └──┴─────────────────────┴────────┘ │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │
│  │Ask   │ │Photo │ │Soil  │ │Market│ │Plan  │ │Expert│    │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Tablet (768–1023px)

- Hero stacks to single column (copy above, image below)
- "Works even with limited internet" panel becomes an inline card below the image
- Hamburger menu replaces nav links
- Feature cards auto-arrange into 2–3 columns

### Mobile (< 768px)

- Compact hero with fluid heading (`clamp(28px, 8vw, 36px)`)
- Full-width action buttons (stacked vertically)
- Feature cards in single column
- Hamburger menu with slide-in drawer
- Bottom footer wraps to centered layout

---

## Internal App Layout

### Desktop (≥ 1024px)

```
┌──────────┬──────────────────────────────────────────────┐
│ Left Nav │  Green Gradient Header                        │
│ (always  ├────────────────────────┬─────────────────────┤
│  visible)│  Content Pane           │  Chat Pane          │
│          │  (schemas, cards)       │  (always visible)   │
│  🏠 Home │  padding: clamp(        │  flex: 0 0          │
│  🌱 Farm │    0.75rem, 2vw, 1.5rem)│    clamp(300px,     │
│  🧪 Soil │                         │    32vw, 420px)     │
│  💬 Ask  │                         │                     │
│  📷 Photo│                         │                     │
│  📈 Market│                        │                     │
│  📋 More │                         │                     │
│          │                         │                     │
│  👨‍🌾 माधव │                         │  🎙️ [input]    ➔   │
└──────────┴────────────────────────┴─────────────────────┘
```

### Tablet (768–1023px)

- Left nav becomes a **drawer** (slides in from left on ☰ tap)
- Bottom nav bar is hidden
- Chat pane is visible at 300px minimum width
- Content pane gets full width

### Mobile (< 768px)

- **Bottom nav bar** with 5 tabs (Home, Farm, Ask, Market, More)
- Chat pane is **hidden by default**, slides in as overlay via 💬 FAB
- Content pane takes full width with 12px padding
- All touch targets are minimum 44px

---

## Touch Optimizations

### `@media (pointer: coarse)`

Applied when the primary input is touch (phones, tablets):

```css
@media (pointer: coarse) {
  .btn, .nav-tab, .a2ui-btn, .send-btn, .mic-btn,
  .header-dropdown, .left-nav-item {
    min-height: 44px;  /* WCAG minimum */
  }
  .nav-drawer a {
    min-height: 48px;
    display: flex;
    align-items: center;
  }
  .text-input-bar input { height: 48px; }
  .send-action-btn { width: 48px; height: 48px; }
}
```

### Tap Delay Removal

```css
body {
  touch-action: manipulation;     /* removes 300ms tap delay */
  -webkit-tap-highlight-color: transparent;  /* no gray flash */
}
```

---

## Theme System

### Light Theme (Default)

| Variable | Value | Usage |
|----------|-------|-------|
| `--bg-dark` | `#f5f7f4` | Page background (warm cream) |
| `--panel-bg` | `#ffffff` | Cards, chat pane |
| `--sidebar-bg` | `#eef4ef` | Sidebar, inputs |
| `--border` | `#dce5dc` | Subtle borders |
| `--text-main` | `#1a2b1f` | Primary text |
| `--text-sub` | `#5a7361` | Secondary text |
| `--accent` | `#2C6B37` | Brand green |
| `--accent-light` | `#4CAF50` | Lighter green for gradients |
| `--header-gradient` | `linear-gradient(135deg, #2C6B37, #4CAF50)` | App header |
| `--card-shadow` | `0px 2px 16px rgba(0,0,0,0.05)` | Soft card shadows |
| `--radius-l` | `20px` | Large card radius |

### Dark Theme (Toggle via 🌙 button)

All dark theme variables are preserved in `.dark-theme` class. The toggle switches between `light-theme` and `dark-theme` on `<body>`.

---

## PWA Configuration

### Manifest (`ui/manifest.webmanifest`)

| Property | Value | Rationale |
|----------|-------|-----------|
| `display` | `standalone` | Native app feel |
| `orientation` | `any` | Allow landscape on tablets |
| `theme_color` | `#2C6B37` | Brand green |
| `background_color` | `#F3F7F2` | Light theme bg |

### Viewport Meta

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
```

`viewport-fit=cover` ensures content extends into notch areas on iPhone X+.

---

## Guest Onboarding Flow

The landing page collects minimum farm info before entering the app:

1. User clicks **Continue as Guest** → modal opens
2. Form fields: **Name** (required), **Email** (optional), **Location** (required), **Soil Type** (required), **Field Size in Acres** (required), **Primary Crop** (required)
3. On submit → `/api/auth/guest` creates session → `/api/profile/user` saves farm profile → redirect to `/app/home`
4. No "Skip" button — minimum info is required for meaningful advice

### Responsive Modal

- **Desktop**: 2-column grid form (520px max-width)
- **Mobile**: Single column, scrollable if needed (max-height: 90vh)

---

## Multilingual Support

The landing page supports 5 languages with real translations (not placeholders):

| Code | Language | Script |
|------|----------|--------|
| `en` | English | Latin |
| `hi` | Hindi | Devanagari |
| `mr` | Marathi | Devanavgar |
| `te` | Telugu | Telugu |
| `sw` | Swahili | Latin |

Language selection persists via `localStorage('aaa_preferred_language')` and is restored on page load.

---

## Files Changed

| File | Purpose |
|------|---------|
| `ui/device.js` (new) | Shared device detection utility |
| `ui/index.html` | Hamburger menu, nav drawer, device.js, viewport meta |
| `ui/landing.css` | Fluid typography, auto-fit grids, hamburger styles, touch optimizations |
| `ui/landing.js` | Hamburger menu logic, saved language restore |
| `ui/agui/index.html` | device.js include, CSS version bump |
| `ui/agui/styles.css` | Fluid chat pane, fluid spacing, touch optimizations, desktop fine-tuning |
| `ui/manifest.webmanifest` | Orientation: `any` (was `portrait-primary`) |

---

## Verification Results

### Landing Page

| Viewport | Device | Hamburger | Nav Links | Hero | Panel |
|----------|--------|-----------|-----------|------|-------|
| 1280px | desktop | hidden | visible | 2-column | overlay |
| 768px | tablet | visible | hidden | 1-column | inline |
| 375px | mobile | visible | hidden | 1-column | inline |

### Internal App

| Viewport | Device | Sidebar | Chat Pane | Bottom Nav | Chat Toggle |
|----------|--------|---------|-----------|------------|-------------|
| 1280px | desktop | visible (grid) | 409px (32vw) | hidden | hidden |
| 768px | tablet | drawer | 300px (min) | hidden | hidden |
| 375px | mobile | drawer | overlay (off-screen) | visible | visible (💬) |