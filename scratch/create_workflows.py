import os
import yaml

workflows = {
    "feature-delivery.yaml": {
        "name": "Feature Delivery Workflow",
        "description": "Standard multi-agent pipeline for feature request intake, implementation, and human approval.",
        "stages": [
            {
                "id": "intake",
                "name": "Feature Intake",
                "actor": "Product Agent",
                "description": "Gather raw request and initial scope details."
            },
            {
                "id": "requirement-analysis",
                "name": "Requirements Formulation",
                "actor": "Product Agent",
                "description": "Output REQ document and acceptance criteria."
            },
            {
                "id": "risk-classification",
                "name": "Risk Assessment",
                "actor": "Product Agent",
                "description": "Classify requirement risks (Low/Medium/High)."
            },
            {
                "id": "architecture-impact",
                "name": "Architectural Evaluation",
                "actor": "Architecture Agent",
                "description": "Assess schema/service impact, write ADR."
            },
            {
                "id": "human-approval-requirements",
                "name": "Human Gate: Requirements Sign-off",
                "actor": "Product Owner (Human)",
                "description": "Review and sign-off on requirements and architecture impact."
            },
            {
                "id": "implementation",
                "name": "Coding and Execution",
                "actor": "Developer Agent",
                "description": "Write source changes, document API, preserve compatibility."
            },
            {
                "id": "developer-selfcheck",
                "name": "Code Self-Check",
                "actor": "Developer Agent",
                "description": "Developer run basic local checks before PR."
            },
            {
                "id": "test-generation",
                "name": "Test Case Formulation",
                "actor": "Test Agent",
                "description": "Develop new unit/integration/E2E test scripts."
            },
            {
                "id": "test-execution",
                "name": "Test Execution",
                "actor": "Test Agent",
                "description": "Run pytest suite and collect coverage statistics."
            },
            {
                "id": "security-review",
                "name": "Security Audit",
                "actor": "Security Agent",
                "description": "Run SAST, dependency, secret, and privacy audits."
            },
            {
                "id": "safety-review",
                "name": "Agricultural Safety Audit",
                "actor": "Safety Agent",
                "description": "Verify prescriptions conform to Safety Kernel registry."
            },
            {
                "id": "documentation-update",
                "name": "Documentation Compilation",
                "actor": "Documentation Agent",
                "description": "Update READMEs, runbooks, and installation guidelines."
            },
            {
                "id": "pr-review",
                "name": "Code Review and Verification",
                "actor": "Developer Agent",
                "description": "Peer code review checks."
            },
            {
                "id": "release-readiness",
                "name": "Release Audit",
                "actor": "Release Agent",
                "description": "Assess evidence package, compile scorecard."
            },
            {
                "id": "human-release-approval",
                "name": "Human Gate: Final Release Board",
                "actor": "Release Board (Human)",
                "description": "Verify readiness report and sign off production deploy."
            }
        ]
    },
    "bug-fix.yaml": {
        "name": "Bug Fix Workflow",
        "description": "Incident response pipeline to reproduce, verify, and minimally hotfix bugs.",
        "stages": [
            {
                "id": "reproduce",
                "name": "Failure Reproduction",
                "actor": "Test Agent",
                "description": "Create failing regression test based on bug report."
            },
            {
                "id": "root-cause-analysis",
                "name": "Root Cause Diagnosis",
                "actor": "Developer Agent",
                "description": "Trace and isolate codebase logic error."
            },
            {
                "id": "regression-test",
                "name": "Hotfix Validation Plan",
                "actor": "Test Agent",
                "description": "Ensure regression test fails before coding fix."
            },
            {
                "id": "minimal-fix",
                "name": "Minimal Fix Coding",
                "actor": "Developer Agent",
                "description": "Write target code fix with minimal churn."
            },
            {
                "id": "test",
                "name": "Fix Verification Run",
                "actor": "Test Agent",
                "description": "Ensure regression test now passes, run full suite."
            },
            {
                "id": "security-review",
                "name": "Patch Security Audit",
                "actor": "Security Agent",
                "description": "Scan hotfix code changes for new vulnerabilities."
            },
            {
                "id": "documentation",
                "name": "Incident Log Update",
                "actor": "Documentation Agent",
                "description": "Document root cause and fix details in runbooks."
            },
            {
                "id": "pr-review",
                "name": "PR Merging Approval",
                "actor": "Developer Agent",
                "description": "Verify code changes and merge to main branch."
            }
        ]
    },
    "pull-request-review.yaml": {
        "name": "Pull Request Review Pipeline",
        "description": "Automated guidelines for checking code changes before merging.",
        "reviewAspects": [
            {
                "aspect": "requirement-alignment",
                "description": "Verify all changes link back to a valid requirement ID."
            },
            {
                "aspect": "architecture-consistency",
                "description": "Ensure modifications match existing ADR principles."
            },
            {
                "aspect": "code-quality",
                "description": "Enforce ruff formatting and type check completeness."
            },
            {
                "aspect": "test-adequacy",
                "description": "Verify statement coverage is at least 80%."
            },
            {
                "aspect": "security",
                "description": "Assert no secrets or vulnerable libraries are merged."
            },
            {
                "aspect": "privacy",
                "description": "Confirm location/PII tracking complies with consent preferences."
            },
            {
                "aspect": "localization",
                "description": "Scan translations.js for complete language dictionaries."
            },
            {
                "aspect": "accessibility",
                "description": "Ensure proper ARIA controls and touch targets."
            },
            {
                "aspect": "offline-behavior",
                "description": "Ensure Offline Gemma/PWA services run without network crashes."
            },
            {
                "aspect": "agricultural-safety",
                "description": "Assert that prescriptive outputs go through the Safety Kernel."
            },
            {
                "aspect": "documentation",
                "description": "Confirm runbooks and comments are matching changes."
            },
            {
                "aspect": "rollback-impact",
                "description": "Ensure SQL migrations and config allow graceful rollbacks."
            }
        ]
    },
    "release.yaml": {
        "name": "Release Workflow",
        "description": "Release assembly pipeline to package, verify, and authorize product deployment.",
        "stages": [
            {
                "id": "version-validation",
                "name": "Release Version Check",
                "actor": "Release Agent",
                "description": "Assert release tag meets semantic versioning."
            },
            {
                "id": "changelog",
                "name": "Release Changelog Compilation",
                "actor": "Release Agent",
                "description": "Compile git diff logs into public release notes."
            },
            {
                "id": "full-test-suite",
                "name": "Full Test Run",
                "actor": "Test Agent",
                "description": "Execute pytest suite (functional, offline, localization)."
            },
            {
                "id": "security-scans",
                "name": "Pre-Release SAST audit",
                "actor": "Security Agent",
                "description": "Run secret detection and codespell across all files."
            },
            {
                "id": "dependency-scan",
                "name": "Vulnerability Check",
                "actor": "Security Agent",
                "description": "Audit uv lockfile dependencies."
            },
            {
                "id": "container-build",
                "name": "Container Packaging",
                "actor": "DevOps Agent",
                "description": "Build deployment Docker image."
            },
            {
                "id": "smoke-test",
                "name": "E2E PWA Smoke Test",
                "actor": "DevOps Agent",
                "description": "Spin up container locally and verify core static endpoints."
            },
            {
                "id": "migration-review",
                "name": "Database Schema Audit",
                "actor": "Architecture Agent",
                "description": "Review SQL and IndexedDB upgrade scripts."
            },
            {
                "id": "configuration-validation",
                "name": "Env Config Check",
                "actor": "DevOps Agent",
                "description": "Check staging/production config files."
            },
            {
                "id": "release-evidence",
                "name": "Evidence Pack Assembly",
                "actor": "Release Agent",
                "description": "Assemble requirements, tests, security, safety, and build JSONs."
            },
            {
                "id": "rollback-plan",
                "name": "Rollback Execution Check",
                "actor": "DevOps Agent",
                "description": "Verify rollback runbooks allow safe recovery."
            },
            {
                "id": "human-release-gate",
                "name": "Human Gate: Production Board Approval",
                "actor": "Release Board (Human)",
                "description": "Final human review and deployment authorization."
            }
        ]
    }
}

os.makedirs('.ai-sdlc/workflows', exist_ok=True)
for filename, content in workflows.items():
    fpath = os.path.join('.ai-sdlc/workflows', filename)
    with open(fpath, 'w', encoding='utf-8') as f:
        yaml.safe_dump(content, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Created workflow: {fpath}")
