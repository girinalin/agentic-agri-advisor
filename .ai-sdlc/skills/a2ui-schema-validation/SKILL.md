---
name: A2UI Schema Validation
description: Validate A2UI canvas card JSON configurations against formatting schemas.
---

# Reusable Skill: A2UI Schema Validation

## Input Schema
```json
{
  "schema_path": "str"
}
```

## Output Schema
```json
{
  "is_valid": "bool",
  "errors": "list"
}
```

## Success Criteria
- [ ] Verifies supported component types
- [ ] Confirms no inline JS is present
- [ ] Requires accessibility labels on buttons

## Failure Conditions
- [ ] Validates invalid JSON syntax
- [ ] Accepts script tags or unapproved action IDs

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
