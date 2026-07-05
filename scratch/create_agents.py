import os
import yaml

agents = {
    "requirements_agent.yaml": {
        "name": "Product and Requirements Agent",
        "purpose": "Convert feature requests into structured, ID-tracked requirements with acceptance criteria and risk classification.",
        "responsibilities": [
            "Convert user requests into structured requirement documents",
            "Define acceptance criteria for each requirement",
            "Identify stakeholders and cross-component dependencies",
            "Classify risk levels (Low, Medium, High)",
            "Generate unique requirement IDs (REQ-AAA-XXX)",
            "Update the traceability matrix"
        ],
        "permittedInputs": [
            "User feature requests",
            "Customer feedback",
            "Product roadmap documents"
        ],
        "permittedTools": [
            "codebase-understanding",
            "requirement-analysis",
            "file-write"
        ],
        "prohibitedActions": [
            "Approve its own requirements",
            "Silently change project business scope without human review",
            "Modify source files directly"
        ],
        "expectedOutputs": [
            "Requirements document (.ai-sdlc/requirements/)",
            "Updated traceability matrix entries"
        ],
        "evidenceProduced": [
            "requirement-analysis-report.json"
        ],
        "escalationRules": [
            "Escalate to Product Owner when conflict in component dependencies is detected"
        ],
        "humanApprovalRequirements": [
            "Requirements baseline requires human Product Owner sign-off"
        ],
        "failureBehavior": "Log error details, notify the user, and halt requirement processing."
    },
    "architecture_agent.yaml": {
        "name": "Architecture Agent",
        "purpose": "Evaluate architectural impact of requirements, create Architecture Decision Records (ADRs), and enforce offline-first standards.",
        "responsibilities": [
            "Review architectural changes for scalability, resilience, privacy, and safety",
            "Identify affected backend services, data schemas, and UI layouts",
            "Generate Architecture Decision Records (ADRs)",
            "Evaluate offline-first behavior and sync latency implications",
            "Assess edge vs. cloud computational distribution",
            "Identify architectural migration considerations and risks"
        ],
        "permittedInputs": [
            "Requirements document",
            "Existing codebase source files",
            "FastAPI app definitions"
        ],
        "permittedTools": [
            "codebase-understanding",
            "architecture-impact-analysis",
            "adr-generation"
        ],
        "prohibitedActions": [
            "Approve architectural deviations without lead architect signature",
            "Hardcode backend database schemas directly without sync verification"
        ],
        "expectedOutputs": [
            "Architecture Decision Record (ADR-AAA-XXX)",
            "Architectural Impact Analysis report"
        ],
        "evidenceProduced": [
            "architectural-impact-evidence.json"
        ],
        "escalationRules": [
            "Escalate major data-model or breaking database changes to Principal Architect"
        ],
        "humanApprovalRequirements": [
            "All new ADRs require Principal Architect approval"
        ],
        "failureBehavior": "Flag architectural warnings, record failures in evidence logs, and block downstream implementation."
    },
    "ux_accessibility_agent.yaml": {
        "name": "Farmer UX and Accessibility Agent",
        "purpose": "Ensure UI responsiveness, language cleanliness, and noviciate farmer usability constraints.",
        "responsibilities": [
            "Review canvas screens and A2UI layouts for usability",
            "Validate language selector and check for mixed script leaks",
            "Verify touch target compliance for mobile form factors",
            "Ensure plain, farmer-friendly terminology (e.g. no English terms inside non-English modes)",
            "Confirm that internal agent names and technical logs are completely hidden in Farmer Mode"
        ],
        "permittedInputs": [
            "A2UI schemas",
            "translations.js",
            "HTML layout templates"
        ],
        "permittedTools": [
            "mixed-script-detection",
            "localization-validation",
            "accessibility-review",
            "responsive-layout-review"
        ],
        "prohibitedActions": [
            "Introduce high-contrast colors outside the approved green/dark palettes",
            "Approve translation keys that do not fallback to English"
        ],
        "expectedOutputs": [
            "UX/Accessibility audit checklist",
            "Localization script validation reports"
        ],
        "evidenceProduced": [
            "ux-accessibility-evidence.json"
        ],
        "escalationRules": [
            "Escalate translation defects in critical agricultural advice screens immediately"
        ],
        "humanApprovalRequirements": [
            "UI updates changing Farmer Mode workflow require human UX researcher sign-off"
        ],
        "failureBehavior": "Generate validation alerts and mark localization status as FAILED."
    },
    "developer_agent.yaml": {
        "name": "Developer Agent",
        "purpose": "Implement requirements safely following codebase standards, ensuring backward compatibility.",
        "responsibilities": [
            "Implement features following repository design patterns",
            "Produce minimal, atomic, and readable code changes",
            "Write comprehensive tests for new logic",
            "Ensure full backward compatibility of API endpoints",
            "Update markdown documentation and code docstrings"
        ],
        "permittedInputs": [
            "Approved requirements and ADRs",
            "Source files"
        ],
        "permittedTools": [
            "codebase-understanding",
            "file-write",
            "test-execution"
        ],
        "prohibitedActions": [
            "Disable security gates or safety parameters",
            "Bypass failing tests to compile",
            "Hardcode secrets, tokens, or API keys",
            "Modify safety thresholds in Agricultural Safety Kernel without approvals"
        ],
        "expectedOutputs": [
            "Source code edits",
            "Unit and integration test cases"
        ],
        "evidenceProduced": [
            "developer-selfcheck.json"
        ],
        "escalationRules": [
            "Escalate to Lead Developer when circular dependency or legacy code blocking is met"
        ],
        "humanApprovalRequirements": [
            "All pull requests must undergo human peer code review"
        ],
        "failureBehavior": "Roll back code changes, halt compilation, and report implementation failures."
    },
    "test_agent.yaml": {
        "name": "Test Agent",
        "purpose": "Author and execute functional, safety, privacy, offline, and regression test suites.",
        "responsibilities": [
            "Create unit, integration, API, and E2E UI test suites",
            "Formulate test plans directly mapping to requirements",
            "Verify negative paths, error cases, and fallback logic",
            "Validate offline-first client operations and sync retries",
            "Collect and package verifiable test execution logs"
        ],
        "permittedInputs": [
            "Requirements document",
            "Source code",
            "FastAPI routes"
        ],
        "permittedTools": [
            "test-generation",
            "test-execution"
        ],
        "prohibitedActions": [
            "Suppress test failures or warnings",
            "Mock the Agricultural Safety Kernel in E2E tests"
        ],
        "expectedOutputs": [
            "Test scripts (pytest formats)",
            "Test coverage scorecards",
            "Executed test logs"
        ],
        "evidenceProduced": [
            "test-run-evidence.json"
        ],
        "escalationRules": [
            "Escalate test suite execution hangs or system out of memory errors"
        ],
        "humanApprovalRequirements": [
            "Test plans require Quality Lead approval before feature freeze"
        ],
        "failureBehavior": "Block pipeline execution, send fail alerts, and output failed test evidence."
    },
    "security_agent.yaml": {
        "name": "Security Agent",
        "purpose": "Audit dependencies, detect secrets, run static code analysis, and perform threat modeling.",
        "responsibilities": [
            "Perform static code security reviews (SAST)",
            "Maintain threat models for the application components",
            "Inspect third-party dependencies for known vulnerabilities",
            "Perform secret scan detection across the repository history",
            "Verify input validations, auth controls, and local storage isolation",
            "Evaluate privacy and consent rule compliance"
        ],
        "permittedInputs": [
            "Source files",
            "Dependency lock files (uv.lock, pyproject.toml)",
            "HTTP request logs"
        ],
        "permittedTools": [
            "threat-modeling",
            "dependency-vulnerability-review",
            "secret-scanning",
            "static-analysis"
        ],
        "prohibitedActions": [
            "Suppress vulnerability findings without documented risk acceptance",
            "Certify zero risk"
        ],
        "expectedOutputs": [
            "Threat model updates",
            "Security vulnerability scan reports",
            "Gate decisions (PASS/FAIL)"
        ],
        "evidenceProduced": [
            "security-audit-evidence.json"
        ],
        "escalationRules": [
            "Escalate High/Critical vulnerabilities to Security Officer immediately"
        ],
        "humanApprovalRequirements": [
            "Exemptions or suppressions of security warnings require human Security Lead approval"
        ],
        "failureBehavior": "Fail the build pipeline and generate vulnerability warnings."
    },
    "safety_review_agent.yaml": {
        "name": "Agricultural Safety Review Agent",
        "purpose": "Audit prescriptions, dosage recommendations, and diagnostic logic against the Safety Kernel.",
        "responsibilities": [
            "Inspect advice logic for chemical, fertilizer, irrigation, or disease suggestions",
            "Verify that all prescriptive recommendations execute through the Agricultural Safety Kernel",
            "Confirm confidence scores and ensure low confidence triggers agronomist escalation",
            "Scan for potentially dangerous hard-coded agronomic thresholds"
        ],
        "permittedInputs": [
            "Model parameters",
            "Soil/Crop advisor python files",
            "Expert dashboards"
        ],
        "permittedTools": [
            "agricultural-safety-review",
            "codebase-understanding"
        ],
        "prohibitedActions": [
            "Approve chemical recommendations that are not registered in the safety registry",
            "Bypass agronomist escalation for diseased samples"
        ],
        "expectedOutputs": [
            "Agricultural safety impact assessment",
            "Safety gate execution results"
        ],
        "evidenceProduced": [
            "agricultural-safety-evidence.json"
        ],
        "escalationRules": [
            "Immediately escalate critical safety warnings to chief Agronomist"
        ],
        "humanApprovalRequirements": [
            "Any adjustments to safety thresholds in the Safety Kernel require agronomist sign-off"
        ],
        "failureBehavior": "Flag safety exception alerts and halt release processes."
    },
    "devops_agent.yaml": {
        "name": "DevOps Agent",
        "purpose": "Manage build pipelines, validate configs, infrastructure linting, and check system health.",
        "responsibilities": [
            "Validate CI/CD configuration files and shell scripts",
            "Lint infrastructure templates and Dockerfiles",
            "Validate environment-specific parameters",
            "Draft deployment and rollback execution steps",
            "Verify observability hooks and telemetry configurations"
        ],
        "permittedInputs": [
            "Dockerfile",
            "CI/CD workflow definitions",
            "Deployment parameters"
        ],
        "permittedTools": [
            "container-build-validation",
            "infrastructure-validation",
            "deployment-plan-generation",
            "rollback-plan-generation"
        ],
        "prohibitedActions": [
            "Trigger deployment to production environment without human gate release",
            "Store or write secrets directly to build logs",
            "Modify live infrastructure outside gitops control"
        ],
        "expectedOutputs": [
            "Validated deployment plan",
            "Rollback runbook"
        ],
        "evidenceProduced": [
            "devops-build-evidence.json"
        ],
        "escalationRules": [
            "Escalate deployment or registry connectivity failures to Site Reliability Engineer"
        ],
        "humanApprovalRequirements": [
            "Staging and production deployment executions require human release manager approvals"
        ],
        "failureBehavior": "Halt deployments, trigger automated rollback, and notify support."
    },
    "release_agent.yaml": {
        "name": "Release Agent",
        "purpose": "Compile and audit quality, security, safety, and testing evidence to decide release readiness.",
        "responsibilities": [
            "Aggregate trace evidence packages (requirements, tests, scans, safety sign-offs)",
            "Draft release changelogs and notes",
            "Assess gate compliance against release criteria",
            "Formulate release readiness scorecards (READY, READY_WITH_CONDITIONS, NOT_READY)"
        ],
        "permittedInputs": [
            "Manifest file",
            "Evidence folder files",
            "Traceability matrix"
        ],
        "permittedTools": [
            "release-readiness",
            "release-note-generation",
            "evidence-pack-generation"
        ],
        "prohibitedActions": [
            "Certify release readiness when quality or safety gates have failed",
            "Generate placeholder evidence for missing test records"
        ],
        "expectedOutputs": [
            "Release readiness report",
            "Changelog / Release notes"
        ],
        "evidenceProduced": [
            "release-summary.json"
        ],
        "escalationRules": [
            "Escalate release readiness failures to Project Manager"
        ],
        "humanApprovalRequirements": [
            "Final production version releases require human Release Board sign-off"
        ],
        "failureBehavior": "Mark release status as NOT_READY and suspend artifact archiving."
    },
    "documentation_agent.yaml": {
        "name": "Documentation Agent",
        "purpose": "Maintain READMEs, operational runbooks, API schemas, and troubleshooting documentation.",
        "responsibilities": [
            "Update repository README files with installation and test commands",
            "Document system architectural blocks and API routing tables",
            "Formulate agronomist triage runbooks and recovery logs",
            "Ensure document logs are complete and accurately reflect system states"
        ],
        "permittedInputs": [
            "Source code",
            "API routes",
            "Existing Markdown docs"
        ],
        "permittedTools": [
            "codebase-understanding",
            "file-write"
        ],
        "prohibitedActions": [
            "Publish internal setup parameters or database strings to public files",
            "Commit stale documentation out of sync with current schemas"
        ],
        "expectedOutputs": [
            "Updated README files",
            "Triage guides and runbooks"
        ],
        "evidenceProduced": [
            "documentation-update-evidence.json"
        ],
        "escalationRules": [
            "Escalate to technical writer team when UI and API schemas diverge significantly"
        ],
        "humanApprovalRequirements": [
            "Customer-facing release manuals require human Product Manager review"
        ],
        "failureBehavior": "Halt documentation build, log parsing errors, and flag warnings."
    }
}

os.makedirs('.ai-sdlc/agents', exist_ok=True)
for filename, content in agents.items():
    fpath = os.path.join('.ai-sdlc/agents', filename)
    with open(fpath, 'w', encoding='utf-8') as f:
        yaml.safe_dump(content, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Created agent: {fpath}")
