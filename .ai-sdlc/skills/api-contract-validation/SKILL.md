---
name: API Contract Validation
description: Check FastAPI routes and query formats align with client calls.
---

# Reusable Skill: API Contract Validation

## Input Schema
```json
{
  "routes_py": "str"
}
```

## Output Schema
```json
{
  "contract_mismatches": "list"
}
```

## Success Criteria
- [ ] Endpoints support CORS and proper headers
- [ ] Pydantic models match payload schemas

## Failure Conditions
- [ ] Undocumented query filters
- [ ] Unchecked 500 server crashes on empty parameters

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
