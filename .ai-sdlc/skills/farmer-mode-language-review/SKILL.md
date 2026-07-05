---
name: Farmer Mode Language Review
description: Audit advisor answers for farmer-friendly language, removing mixed languages and brackets.
---

# Reusable Skill: Farmer Mode Language Review

## Input Schema
```json
{
  "assistant_response": "str"
}
```

## Output Schema
```json
{
  "is_compliant": "bool",
  "revisions": "str"
}
```

## Success Criteria
- [ ] Hides specialist/agent terms (pathologist, etc.)
- [ ] Removes English translation parentheticals
- [ ] Conforms response under 80 words

## Failure Conditions
- [ ] Approved content with markdown tags (** or ###)
- [ ] Preserved technical system jargon in responses

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
