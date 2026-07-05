---
name: Infrastructure Validation
description: Lint terraform or configuration maps for security settings.
---

# Reusable Skill: Infrastructure Validation

## Input Schema
```json
{
  "config_path": "str"
}
```

## Output Schema
```json
{
  "violations": "list"
}
```

## Success Criteria
- [ ] Validates CORS limits
- [ ] Ensures bucket access parameters require IAM controls

## Failure Conditions
- [ ] Allowed wildcard (*) origins
- [ ] Open bucket policies approved

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
