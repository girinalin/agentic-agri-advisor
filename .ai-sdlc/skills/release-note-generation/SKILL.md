---
name: Release Note Generation
description: Aggregate requirement IDs and git log commits into release notes.
---

# Reusable Skill: Release Note Generation

## Input Schema
```json
{
  "git_diff": "str"
}
```

## Output Schema
```json
{
  "release_notes": "str"
}
```

## Success Criteria
- [ ] Requirements (REQ-AAA-XXX) mapped to commit lines
- [ ] Outlines known limitations

## Failure Conditions
- [ ] Empty release notes
- [ ] Omitted requirement links

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
