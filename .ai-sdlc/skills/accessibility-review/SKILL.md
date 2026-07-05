---
name: Accessibility Review
description: Verify ARIA labels, tap target dimensions, and tab indexes.
---

# Reusable Skill: Accessibility Review

## Input Schema
```json
{
  "html_content": "str"
}
```

## Output Schema
```json
{
  "findings": "list"
}
```

## Success Criteria
- [ ] Flags buttons without keyboard focus states
- [ ] Tap targets larger than 48px verified

## Failure Conditions
- [ ] Overlooks missing alt tags
- [ ] Accepted outline-none CSS styles

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
