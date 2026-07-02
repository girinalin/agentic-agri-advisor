---
name: Evidence Pack Generation
description: Compile and sign verifiable artifact JSON packages.
---

# Reusable Skill: Evidence Pack Generation

## Input Schema
```json
{
  "release_version": "str"
}
```

## Output Schema
```json
{
  "evidence_paths": "list"
}
```

## Success Criteria
- [ ] Creates verifiable signed logs for tests, security, and safety
- [ ] Redacts sensitive user details

## Failure Conditions
- [ ] Fabricated validation test results
- [ ] Leaked credentials inside evidence packs

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
