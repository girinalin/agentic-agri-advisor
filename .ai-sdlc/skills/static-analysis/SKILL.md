---
name: Static Analysis
description: Analyze python files with ruff and JavaScript with eslint for code syntax.
---

# Reusable Skill: Static Analysis

## Input Schema
```json
{
  "source_files": "list"
}
```

## Output Schema
```json
{
  "violations": "list"
}
```

## Success Criteria
- [ ] Captures syntax errors and unused imports
- [ ] Returns non-zero exit status on rule breaches

## Failure Conditions
- [ ] Suppressed checks without config override
- [ ] Syntax checks skipped on new modules

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
