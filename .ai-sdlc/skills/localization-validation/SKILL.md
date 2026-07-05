---
name: Localization Validation
description: Validate translations.js dictionaries and check for raw key leaks or script mix-ups.
---

# Reusable Skill: Localization Validation

## Input Schema
```json
{
  "translations_path": "str"
}
```

## Output Schema
```json
{
  "is_valid": "bool",
  "untranslated_keys": "list",
  "script_leaks": "list"
}
```

## Success Criteria
- [ ] All *Key fields checked across 5 languages
- [ ] Verifies zero Telugu script in Hindi dictionary
- [ ] Preserves user-entered location names

## Failure Conditions
- [ ] Fails to detect untranslated key paths
- [ ] Accepts empty values for Telugu or Swahili

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
