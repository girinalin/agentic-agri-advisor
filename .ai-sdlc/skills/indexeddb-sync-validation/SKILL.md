---
name: IndexedDB Sync Validation
description: Validate sync queue DB integrity, retry mechanisms, and DLQ serialization.
---

# Reusable Skill: IndexedDB Sync Validation

## Input Schema
```json
{
  "local_db_js": "str"
}
```

## Output Schema
```json
{
  "is_sync_robust": "bool"
}
```

## Success Criteria
- [ ] Sync retries implement exponential backoff
- [ ] Failed payloads migrate to DLQ store

## Failure Conditions
- [ ] Infinite retry loops on HTTP error
- [ ] Undocumented DLQ schema layout

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
