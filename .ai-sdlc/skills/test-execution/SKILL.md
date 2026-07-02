---
name: Test Execution
description: Run pytest suite and gather test execution logs and code coverage.
---

# Reusable Skill: Test Execution

## Input Schema
```json
{
  "test_path": "str"
}
```

## Output Schema
```json
{
  "total_tests": "int",
  "passed_tests": "int",
  "coverage_percentage": "float"
}
```

## Success Criteria
- [ ] Returns non-zero exit code on failure
- [ ] Coverage statistics logged

## Failure Conditions
- [ ] Timeout during test run
- [ ] Failed process forks during execution

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
