# AI-SDLC Operating Model

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** DevSecOps / Architecture
> **Related ADR:** [ADR-AAA-003](../02-architecture/adr/ADR-AAA-003-agent-skills-based-ai-sdlc.md)

---

## Overview

Every feature begins with a spec and ends with evidence. The AI-SDLC framework enforces this through 10 lifecycle agents, 29 skills, 2 workflows, and command-backed evidence.

## Framework Structure

```
.ai-sdlc/
├── manifest.yaml          # Project parameters, agent/skill/tool registries
├── agents/                # 10 lifecycle agent personas (YAML)
├── skills/                # 29 reusable skill definitions (SKILL.md)
├── workflows/             # 2 pipelines (feature-delivery, pull-request-review)
├── evidence/              # Command-backed evidence (PASS/WARN/FAIL/NOT_EXECUTED)
│   ├── tests/             #   JUnit, coverage, test JSON
│   ├── safety/            #   Safety validation
│   ├── security/          #   SAST, secrets, dependencies, container
│   └── approvals/         #   Human production approval
└── reports/               # Quality scorecard, release readiness, traceability
```

## Lifecycle Agents (10)

| Agent | SDLC Phase | Evidence Produced |
|-------|-----------|-------------------|
| Requirements Agent | Requirements | `requirement-analysis-report.json` |
| Architecture Agent | Design | `architectural-impact-evidence.json` |
| Developer Agent | Implementation | `developer-selfcheck.json` |
| Test Agent | Testing | `test-run-evidence.json` |
| Security Agent | Security | `security-audit-evidence.json` |
| Safety Review Agent | Domain Safety | `agricultural-safety-evidence.json` |
| DevOps Agent | Deployment | `devops-build-evidence.json` |
| Release Agent | Release | `release-summary.json` |
| Documentation Agent | Documentation | `documentation-update-evidence.json` |
| UX/Accessibility Agent | UX Review | `ux-accessibility-evidence.json` |

Each agent YAML defines: purpose, responsibilities, permitted inputs, permitted tools, prohibited actions, expected outputs, evidence produced, escalation rules, human approval requirements, and failure behavior.

## Feature Delivery Workflow

```
Intake → Requirements → Risk Classification → Architecture Impact
    → [HUMAN GATE: Requirements Sign-off]
    → Implementation → Developer Self-Check
    → Test Generation → Test Execution
    → Security Audit → Safety Audit
    → Documentation Update
    → PR Review → Release Audit
    → [HUMAN GATE: Final Release Board]
```

## Pull Request Review Aspects (12)

1. Requirement alignment (changes link to requirement ID)
2. Architecture consistency (matches ADR principles)
3. Code quality (ruff formatting, type checks)
4. Test adequacy (≥80% statement coverage)
5. Security (no secrets, no vulnerable libraries)
6. Privacy (PII/consent compliance)
7. Localization (complete translation dictionaries)
8. Accessibility (ARIA controls, touch targets)
9. Offline behavior (PWA services run without network)
10. Agricultural safety (prescriptions go through Safety Kernel)
11. Documentation (runbooks and comments match changes)
12. Rollback impact (SQL migrations allow graceful rollback)

## CLI Tools

**Location:** `tools/ai_sdlc/`

```bash
make validate-schemas        # A2UI schema validation
make validate-translations   # 5-language translation completeness
make validate-safety         # Safety policy validation
make coverage                # pytest with evidence
make secret-scan             # Secret scanning
make dependency-scan         # pip-audit
make sast                    # bandit static analysis
make evidence                # Evidence manifest verification
make release-check           # Release readiness report
make ai-sdlc-check           # Run ALL gates
```

## Evidence Principles

1. **PASS requires command-backed evidence** — not self-certified
2. **Missing tools are NOT_EXECUTED** — not PASS
3. **Evidence is hashed and commit-linked** — SHA-256 + commit SHA
4. **Evidence is NOT cryptographically signed** — known limitation
5. **Release readiness is conservative** — NOT_READY if any mandatory gate is not PASS

## Human Approval Gates

| Gate | Who | When |
|------|-----|------|
| Requirements sign-off | Product Owner | After requirements + architecture impact |
| Production release | Release Board | After all evidence gates pass |

**File:** `.ai-sdlc/evidence/approvals/approvals.json`

## CI/CD Integration

**File:** `.github/workflows/ai-sdlc-gates.yml`

Runs on every PR to `main`:
- Requirements traceability verification
- Evidence manifest verification
- Quality scorecard generation
- Report archiving

## Related Documents

- [Agent Skills Operating Model](agent-skills-operating-model.md)
- [Lifecycle Mapping](lifecycle-mapping.md)
- [ADR-AAA-003: Agent-Skills-Based AI-SDLC](../02-architecture/adr/ADR-AAA-003-agent-skills-based-ai-sdlc.md)
- [Release Readiness](release-readiness.md)