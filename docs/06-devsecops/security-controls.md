# Security Controls

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Security / DevSecOps

---

## Security Layers

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Pre-commit Hooks (7-8 checks)                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │ end-of-file-fixer │ trailing-whitespace          │  │
│  │ check-yaml/json/merge-conflict │ detect-private-key│ │
│  │ semgrep │ ruff                                    │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Semgrep Static Rules (6 rules)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │ API key detection │ Safety kernel bypass detection│  │
│  │ SQL injection │ Dangerous command execution       │  │
│  │ Path traversal │ Hardcoded secrets                │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Tool Validation & Agent Hooks                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │ validate_tool_call.py │ 3 PreToolUse guards       │  │
│  │ Blocks: write_okf_concept, path traversal,        │  │
│  │ dangerous commands                                  │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Layer 4: Safety Kernel (Agricultural Domain Safety)    │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Banned chemicals (5) │ Dosage limits (10)         │  │
│  │ PHI enforcement │ Escalation queue                 │  │
│  │ 19 adversarial tests                               │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Layer 5: Evidence & Release Gates                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Secret scan │ Dependency scan │ SAST │ Container  │  │
│  │ Human approval gate │ Release readiness report    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Pre-commit Hooks

**File:** `.pre-commit-config.yaml`

| Hook | Purpose | Status |
|------|---------|--------|
| end-of-file-fixer | Ensures files end with newline | ✅ |
| trailing-whitespace | Removes trailing whitespace | ✅ |
| check-yaml | Validates YAML syntax | ✅ |
| check-json | Validates JSON syntax | ✅ |
| check-merge-conflict | Detects merge conflict markers | ✅ |
| detect-private-key | Detects private keys | ✅ |
| semgrep | Runs 6 custom security rules | ✅ |
| ruff | Python linting and formatting | ✅ |

## Semgrep Rules

**File:** `.semgrep/rules.yaml`

| Rule ID | Purpose |
|---------|---------|
| `api-key-detection` | Detect hardcoded API keys (Gemini, OpenAI, AWS) |
| `safety-kernel-bypass` | Detect code that disables safety callbacks |
| `sql-injection` | Detect SQL string formatting without parameterization |
| `dangerous-command-execution` | Detect `os.system()`, `subprocess.call(shell=True)` with user input |
| `path-traversal` | Detect file path construction with user input |
| `hardcoded-secrets` | Detect hardcoded passwords and tokens |

## Tool Validation

**File:** `.agents/scripts/validate_tool_call.py`

Blocks the following tool calls:
- `write_okf_concept` — Prevents runtime modification of safety data
- Path traversal patterns (`../`, `~/.`)
- Dangerous shell commands (`rm -rf`, `sudo`, `chmod 777`)

## Agent Hooks

**File:** `.agents/hooks.json`

3 PreToolUse guards:
1. Validate tool name against allowed list
2. Check parameters for dangerous patterns
3. Block write operations to OKF/safety files

## Safety Kernel Security

See: [ADR-AAA-005](../02-architecture/adr/ADR-AAA-005-agricultural-safety-kernel.md) and [Threat Model](threat-model.md)

## Evidence Gates

| Gate | Command | Status (as of Jul 2) |
|------|---------|---------------------|
| Tests | `make coverage` | ⚠️ FAIL (stale evidence) |
| Secret scan | `make secret-scan` | ⚠️ NOT_EXECUTED (gitleaks not installed) |
| Dependency scan | `make dependency-scan` | ⚠️ NOT_EXECUTED (pip-audit not installed) |
| SAST | `make sast` | ⚠️ NOT_EXECUTED (bandit not installed) |
| Safety | `make validate-safety` | ✅ PASS |
| Container scan | `make container-scan` | ⚠️ NOT_EXECUTED (trivy not installed) |
| Human approval | Manual | ❌ Pending |

**Note:** Evidence needs regeneration against current commit. Run `make ai-sdlc-check`.

## Related Documents

- [Threat Model](threat-model.md)
- [AI-SDLC Operating Model](ai-sdlc-operating-model.md)
- [Release Readiness](release-readiness.md)
- [ADR-AAA-005: Safety Kernel](../02-architecture/adr/ADR-AAA-005-agricultural-safety-kernel.md)