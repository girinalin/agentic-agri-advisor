# Release Readiness

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Release / DevSecOps

---

## Current Status: NOT_READY

The release readiness report (`/.ai-sdlc/reports/release-readiness.md`) shows **NOT_READY** as of July 2, 2026 (commit `361502a`). Evidence needs regeneration against the current commit.

## Release Gates

| Gate | Required | Current Status | Evidence |
|------|----------|---------------|----------|
| Tests | Yes | ⚠️ FAIL (stale) | `.ai-sdlc/evidence/tests/tests.json` |
| Secret Scan | Yes | ⚠️ NOT_EXECUTED | `.ai-sdlc/evidence/security/secrets.json` |
| Dependency Scan | Yes | ⚠️ NOT_EXECUTED | `.ai-sdlc/evidence/security/dependencies.json` |
| SAST Scan | Yes | ⚠️ NOT_EXECUTED | `.ai-sdlc/evidence/security/sast.json` |
| Traceability | Yes | ⚠️ WARNING | `.ai-sdlc/reports/traceability-matrix.json` |
| Safety | Yes | ✅ PASS | `.ai-sdlc/evidence/safety/safety.json` |
| Evidence Integrity | Yes | ✅ PASS | Manifest hashes verified |
| Human Production Approval | Yes | ❌ FAIL (pending) | `.ai-sdlc/evidence/approvals/approvals.json` |
| Rollback Plan | Yes | ✅ PASS | `.ai-sdlc/workflows/release.yaml` |

## Release Readiness Decision Logic

```
IF any mandatory gate = FAIL → NOT_READY
IF any mandatory gate = NOT_EXECUTED → NOT_READY
IF human approval = pending → NOT_READY
IF all mandatory gates = PASS
   AND human approval = approved (for current commit)
   AND rollback plan exists
   AND evidence is current (matches commit SHA)
→ READY
```

Release readiness is **conservative**: missing tools, stale evidence, missing rollback plans, or missing production approvals produce **NOT_READY** rather than a fabricated PASS.

## How to Regenerate Evidence

```bash
# Run all gates
make ai-sdlc-check

# Or run individual gates
make coverage
make secret-scan
make dependency-scan
make sast
make validate-safety
make validate-translations
make validate-schemas

# Generate release readiness report
make release-check

# Verify evidence manifest
make evidence
```

## Human Approval Process

1. Run `make ai-sdlc-check` — verify all gates pass
2. Review `.ai-sdlc/reports/release-readiness.md` — confirm READY
3. Review `.ai-sdlc/reports/quality-scorecard.md` — confirm quality
4. Get commit SHA: `git rev-parse HEAD`
5. Edit `.ai-sdlc/evidence/approvals/approvals.json`:
```json
{
  "approvals": [
    {
      "approvalId": "APR-PRODUCTION-RELEASE",
      "approvalType": "release",
      "environment": "production",
      "approvedBy": "Authorized Human Name",
      "approvedAt": "2026-07-04T12:00:00+00:00",
      "commitSha": "<exact-commit-sha>",
      "status": "approved",
      "comments": "All gates pass. Ready for production."
    }
  ]
}
```

6. Commit the approval
7. Deploy: `agents-cli deploy`

## Known Blockers

1. **Tests FAIL** — Evidence from July 2, needs regeneration on current commit
2. **Security scanners NOT_EXECUTED** — gitleaks, pip-audit, bandit, trivy not installed locally
3. **Human approval PENDING** — No authorized human has approved the current commit
4. **Traceability gaps** — 3 ADRs were missing (now created in `docs/02-architecture/adr/`)

## Related Documents

- [AI-SDLC Operating Model](ai-sdlc-operating-model.md)
- [Security Controls](security-controls.md)
- [Threat Model](threat-model.md)
- [Traceability Matrix](../../.ai-sdlc/reports/traceability-matrix.md)