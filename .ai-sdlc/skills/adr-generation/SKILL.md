---
name: ADR Generation
description: Generate an Architecture Decision Record (ADR-AAA-XXX) for new architectural patterns.
---

# Reusable Skill: ADR Generation

## Input Schema
```json
{
  "context": "str",
  "decision": "str"
}
```

## Output Schema
```json
{
  "adr_id": "str",
  "adr_content": "str"
}
```

## Success Criteria
- [ ] Conforms to ADR-AAA-XXX format
- [ ] Lists consequences and alternatives

## Failure Conditions
- [ ] Undocumented architectural side effects
- [ ] Decisions without context mapping

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
