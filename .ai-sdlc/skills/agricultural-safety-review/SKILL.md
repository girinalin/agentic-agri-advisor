---
name: Agricultural Safety Review
description: Ensure recommendations, chemicals, and dosages are audited by the Safety Kernel.
---

# Reusable Skill: Agricultural Safety Review

## Input Schema
```json
{
  "recommendations": "list"
}
```

## Output Schema
```json
{
  "safety_status": "str",
  "kernel_passed": "bool"
}
```

## Success Criteria
- [ ] Prescriptive actions verified against Safety registry
- [ ] Escalates low confidence advice to agronomist

## Failure Conditions
- [ ] Bypassed Safety Kernel checks
- [ ] Approved dosage recommendations outside registered limits

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
