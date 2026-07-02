---
name: Codebase Understanding
description: Analyze structure, dependencies, and layout of components.
---

# Reusable Skill: Codebase Understanding

## Input Schema
```json
{
  "target_dir": "str"
}
```

## Output Schema
```json
{
  "components": "list",
  "dependency_tree": "dict"
}
```

## Success Criteria
- [ ] Resolves component import targets correctly
- [ ] Identifies third party dependencies

## Failure Conditions
- [ ] Stale module paths
- [ ] Missing configuration parameters in output

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
