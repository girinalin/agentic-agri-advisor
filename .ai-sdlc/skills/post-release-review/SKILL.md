---
name: Post Release Review
description: Conduct post-deployment reviews and document issues in incident logs.
---

# Reusable Skill: Post Release Review

## Input Schema
```json
{
  "release_summary": "str"
}
```

## Output Schema
```json
{
  "incident_logs": "list",
  "recommendations": "list"
}
```

## Success Criteria
- [ ] Identifies performance issues and latency stats
- [ ] Updates developer guidelines based on post-deployment findings

## Failure Conditions
- [ ] Suppressed operational alerts
- [ ] No post-release report generated

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
