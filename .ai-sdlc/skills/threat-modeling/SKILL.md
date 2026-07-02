---
name: Threat Modeling
description: Create STRIDE threat models and identify vulnerabilities in component flows.
---

# Reusable Skill: Threat Modeling

## Input Schema
```json
{
  "architecture_map": "str"
}
```

## Output Schema
```json
{
  "threats": "list",
  "mitigations": "list"
}
```

## Success Criteria
- [ ] Correctly identifies elevation of privilege vulnerabilities
- [ ] Outlines clear mitigations

## Failure Conditions
- [ ] Vague threat mappings
- [ ] No security boundary mapping

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
