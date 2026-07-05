---
name: Requirement Analysis
description: Formulate structured requirements (REQ-AAA-XXX) from feature request descriptions.
---

# Reusable Skill: Requirement Analysis

## Input Schema
```json
{
  "feature_request": "str"
}
```

## Output Schema
```json
{
  "requirement_id": "str",
  "acceptance_criteria": "list",
  "risk_level": "str",
  "traceability_link": "str"
}
```

## Success Criteria
- [ ] Correct REQ-AAA-XXX ID format
- [ ] Traceability link generated
- [ ] Acceptance criteria covers negative boundary paths

## Failure Conditions
- [ ] Vague requirements without acceptance criteria
- [ ] Scope drift without document revision

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
