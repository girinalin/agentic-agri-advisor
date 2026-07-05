# Test Strategy

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Engineering / QA

---

## Test Pyramid

```
                    ┌─────────┐
                    │   E2E   │  Browser-based manual testing
                  ┌─┴─────────┴─┐
                  │ Integration │  API + agent + database tests
                ┌─┴─────────────┴─┐
                │   Unit Tests    │  Safety kernel, db_manager, tools
              ┌─┴─────────────────┴─┐
              │  Evaluation Suite    │  29 cases × 4 metrics, LLM-as-judge
            ┌─┴───────────────────────┴─┐
            │   Adversarial Safety Tests │  19 prompt injection + bypass tests
          └──────────────────────────────┘
```

## Test Types

### 1. Unit Tests

**Location:** `tests/unit/`

| File | Tests | Purpose |
|------|-------|---------|
| `test_safety_kernel.py` | 19 | Adversarial safety tests (banned chemicals, overdose, PHI, prompt injection) |
| `test_ai_sdlc_hardening.py` | — | AI-SDLC framework validation |

**Run:**
```bash
uv run pytest tests/unit/ -v
```

### 2. Integration Tests

**Location:** `tests/integration/`

| File | Tests | Purpose |
|------|-------|---------|
| `test_server_e2e.py` | — | FastAPI endpoint integration |
| `test_localization.py` | — | Translation completeness and script purity |
| `test_phase4.py` | — | PWA offline functionality |

**Run:**
```bash
uv run pytest tests/integration/ -v
make test-integration
```

### 3. Evaluation Suite (Agent Quality)

**Location:** `tests/eval/`

- 29 eval cases across 10 categories
- 4 metrics: hallucination, safety compliance, tool-use quality, response quality
- LLM-as-judge grading using Gemini 2.5 Flash

**Run:**
```bash
set -a && source .env && set +a
uv run python tests/eval/run_local_eval.py --dataset tests/eval/datasets/agri-dataset.json --output-dir artifacts
```

See: [AI Evaluation Flywheel](ai-evaluation-flywheel.md)

### 4. Adversarial Safety Tests

**Location:** `tests/unit/test_safety_kernel.py`

19 tests covering:
- Banned chemical requests (endosulfan, monocrotophos)
- Dosage limit violations (10x overdose)
- Pre-harvest interval violations
- Prompt injection attacks ("ignore instructions")
- Safety kernel bypass attempts

### 5. Browser Testing (Manual)

**Tool:** VS Code integrated browser (Playwright-based)

| Test | Steps | Expected |
|------|-------|----------|
| Language switching | Change language dropdown | All UI text translates instantly |
| Voice STT | Tap mic, speak Hindi | Transcription appears in chat |
| Voice TTS | Send query, wait for response | Response read aloud in correct language |
| Camera | Open photo diagnosis, capture | Image captured and classified |
| Offline mode | Enable airplane mode, open app | App loads, OKF queries work |
| Soil test | Nav → मिट्टी जांच → manual entry → save | Summary with interpretations |
| Advisor selection | Nav → पूछें → select Sastri | Chat opens with Sastri persona |
| Escalation | Trigger low-confidence query | Escalation prompt with हाँ/नहीं |
| Market prices | Nav → मंडी भाव | Price table with 6 crops |

See: [Browser Testing Guide](browser-testing-guide.md)

## Test Coverage

**Run:**
```bash
make coverage  # pytest with JUnit + coverage evidence
```

Coverage evidence is stored in `.ai-sdlc/evidence/tests/coverage.json`.

## CI/CD Integration

**File:** `.github/workflows/ai-sdlc-gates.yml`

GitHub Actions runs on every PR to `main`:
- Requirements traceability verification
- Evidence manifest verification
- Quality scorecard generation
- Report archiving

## Related Documents

- [AI Evaluation Flywheel](ai-evaluation-flywheel.md)
- [Browser Testing Guide](browser-testing-guide.md)
- [Evaluation & Safety Report](evaluation-and-safety-report.md)
- [Release Readiness](../06-devsecops/release-readiness.md)