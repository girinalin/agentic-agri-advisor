---
name: Responsive Layout Review
description: Check layout scaling on tablet, mobile, and Chromebook widths.
---

# Reusable Skill: Responsive Layout Review

## Input Schema
```json
{
  "css_and_html": "str"
}
```

## Output Schema
```json
{
  "is_responsive": "bool",
  "breakpoints": "list"
}
```

## Success Criteria
- [ ] Ensures navigation rail scaling works
- [ ] No clipped text elements detected

## Failure Conditions
- [ ] Misses overlapping absolute positioned divs
- [ ] Layout breaks on 320px viewport

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
