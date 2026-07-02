---
name: Offline PWA Validation
description: Verify offline asset precaching and check online status listener.
---

# Reusable Skill: Offline PWA Validation

## Input Schema
```json
{
  "sw_code": "str"
}
```

## Output Schema
```json
{
  "is_pwa_compliant": "bool",
  "cache_assets": "list"
}
```

## Success Criteria
- [ ] Precaches index.html and local DB script files
- [ ] Catches network fetch failures cleanly

## Failure Conditions
- [ ] Uncaught fetch rejections in Service Worker
- [ ] Missing online event listener bindings

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
