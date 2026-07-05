---
name: Release Readiness
description: Compile scorecard of test results, security audits, and approvals.
---

# Reusable Skill: Release Readiness

## Input Schema
```json
{
  "version": "str"
}
```

## Output Schema
```json
{
  "is_ready": "bool",
  "scorecard": "dict"
}
```

## Success Criteria
- [ ] Aggregates evidence packages
- [ ] Decision reflects quality and security rules

## Failure Conditions
- [ ] Certified release ready with failing gates
- [ ] No documented rollback script links

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
