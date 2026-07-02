## Description
Provide a detailed change summary and motivation behind this pull request.

## SDLC Context
- **Requirement ID(s)**: REQ-AAA-XXX
- **Architecture ADR**: ADR-AAA-XXX

## Impact Matrix
- **Farmer Experience Impact**: [Describe how it alters Farmer Mode screens / responses]
- **Offline / Storage Impact**: [IndexedDB data twins, Sw.js asset additions]
- **Localization / Language Impact**: [Did you add/modify keys in translations.js? Checked leaks?]
- **Security / Privacy Impact**: [Were new routes added? Local storage settings?]
- **Agricultural Safety Impact**: [Does advice route through Safety Kernel?]

## Gates Verification
- [ ] Static ruff / ty validation checks pass (`make lint`, `make typecheck`)
- [ ] Schema and localization checks pass (`make ai-sdlc-check`)
- [ ] Regression and unit tests run successfully (`make test`)
- [ ] Signed evidence package compiled (`make evidence`)

## Rollback Plan
Describe the rollback commands or migration scripts if this change fails in staging/production.
