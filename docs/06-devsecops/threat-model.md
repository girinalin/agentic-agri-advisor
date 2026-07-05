# Threat Model

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Security
> **Related ADR:** [ADR-AAA-005](../02-architecture/adr/ADR-AAA-005-agricultural-safety-kernel.md)

---

## System Boundaries and Data Flow

### Entry Points

| Entry Point | Description | Risk |
|-------------|-------------|------|
| Farmer Voice/Text Input | Voice (Web Speech API) or text via PWA chat | Prompt injection, multilingual adversarial input |
| Camera/Image Upload | Photo capture for crop disease diagnosis | Malicious images, EXIF metadata leakage |
| ADK Agent SSE Endpoint | `/run_sse` on port 8080 — agent chat | Unauthenticated access, DoS |
| FastAPI Endpoints | Profile, telemetry, OKF sync, TTS, safety, escalations | Unauthenticated API access |
| MCP Tool Calls | Weather, market, OKF, image analysis, TTS, STT | Tool abuse, injection via tool parameters |
| IndexedDB (PWA) | Offline farmer data, OKF cache, chat history | Data exfiltration via XSS, sync conflicts |

### Data Storage

| Store | Location | Sensitivity |
|-------|----------|-------------|
| Farmer Profile | SQLite (`farm_twin.db`) | PII (name, location, field data) |
| OKF Knowledge | Markdown files | Public (agricultural facts) |
| Chat History | IndexedDB (browser) | PII (farmer questions, responses) |
| API Keys | `.env` file | CRITICAL (Gemini, data.gov.in) |
| Escalation Queue | In-memory list | PII (farmer name, query, response) |
| Telemetry | SQLite + Cloud Logging | PII (farmer activity data) |

## STRIDE Evaluation

### Spoofing (S)

| Threat | Impact | Status | Mitigation |
|--------|--------|--------|------------|
| Farmer impersonation (`user_id` passed without auth) | HIGH | ❌ Open | Add session authentication |
| Expert mode spoofing | HIGH | ✅ Mitigated | Safety kernel runs regardless of user claims |
| MCP tool spoofing | MEDIUM | ⚠️ Partial | MCP servers are co-located (direct import) |

### Tampering (T)

| Threat | Impact | Status | Mitigation |
|--------|--------|--------|------------|
| Prompt injection via farmer query | CRITICAL | ✅ Mitigated | Eval tests confirm resistance; safety kernel blocks banned chemicals |
| OKF knowledge tampering via `write_okf_concept` | HIGH | ✅ Mitigated | Tool validation blocks `write_okf_concept` |
| Telemetry manipulation (unauthenticated POST) | MEDIUM | ❌ Open | Add authentication to telemetry endpoints |
| Safety kernel bypass | HIGH | ✅ Mitigated | Semgrep rule detects bypass in pre-commit |
| IndexedDB sync conflicts | LOW | ⚠️ Partial | Sync queue exists but no conflict resolution |

### Repudiation (R)

| Threat | Impact | Status | Mitigation |
|--------|--------|--------|------------|
| No audit trail for agent decisions | MEDIUM | ❌ Open | Add logging for all safety kernel decisions |
| Chat history deletions | LOW | ⚠️ Partial | IndexedDB stores history but can be cleared by user |

### Information Disclosure (I)

| Threat | Impact | Status | Mitigation |
|--------|--------|--------|------------|
| API key exposure in client code | CRITICAL | ✅ Mitigated | No secrets in client-side code; `make secret-scan` |
| EXIF metadata in uploaded photos | MEDIUM | ❌ Open | Strip EXIF before processing |
| Chat history XSS exfiltration | HIGH | ⚠️ Partial | No HTML rendering in chat (text only) |
| Error message information leakage | LOW | ✅ Mitigated | Generic error messages, no stack traces to client |

### Denial of Service (D)

| Threat | Impact | Status | Mitigation |
|--------|--------|--------|------------|
| ADK agent SSE endpoint DoS | MEDIUM | ❌ Open | Add rate limiting |
| Image upload size abuse | LOW | ⚠️ Partial | Browser limits, no server-side validation |
| MCP tool call flooding | MEDIUM | ❌ Open | Add rate limiting per session |

### Elevation of Privilege (E)

| Threat | Impact | Status | Mitigation |
|--------|--------|--------|------------|
| Safety kernel privilege escalation | HIGH | ✅ Mitigated | Safety kernel runs regardless of user claims; 19 adversarial tests |
| Agent instruction override | HIGH | ✅ Mitigated | Prompt injection tests confirm resistance |
| MCP tool abuse (path traversal, dangerous commands) | HIGH | ✅ Mitigated | `.agents/scripts/validate_tool_call.py` blocks dangerous operations |

## Mitigations Implemented

| Mitigation | Tool | File |
|------------|------|------|
| Pre-commit hooks (7-8) | pre-commit | `.pre-commit-config.yaml` |
| Semgrep rules (6) | semgrep | `.semgrep/rules.yaml` |
| Tool call validation | Python | `.agents/scripts/validate_tool_call.py` |
| Agent hooks (3 PreToolUse) | JSON | `.agents/hooks.json` |
| Safety kernel callbacks | Python | `safety_kernel/kernel.py` |
| Adversarial tests (19) | pytest | `tests/unit/test_safety_kernel.py` |
| Secret scanning | CLI | `make secret-scan` |
| SAST | bandit | `make sast` |

## Open Risks (Prioritized)

1. **HIGH: Farmer impersonation** — Add session authentication
2. **HIGH: No audit trail** — Log all safety kernel decisions
3. **MEDIUM: EXIF metadata** — Strip EXIF before processing
4. **MEDIUM: Rate limiting** — Add rate limits to SSE and API endpoints
5. **MEDIUM: Escalation queue persistence** — Move from in-memory to SQLite
6. **LOW: IndexedDB sync conflicts** — Implement conflict resolution strategy

## Related Documents

- [Security Controls](security-controls.md)
- [ADR-AAA-005: Safety Kernel](../02-architecture/adr/ADR-AAA-005-agricultural-safety-kernel.md)
- [Release Readiness](release-readiness.md)