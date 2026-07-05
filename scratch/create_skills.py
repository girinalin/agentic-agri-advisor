import os
import json

skills_data = {
    "requirement-analysis": {
        "name": "Requirement Analysis",
        "description": "Formulate structured requirements (REQ-AAA-XXX) from feature request descriptions.",
        "input_schema": {"feature_request": "str"},
        "output_schema": {"requirement_id": "str", "acceptance_criteria": "list", "risk_level": "str", "traceability_link": "str"},
        "success_criteria": ["Correct REQ-AAA-XXX ID format", "Traceability link generated", "Acceptance criteria covers negative boundary paths"],
        "failure_conditions": ["Vague requirements without acceptance criteria", "Scope drift without document revision"]
    },
    "architecture-impact-analysis": {
        "name": "Architecture Impact Analysis",
        "description": "Assess the impact of requirements on database, APIs, UI layout, and offline storage.",
        "input_schema": {"requirement_id": "str"},
        "output_schema": {"affected_files": "list", "affected_schemas": "list", "offline_impact": "str"},
        "success_criteria": ["All schemas identified", "Offline storage impact assessed"],
        "failure_conditions": ["Omitted affected files", "Undefined database migration plans"]
    },
    "adr-generation": {
        "name": "ADR Generation",
        "description": "Generate an Architecture Decision Record (ADR-AAA-XXX) for new architectural patterns.",
        "input_schema": {"context": "str", "decision": "str"},
        "output_schema": {"adr_id": "str", "adr_content": "str"},
        "success_criteria": ["Conforms to ADR-AAA-XXX format", "Lists consequences and alternatives"],
        "failure_conditions": ["Undocumented architectural side effects", "Decisions without context mapping"]
    },
    "codebase-understanding": {
        "name": "Codebase Understanding",
        "description": "Analyze structure, dependencies, and layout of components.",
        "input_schema": {"target_dir": "str"},
        "output_schema": {"components": "list", "dependency_tree": "dict"},
        "success_criteria": ["Resolves component import targets correctly", "Identifies third party dependencies"],
        "failure_conditions": ["Stale module paths", "Missing configuration parameters in output"]
    },
    "code-review": {
        "name": "Code Review",
        "description": "Audit pull requests against style guidelines and architectural constraints.",
        "input_schema": {"git_diff": "str"},
        "output_schema": {"comments": "list", "approvals": "bool"},
        "success_criteria": ["Captures ruff compliance issues", "Flags safety parameter modifications"],
        "failure_conditions": ["Approved PR containing unhandled exceptions", "Missed hardcoded secrets"]
    },
    "test-generation": {
        "name": "Test Generation",
        "description": "Formulate new automated pytest unit and integration cases based on acceptance criteria.",
        "input_schema": {"acceptance_criteria": "list"},
        "output_schema": {"test_scripts": "list"},
        "success_criteria": ["Test scripts compiled in correct formats", "Mocks dependencies cleanly"],
        "failure_conditions": ["Syntactically invalid python scripts", "Tests that bypass core assertion logic"]
    },
    "test-execution": {
        "name": "Test Execution",
        "description": "Run pytest suite and gather test execution logs and code coverage.",
        "input_schema": {"test_path": "str"},
        "output_schema": {"total_tests": "int", "passed_tests": "int", "coverage_percentage": "float"},
        "success_criteria": ["Returns non-zero exit code on failure", "Coverage statistics logged"],
        "failure_conditions": ["Timeout during test run", "Failed process forks during execution"]
    },
    "a2ui-schema-validation": {
        "name": "A2UI Schema Validation",
        "description": "Validate A2UI canvas card JSON configurations against formatting schemas.",
        "input_schema": {"schema_path": "str"},
        "output_schema": {"is_valid": "bool", "errors": "list"},
        "success_criteria": ["Verifies supported component types", "Confirms no inline JS is present", "Requires accessibility labels on buttons"],
        "failure_conditions": ["Validates invalid JSON syntax", "Accepts script tags or unapproved action IDs"]
    },
    "localization-validation": {
        "name": "Localization Validation",
        "description": "Validate translations.js dictionaries and check for raw key leaks or script mix-ups.",
        "input_schema": {"translations_path": "str"},
        "output_schema": {"is_valid": "bool", "untranslated_keys": "list", "script_leaks": "list"},
        "success_criteria": ["All *Key fields checked across 5 languages", "Verifies zero Telugu script in Hindi dictionary", "Preserves user-entered location names"],
        "failure_conditions": ["Fails to detect untranslated key paths", "Accepts empty values for Telugu or Swahili"]
    },
    "mixed-script-detection": {
        "name": "Mixed Script Detection",
        "description": "Detect leaks of Devanagari in Telugu layout files and vice versa.",
        "input_schema": {"text": "str"},
        "output_schema": {"has_mixed_script": "bool", "detected_blocks": "list"},
        "success_criteria": ["Correctly identifies Devanagari characters in Telugu block", "Highlights offending line details"],
        "failure_conditions": ["False positives on standard place names", "Undetected leaks of scripts in dynamic outputs"]
    },
    "farmer-mode-language-review": {
        "name": "Farmer Mode Language Review",
        "description": "Audit advisor answers for farmer-friendly language, removing mixed languages and brackets.",
        "input_schema": {"assistant_response": "str"},
        "output_schema": {"is_compliant": "bool", "revisions": "str"},
        "success_criteria": ["Hides specialist/agent terms (pathologist, etc.)", "Removes English translation parentheticals", "Conforms response under 80 words"],
        "failure_conditions": ["Approved content with markdown tags (** or ###)", "Preserved technical system jargon in responses"]
    },
    "accessibility-review": {
        "name": "Accessibility Review",
        "description": "Verify ARIA labels, tap target dimensions, and tab indexes.",
        "input_schema": {"html_content": "str"},
        "output_schema": {"findings": "list"},
        "success_criteria": ["Flags buttons without keyboard focus states", "Tap targets larger than 48px verified"],
        "failure_conditions": ["Overlooks missing alt tags", "Accepted outline-none CSS styles"]
    },
    "responsive-layout-review": {
        "name": "Responsive Layout Review",
        "description": "Check layout scaling on tablet, mobile, and Chromebook widths.",
        "input_schema": {"css_and_html": "str"},
        "output_schema": {"is_responsive": "bool", "breakpoints": "list"},
        "success_criteria": ["Ensures navigation rail scaling works", "No clipped text elements detected"],
        "failure_conditions": ["Misses overlapping absolute positioned divs", "Layout breaks on 320px viewport"]
    },
    "offline-pwa-validation": {
        "name": "Offline PWA Validation",
        "description": "Verify offline asset precaching and check online status listener.",
        "input_schema": {"sw_code": "str"},
        "output_schema": {"is_pwa_compliant": "bool", "cache_assets": "list"},
        "success_criteria": ["Precaches index.html and local DB script files", "Catches network fetch failures cleanly"],
        "failure_conditions": ["Uncaught fetch rejections in Service Worker", "Missing online event listener bindings"]
    },
    "indexeddb-sync-validation": {
        "name": "IndexedDB Sync Validation",
        "description": "Validate sync queue DB integrity, retry mechanisms, and DLQ serialization.",
        "input_schema": {"local_db_js": "str"},
        "output_schema": {"is_sync_robust": "bool"},
        "success_criteria": ["Sync retries implement exponential backoff", "Failed payloads migrate to DLQ store"],
        "failure_conditions": ["Infinite retry loops on HTTP error", "Undocumented DLQ schema layout"]
    },
    "api-contract-validation": {
        "name": "API Contract Validation",
        "description": "Check FastAPI routes and query formats align with client calls.",
        "input_schema": {"routes_py": "str"},
        "output_schema": {"contract_mismatches": "list"},
        "success_criteria": ["Endpoints support CORS and proper headers", "Pydantic models match payload schemas"],
        "failure_conditions": ["Undocumented query filters", "Unchecked 500 server crashes on empty parameters"]
    },
    "agricultural-safety-review": {
        "name": "Agricultural Safety Review",
        "description": "Ensure recommendations, chemicals, and dosages are audited by the Safety Kernel.",
        "input_schema": {"recommendations": "list"},
        "output_schema": {"safety_status": "str", "kernel_passed": "bool"},
        "success_criteria": ["Prescriptive actions verified against Safety registry", "Escalates low confidence advice to agronomist"],
        "failure_conditions": ["Bypassed Safety Kernel checks", "Approved dosage recommendations outside registered limits"]
    },
    "threat-modeling": {
        "name": "Threat Modeling",
        "description": "Create STRIDE threat models and identify vulnerabilities in component flows.",
        "input_schema": {"architecture_map": "str"},
        "output_schema": {"threats": "list", "mitigations": "list"},
        "success_criteria": ["Correctly identifies elevation of privilege vulnerabilities", "Outlines clear mitigations"],
        "failure_conditions": ["Vague threat mappings", "No security boundary mapping"]
    },
    "dependency-vulnerability-review": {
        "name": "Dependency Vulnerability Review",
        "description": "Audit lockfile packages for known CVEs.",
        "input_schema": {"lockfile_path": "str"},
        "output_schema": {"vulnerabilities": "list"},
        "success_criteria": ["Scans all python dependency groups", "Flags critical severity CVEs"],
        "failure_conditions": ["Suppressed vulnerabilities without reasoning", "Incomplete package registry audits"]
    },
    "secret-scanning": {
        "name": "Secret Scanning",
        "description": "Scan codebase history for leaked developer credentials, keys, or credentials.",
        "input_schema": {"repo_history": "str"},
        "output_schema": {"leaks": "list"},
        "success_criteria": ["Scans .env and configurations", "Flags strings matching API patterns"],
        "failure_conditions": ["Missed credentials in documentation files", "Suppressed matching keys"]
    },
    "static-analysis": {
        "name": "Static Analysis",
        "description": "Analyze python files with ruff and JavaScript with eslint for code syntax.",
        "input_schema": {"source_files": "list"},
        "output_schema": {"violations": "list"},
        "success_criteria": ["Captures syntax errors and unused imports", "Returns non-zero exit status on rule breaches"],
        "failure_conditions": ["Suppressed checks without config override", "Syntax checks skipped on new modules"]
    },
    "container-build-validation": {
        "name": "Container Build Validation",
        "description": "Validate Dockerfile building and audit image configurations.",
        "input_schema": {"dockerfile_path": "str"},
        "output_schema": {"build_success": "bool", "vulnerabilities": "list"},
        "success_criteria": ["Docker image compiles successfully", "Multi-stage builds reduce image foot-print"],
        "failure_conditions": ["Leaked build arguments", "Run commands as root user in production"]
    },
    "infrastructure-validation": {
        "name": "Infrastructure Validation",
        "description": "Lint terraform or configuration maps for security settings.",
        "input_schema": {"config_path": "str"},
        "output_schema": {"violations": "list"},
        "success_criteria": ["Validates CORS limits", "Ensures bucket access parameters require IAM controls"],
        "failure_conditions": ["Allowed wildcard (*) origins", "Open bucket policies approved"]
    },
    "deployment-plan-generation": {
        "name": "Deployment Plan Generation",
        "description": "Generate step-by-step pipeline stages for deployment.",
        "input_schema": {"release_version": "str"},
        "output_schema": {"stages": "list", "commands": "list"},
        "success_criteria": ["Outlines configuration verification checks", "Details validation tests for staging"],
        "failure_conditions": ["Missing deployment validation steps", "Ambiguous directory targets"]
    },
    "rollback-plan-generation": {
        "name": "Rollback Plan Generation",
        "description": "Compile data and configuration rollback instructions.",
        "input_schema": {"deployment_plan": "str"},
        "output_schema": {"rollback_actions": "list"},
        "success_criteria": ["Provides clear database rollback migration SQLs", "Preserves offline local twin state on client rollbacks"],
        "failure_conditions": ["destructive rollback scripts", "No rollback validation criteria"]
    },
    "release-readiness": {
        "name": "Release Readiness",
        "description": "Compile scorecard of test results, security audits, and approvals.",
        "input_schema": {"version": "str"},
        "output_schema": {"is_ready": "bool", "scorecard": "dict"},
        "success_criteria": ["Aggregates evidence packages", "Decision reflects quality and security rules"],
        "failure_conditions": ["Certified release ready with failing gates", "No documented rollback script links"]
    },
    "release-note-generation": {
        "name": "Release Note Generation",
        "description": "Aggregate requirement IDs and git log commits into release notes.",
        "input_schema": {"git_diff": "str"},
        "output_schema": {"release_notes": "str"},
        "success_criteria": ["Requirements (REQ-AAA-XXX) mapped to commit lines", "Outlines known limitations"],
        "failure_conditions": ["Empty release notes", "Omitted requirement links"]
    },
    "evidence-pack-generation": {
        "name": "Evidence Pack Generation",
        "description": "Compile and sign verifiable artifact JSON packages.",
        "input_schema": {"release_version": "str"},
        "output_schema": {"evidence_paths": "list"},
        "success_criteria": ["Creates verifiable signed logs for tests, security, and safety", "Redacts sensitive user details"],
        "failure_conditions": ["Fabricated validation test results", "Leaked credentials inside evidence packs"]
    },
    "post-release-review": {
        "name": "Post Release Review",
        "description": "Conduct post-deployment reviews and document issues in incident logs.",
        "input_schema": {"release_summary": "str"},
        "output_schema": {"incident_logs": "list", "recommendations": "list"},
        "success_criteria": ["Identifies performance issues and latency stats", "Updates developer guidelines based on post-deployment findings"],
        "failure_conditions": ["Suppressed operational alerts", "No post-release report generated"]
    }
}

os.makedirs('.ai-sdlc/skills', exist_ok=True)
for dirname, data in skills_data.items():
    sdir = os.path.join('.ai-sdlc/skills', dirname)
    os.makedirs(sdir, exist_ok=True)

    skill_md = f"""---
name: {data['name']}
description: {data['description']}
---

# Reusable Skill: {data['name']}

## Input Schema
```json
{json.dumps(data['input_schema'], indent=2)}
```

## Output Schema
```json
{json.dumps(data['output_schema'], indent=2)}
```

## Success Criteria
{chr(10).join(f"- [ ] {item}" for item in data['success_criteria'])}

## Failure Conditions
{chr(10).join(f"- [ ] {item}" for item in data['failure_conditions'])}

## Execution Instructions
1. Invoke the skill within the active workflow stage.
2. Read the required input parameters from the environment.
3. Run validation scripts using permitted tools.
4. Record performance evidence to `.ai-sdlc/evidence/` directory.
"""

    fpath = os.path.join(sdir, 'SKILL.md')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(skill_md)
    print(f"Created skill: {fpath}")

print("All 29 skills successfully generated.")
