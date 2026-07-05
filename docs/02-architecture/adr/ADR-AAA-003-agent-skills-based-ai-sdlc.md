# ADR-AAA-003: Agent-Skills-Based AI-SDLC

> **Status:** Accepted
> **Date:** 2026-07-04
> **Related Requirements:** REQ-AAA-004, REQ-AAA-012

---

## Context

The project needed a software development lifecycle framework that:
- Enforces evidence-driven quality gates (not self-certified PASS)
- Supports AI-assisted development with clear agent personas
- Aligns with Google ADK's development workflow (understand → scaffold → build → evaluate → deploy → observe)
- Enforces human approval gates for production releases
- Produces traceable evidence linking requirements to tests to releases

Approaches considered:
1. **GitHub Actions only** — CI/CD without declarative agent personas or skill definitions
2. **Custom Python CI** — Flexible but no standard agent/skill abstraction
3. **AI-SDLC with declarative agents + skills + workflows + evidence** — Structured, auditable, human-gated

## Decision

Adopt a **declarative AI-SDLC framework** with 4 layers:

### Layer 1: Lifecycle Agents (10 personas)

Each SDLC phase has a dedicated agent persona defined in YAML:

| Agent | Phase | File |
|-------|-------|------|
| Requirements Agent | Requirements | `.ai-sdlc/agents/requirements_agent.yaml` |
| Architecture Agent | Design | `.ai-sdlc/agents/architecture_agent.yaml` |
| Developer Agent | Implementation | `.ai-sdlc/agents/developer_agent.yaml` |
| Test Agent | Testing | `.ai-sdlc/agents/test_agent.yaml` |
| Security Agent | Security | `.ai-sdlc/agents/security_agent.yaml` |
| Safety Review Agent | Domain Safety | `.ai-sdlc/agents/safety_review_agent.yaml` |
| DevOps Agent | Deployment | `.ai-sdlc/agents/devops_agent.yaml` |
| Release Agent | Release | `.ai-sdlc/agents/release_agent.yaml` |
| Documentation Agent | Documentation | `.ai-sdlc/agents/documentation_agent.yaml` |
| UX/Accessibility Agent | UX Review | `.ai-sdlc/agents/ux_accessibility_agent.yaml` |

Each agent defines: purpose, responsibilities, permitted inputs, permitted tools, prohibited actions, expected outputs, evidence produced, escalation rules, human approval requirements, and failure behavior.

### Layer 2: Skills (29 reusable capabilities)

Schema-validated skill definitions in `.ai-sdlc/skills/`:
- `agricultural-safety-review`, `a2ui-schema-validation`, `localization-validation`
- `threat-modeling`, `secret-scanning`, `static-analysis`
- `offline-pwa-validation`, `indexeddb-sync-validation`
- `release-readiness`, `evidence-pack-generation`
- `code-review`, `test-execution`, `requirement-analysis`
- (and 16 more)

### Layer 3: Workflows (2 pipelines)

- **Feature Delivery** (`.ai-sdlc/workflows/feature-delivery.yaml`) — 15 stages from intake to release board
- **Pull Request Review** (`.ai-sdlc/workflows/pull-request-review.yaml`) — 12 review aspects

### Layer 4: Evidence & Reports

- Evidence stored in `.ai-sdlc/evidence/` with SHA-256 hashes and commit SHAs
- Reports generated in `.ai-sdlc/reports/`: quality scorecard, release readiness, traceability matrix
- Human approval required for production (`.ai-sdlc/evidence/approvals/approvals.json`)
- Release readiness is conservative: NOT_READY if any mandatory gate is not PASS

## Rationale

- **Evidence-driven:** Every PASS requires command-backed evidence; missing tools are NOT_EXECUTED, not PASS
- **Human gates:** Requirements sign-off and release board are human gates, not auto-approved
- **Declarative agents:** YAML personas describe responsibilities without being enforcement mechanisms themselves
- **CLI tools:** `tools/ai_sdlc/` Python scripts implement the validation gates
- **ADK alignment:** Maps to Google ADK lifecycle phases (understand → build → evaluate → deploy → observe)

## Consequences

**Positive:**
- Every release decision is traceable to evidence
- Security and safety gates are mandatory, not optional
- Agent personas provide clear responsibility boundaries
- Skills are reusable across features
- CI/CD integration via `make ai-sdlc-check`

**Negative:**
- 10 agent YAMLs + 29 skills + 2 workflows = significant declarative overhead
- Evidence is hashed but not cryptographically signed
- Declarative agents are specifications, not runtime enforcement
- External scanners (gitleaks, trivy, pip-audit) must be installed to produce PASS evidence

## Related Artifacts

- `.ai-sdlc/manifest.yaml` — Project parameters and registries
- `.ai-sdlc/agents/` — 10 lifecycle agent YAMLs
- `.ai-sdlc/skills/` — 29 skill definitions
- `.ai-sdlc/workflows/` — 2 workflow YAMLs
- `.ai-sdlc/evidence/` — Evidence artifacts
- `.ai-sdlc/reports/` — Quality scorecard, release readiness, traceability
- `tools/ai_sdlc/` — 13 Python CLI scripts
- `Makefile` — 15+ AI-SDLC targets
- `.github/workflows/ai-sdlc-gates.yml` — GitHub Actions CI/CD
- `AGENTS.md` — Root governance file

## Validation Approach

```bash
make ai-sdlc-check    # Run all gates: lint, typecheck, schemas, translations, safety, coverage, security, evidence
make release-check   # Generate release-readiness report
make evidence        # Verify evidence manifest integrity
```