---
name: Rollback Plan Generation
description: Compile data and configuration rollback instructions.
---

# Reusable Skill: Rollback Plan Generation

## Input Schema
```json
{
  "deployment_plan": "str"
}
```

## Output Schema
```json
{
  "rollback_actions": "list"
}
```

## Success Criteria
- [ ] Provides clear database rollback migration SQLs
- [ ] Preserves offline local twin state on client rollbacks

## Failure Conditions
- [ ] destructive rollback scripts
- [ ] No rollback validation criteria

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
