# ADR-AAA-002: Offline-First PWA with IndexedDB Sync

> **Status:** Accepted
> **Date:** 2026-07-04
> **Related Requirements:** REQ-AAA-002

---

## Context

Target farmers have intermittent 2G/3G connectivity. The app must:
- Load instantly with zero connectivity
- Cache knowledge for offline queries
- Queue activities for sync when connectivity returns
- Not lose data on app restart or browser crash

Approaches considered:
1. **React Native / native app** — Requires app store distribution, large binary, platform-specific
2. **WebView wrapper (Capacitor)** — Adds complexity, still needs web caching
3. **Pure PWA with IndexedDB** — Installable, offline-capable, zero installation friction

## Decision

Implement a **Progressive Web App** with:
- Service worker for static asset caching (cache-first strategy)
- IndexedDB with 11 object stores for structured offline data
- Network-first strategy for API data with offline fallback
- Sync queue pattern for bidirectional data flow

**Key files:**
- `ui/sw.js` — Service worker (cache-first for static, network-first for API)
- `ui/manifest.webmanifest` — PWA manifest (installable, standalone, brand icons)
- `ui/agui/local_db.js` — IndexedDB manager (11 stores)
- `ui/agui/dashboard.js` — Hybrid connectivity routing
- `ui/agui/pwa_config.js` — Configurable backend URLs, install prompt, background sync

### IndexedDB Stores

| Store | Sync Direction | Purpose |
|-------|---------------|---------|
| `farmer_profile` | Server → Client | Cached farmer profile |
| `chat_history` | Bidirectional | Offline chat messages |
| `telemetry_queue` | Client → Server | Pending telemetry updates |
| `okf_knowledge` | Server → Client | OKF entity cache |
| `farm_activities` | Bidirectional | Logged activities |
| `reminders` | Client → Server | Irrigation/treatment reminders |
| `escalations` | Bidirectional | Expert escalation queue |
| `feedback` | Client → Server | User feedback |
| `soil_reports` | Bidirectional | Cached soil reports |
| `market_cache` | Server → Client | Market price cache |
| `weather_cache` | Server → Client | Weather data cache |

## Rationale

- **Zero installation friction:** Farmers tap a link, get "Add to Home Screen" prompt, done
- **Service worker caching:** App shell loads in <500ms from cache even with zero connectivity
- **IndexedDB over localStorage:** Structured data, larger storage quota, transactional
- **Sync queue pattern:** Activities are queued locally and synced when online — no data loss
- **PWA over native:** No app store review, no binary distribution, updates are instant

## Consequences

**Positive:**
- App works fully offline for core functionality
- Installable on Android Chrome, Samsung Internet, iOS Safari (limited)
- No app store dependency or review process
- Updates deployed by changing server files

**Negative:**
- iOS Safari has limited PWA support (no background sync, limited IndexedDB)
- Service worker cache must be carefully versioned to avoid stale content (solved with `?v=N` cache-busting)
- IndexedDB storage limits vary by browser (typically 50MB+ on Android Chrome)
- No push notifications on iOS

## Related Artifacts

- `ui/sw.js` — Service worker
- `ui/manifest.webmanifest` — PWA manifest
- `ui/agui/local_db.js` — IndexedDB manager
- `ui/agui/pwa_config.js` — PWA configuration
- `ui/agui/dashboard.js` — Offline routing logic
- `.ai-sdlc/skills/offline-pwa-validation/SKILL.md`
- `.ai-sdlc/skills/indexeddb-sync-validation/SKILL.md`

## Validation Approach

```bash
# Manual: Enable airplane mode, open app, verify it loads and responds
# Manual: Log activity offline, reconnect, verify sync to server
# Manual: Check IndexedDB stores in browser DevTools > Application > IndexedDB
```