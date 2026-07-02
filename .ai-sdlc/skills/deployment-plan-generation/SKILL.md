---
name: Deployment Plan Generation
description: Generate step-by-step pipeline stages for deployment.
---

# Reusable Skill: Deployment Plan Generation

## Input Schema
```json
{
  "release_version": "str"
}
```

## Output Schema
```json
{
  "stages": "list",
  "commands": "list"
}
```

## Success Criteria
- [ ] Outlines configuration verification checks
- [ ] Details validation tests for staging

## Failure Conditions
- [ ] Missing deployment validation steps
- [ ] Ambiguous directory targets

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
