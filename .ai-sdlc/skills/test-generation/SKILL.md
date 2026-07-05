---
name: Test Generation
description: Formulate new automated pytest unit and integration cases based on acceptance criteria.
---

# Reusable Skill: Test Generation

## Input Schema
```json
{
  "acceptance_criteria": "list"
}
```

## Output Schema
```json
{
  "test_scripts": "list"
}
```

## Success Criteria
- [ ] Test scripts compiled in correct formats
- [ ] Mocks dependencies cleanly

## Failure Conditions
- [ ] Syntactically invalid python scripts
- [ ] Tests that bypass core assertion logic

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
