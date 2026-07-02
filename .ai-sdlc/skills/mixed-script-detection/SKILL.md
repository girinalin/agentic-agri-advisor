---
name: Mixed Script Detection
description: Detect leaks of Devanagari in Telugu layout files and vice versa.
---

# Reusable Skill: Mixed Script Detection

## Input Schema
```json
{
  "text": "str"
}
```

## Output Schema
```json
{
  "has_mixed_script": "bool",
  "detected_blocks": "list"
}
```

## Success Criteria
- [ ] Correctly identifies Devanagari characters in Telugu block
- [ ] Highlights offending line details

## Failure Conditions
- [ ] False positives on standard place names
- [ ] Undetected leaks of scripts in dynamic outputs

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
