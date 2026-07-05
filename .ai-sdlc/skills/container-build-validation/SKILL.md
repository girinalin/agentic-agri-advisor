---
name: Container Build Validation
description: Validate Dockerfile building and audit image configurations.
---

# Reusable Skill: Container Build Validation

## Input Schema
```json
{
  "dockerfile_path": "str"
}
```

## Output Schema
```json
{
  "build_success": "bool",
  "vulnerabilities": "list"
}
```

## Success Criteria
- [ ] Docker image compiles successfully
- [ ] Multi-stage builds reduce image foot-print

## Failure Conditions
- [ ] Leaked build arguments
- [ ] Run commands as root user in production

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
