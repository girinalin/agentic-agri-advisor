---
name: Secret Scanning
description: Scan codebase history for leaked developer credentials, keys, or credentials.
---

# Reusable Skill: Secret Scanning

## Input Schema
```json
{
  "repo_history": "str"
}
```

## Output Schema
```json
{
  "leaks": "list"
}
```

## Success Criteria
- [ ] Scans .env and configurations
- [ ] Flags strings matching API patterns

## Failure Conditions
- [ ] Missed credentials in documentation files
- [ ] Suppressed matching keys

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
