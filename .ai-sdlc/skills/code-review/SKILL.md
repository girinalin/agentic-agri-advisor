---
name: Code Review
description: Audit pull requests against style guidelines and architectural constraints.
---

# Reusable Skill: Code Review

## Input Schema
```json
{
  "git_diff": "str"
}
```

## Output Schema
```json
{
  "comments": "list",
  "approvals": "bool"
}
```

## Success Criteria
- [ ] Captures ruff compliance issues
- [ ] Flags safety parameter modifications

## Failure Conditions
- [ ] Approved PR containing unhandled exceptions
- [ ] Missed hardcoded secrets

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
