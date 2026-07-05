# Agent Skills Operating Model

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** DevSecOps

---

## Skills Overview

The AI-SDLC framework includes 29 reusable, schema-validated skills in `.ai-sdlc/skills/`. Each skill is a declarative specification with input/output schemas, success criteria, and failure conditions.

## Skill Registry

### Requirements & Architecture

| Skill | ID | Purpose |
|-------|-----|---------|
| Requirement Analysis | SKILL-LOC-01 | Convert requests into ID-tracked requirements |
| Architecture Impact Analysis | SKILL-CODE-01 | Evaluate architectural changes |
| ADR Generation | — | Create Architecture Decision Records |
| Codebase Understanding | SKILL-CODE-01 | Inspect existing code before editing |

### Code Quality & Review

| Skill | ID | Purpose |
|-------|-----|---------|
| Code Review | — | Peer code review checks |
| Static Analysis | — | SAST scanning |
| API Contract Validation | — | Validate API contracts |

### Testing

| Skill | ID | Purpose |
|-------|-----|---------|
| Test Generation | — | Create unit/integration/E2E tests |
| Test Execution | — | Run pytest and collect coverage |

### Security

| Skill | ID | Purpose |
|-------|-----|---------|
| Threat Modeling | SKILL-SEC-01 | STRIDE threat models |
| Secret Scanning | — | Detect API keys and credentials |
| Dependency Vulnerability Review | — | pip-audit / npm audit |

### Domain Safety

| Skill | ID | Purpose |
|-------|-----|---------|
| Agricultural Safety Review | SKILL-SAFE-01 | Verify prescriptions through Safety Kernel |

### Localization & Accessibility

| Skill | ID | Purpose |
|-------|-----|---------|
| Localization Validation | SKILL-LOC-01 | Translation completeness |
| Mixed Script Detection | — | Script purity (no Devanagari in Telugu) |
| Farmer-Mode Language Review | — | No technical terms in farmer mode |
| Accessibility Review | — | ARIA, touch targets, contrast |
| Responsive Layout Review | — | Mobile form factor compliance |

### PWA & Offline

| Skill | ID | Purpose |
|-------|-----|---------|
| Offline PWA Validation | — | Service worker, cache, offline fallback |
| IndexedDB Sync Validation | — | Sync queue, data persistence |

### Deployment & Release

| Skill | ID | Purpose |
|-------|-----|---------|
| Container Build Validation | — | Dockerfile linting |
| Infrastructure Validation | — | Terraform/IaC linting |
| Deployment Plan Generation | — | Deployment + rollback steps |
| Rollback Plan Generation | — | Rollback runbook |
| Release Readiness | — | Evidence aggregation, scorecard |
| Release Note Generation | — | Changelog / release notes |
| Evidence Pack Generation | — | Compile evidence package |
| Post-Release Review | — | Post-deployment retrospective |

## Skill Structure

Each skill is defined in `SKILL.md`:

```markdown
---
name: Agricultural Safety Review
description: Ensure recommendations are audited by the Safety Kernel
---

# Reusable Skill: Agricultural Safety Review

## Input Schema
{ "recommendations": "list" }

## Output Schema
{ "safety_status": "str", "kernel_passed": "bool" }

## Success Criteria
- [ ] Prescriptive actions verified against Safety registry
- [ ] Escalates low confidence advice to agronomist

## Failure Conditions
- [ ] Bypassed Safety Kernel checks
- [ ] Approved dosage outside registered limits
```

## Skill Execution

Skills are invoked within workflow stages. Each skill:
1. Reads required input parameters from the environment
2. Runs validation scripts using permitted tools
3. Records performance evidence to `.ai-sdlc/evidence/`

## Known Limitations

- Skills are declarative specifications, not runtime enforcement mechanisms
- Not all skills have corresponding CLI tools in `tools/ai_sdlc/`
- Some skills (post-release-review, api-contract-validation) lack CLI implementations
- Skills describe expected behavior but do not auto-execute

## Related Documents

- [AI-SDLC Operating Model](ai-sdlc-operating-model.md)
- [Lifecycle Mapping](lifecycle-mapping.md)
- [ADR-AAA-003: Agent-Skills-Based AI-SDLC](../02-architecture/adr/ADR-AAA-003-agent-skills-based-ai-sdlc.md)