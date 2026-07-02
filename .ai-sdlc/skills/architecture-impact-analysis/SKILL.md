---
name: Architecture Impact Analysis
description: Assess the impact of requirements on database, APIs, UI layout, and offline storage.
---

# Reusable Skill: Architecture Impact Analysis

## Input Schema
```json
{
  "requirement_id": "str"
}
```

## Output Schema
```json
{
  "affected_files": "list",
  "affected_schemas": "list",
  "offline_impact": "str"
}
```

## Success Criteria
- [ ] All schemas identified
- [ ] Offline storage impact assessed

## Failure Conditions
- [ ] Omitted affected files
- [ ] Undefined database migration plans

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
