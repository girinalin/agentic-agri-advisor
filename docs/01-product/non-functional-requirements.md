# Non-Functional Requirements

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Architecture / Engineering

---

## Performance

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-P01 | App initial load (cold) < 3 seconds on 3G | Browser DevTools network tab |
| NFR-P02 | Service worker cache load (warm) < 500ms | Browser DevTools |
| NFR-P03 | Agent response (online) < 5 seconds for simple queries | Eval suite timing |
| NFR-P04 | Agent response (online) < 15 seconds for complex multi-agent queries | Eval suite timing |
| NFR-P05 | Local rule-based response (offline) < 1 second | Manual testing |
| NFR-P06 | TFLite image classification < 3 seconds | Browser timing |
| NFR-P07 | TTS voice playback begins < 500ms after response | Browser audio timing |
| NFR-P08 | Language switching < 100ms (no page reload) | Browser testing |

## Reliability & Availability

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-R01 | App must function with zero connectivity | Airplane mode test |
| NFR-R02 | IndexedDB sync queue must not lose data on app restart | Offline → restart → online test |
| NFR-R03 | Service worker must serve cached fallback for API failures | Simulate API timeout |
| NFR-R04 | Safety kernel must never be bypassed, even under prompt injection | 19 adversarial tests |
| NFR-R05 | Escalation queue must persist across server restarts | In-memory currently; SQLite persistence planned |

## Scalability

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-S01 | Backend must handle 100 concurrent users on single Cloud Run instance | Load test |
| NFR-S02 | PWA must run on devices with 2GB RAM | Android budget device testing |
| NFR-S03 | OKF knowledge cache must be < 5MB for IndexedDB storage | Cache size measurement |
| NFR-S04 | TFLite model must be < 20MB for download | Model file size |

## Security

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-SEC01 | No secrets in client-side code | `make secret-scan` |
| NFR-SEC02 | Pre-commit hooks block API keys, private keys | `.pre-commit-config.yaml` |
| NFR-SEC03 | Semgrep rules detect safety kernel bypass and SQL injection | `semgrep --config .semgrep/rules.yaml` |
| NFR-SEC04 | Tool validation blocks dangerous operations (write_okf_concept, path traversal) | `.agents/scripts/validate_tool_call.py` |
| NFR-SEC05 | Agent hooks enforce 3 PreToolUse guards | `.agents/hooks.json` |
| NFR-SEC06 | Production release requires human approval for exact commit SHA | `.ai-sdlc/evidence/approvals/approvals.json` |

## Safety

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-SAF01 | All 5 banned chemicals must be blocked by safety kernel | `tests/unit/test_safety_kernel.py` |
| NFR-SAF02 | Dosage limits for 10 pesticides must be enforced | Safety kernel tests |
| NFR-SAF03 | PHI violations must be flagged with days remaining | Safety kernel tests |
| NFR-SAF04 | Low-confidence diagnoses must trigger escalation | Eval safety_critical cases |
| NFR-SAF05 | Safety kernel must run regardless of user claims or mode | Adversarial tests |

## Localization

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-L01 | All translation keys must be defined in all 5 languages | `make validate-translations` |
| NFR-L02 | Hindi mode contains zero Telugu script characters | `make validate-translations` |
| NFR-L03 | Telugu mode contains zero Devanagari characters | `make validate-translations` |
| NFR-L04 | Farmer names and locations remain untranslated | Manual testing |
| NFR-L05 | Voice STT must use correct BCP-47 code per language | `ui/agui/voice.js` voice map |

## Maintainability

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-M01 | Code must pass `make lint` (ruff) | Pre-commit hook |
| NFR-M02 | Code must pass `make typecheck` (ty) | Pre-commit hook |
| NFR-M03 | All tests must pass: `make test` | CI/CD pipeline |
| NFR-M04 | Evidence must be regenerated on every commit | GitHub Actions |
| NFR-M05 | Release readiness report must be conservative (NOT_READY if any gate fails) | `.ai-sdlc/reports/release-readiness.md` |

## Portability

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-PT01 | PWA must install on Android Chrome, Samsung Internet | Manual testing |
| NFR-PT02 | PWA must work on iOS Safari (with limitations) | Manual testing |
| NFR-PT03 | Backend must run in Docker container | `make build` |
| NFR-PT04 | Backend must deploy to Google Cloud Run | `agents-cli deploy` |

## Usability

| NFR | Requirement | Validation |
|-----|-------------|------------|
| NFR-U01 | Farmer Mode responses must be under 80 words | Eval suite |
| NFR-U02 | Farmer Mode must hide internal agent names | Eval suite |
| NFR-U03 | No markdown symbols in Farmer Mode responses | Eval suite |
| NFR-U04 | Touch targets must be ≥ 44×44 pixels | Accessibility review |
| NFR-U05 | Color contrast must meet WCAG AA standards | Accessibility review |

## Related Documents

- [Functional Requirements](functional-requirements.md)
- [Security Controls](../06-devsecops/security-controls.md)
- [Threat Model](../06-devsecops/threat-model.md)
- [Test Strategy](../05-testing/test-strategy.md)