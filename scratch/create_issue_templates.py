import os

os.makedirs('.github/ISSUE_TEMPLATE', exist_ok=True)

def write_template(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created template: {filepath}")

# 1. pull_request_template.md
write_template(".github/pull_request_template.md", """## Description
Provide a detailed change summary and motivation behind this pull request.

## SDLC Context
- **Requirement ID(s)**: REQ-AAA-XXX
- **Architecture ADR**: ADR-AAA-XXX

## Impact Matrix
- **Farmer Experience Impact**: [Describe how it alters Farmer Mode screens / responses]
- **Offline / Storage Impact**: [IndexedDB data twins, Sw.js asset additions]
- **Localization / Language Impact**: [Did you add/modify keys in translations.js? Checked leaks?]
- **Security / Privacy Impact**: [Were new routes added? Local storage settings?]
- **Agricultural Safety Impact**: [Does advice route through Safety Kernel?]

## Gates Verification
- [ ] Static ruff / ty validation checks pass (`make lint`, `make typecheck`)
- [ ] Schema and localization checks pass (`make ai-sdlc-check`)
- [ ] Regression and unit tests run successfully (`make test`)
- [ ] Signed evidence package compiled (`make evidence`)

## Rollback Plan
Describe the rollback commands or migration scripts if this change fails in staging/production.
""")

# 2. bug_report.md
write_template(".github/ISSUE_TEMPLATE/bug_report.md", """---
name: Bug Report
about: Create a report to help us improve.
title: "[BUG] "
labels: bug
---

## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. See error '...'

## Expected Behavior
What should happen under standard conditions.

## Environment Details
- Viewport size: [Chromebook / Tablet / Mobile]
- Offline Mode: [Yes / No]
- Language selected: [hi / mr / te / sw / en]
""")

# 3. feature_request.md
write_template(".github/ISSUE_TEMPLATE/feature_request.md", """---
name: Feature Request
about: Propose a feature request for this project.
title: "[FEATURE] "
labels: enhancement
---

## Feature Description
Describe the feature request clearly.

## Farmer Usability Context
How does this feature assist village smallholders?

## Affected Components
- [ ] Frontend PWA
- [ ] A2UI schemas
- [ ] ADK cloud agents
- [ ] Offline storage / IndexedDB
""")

# 4. security_finding.md
write_template(".github/ISSUE_TEMPLATE/security_finding.md", """---
name: Security Finding
about: Report a detected vulnerability, secret leak, or security bug.
title: "[SEC] "
labels: security
---

## Vulnerability Details
Describe the vulnerability, secret exposure, or input injection vector.

## Risk Assessment
- Severity: [Low / Medium / High / Critical]
- Affected Package / Endpoint:

## Remediation Steps
Describe recommended patch implementations or dependency updates.
""")

# 5. safety_concern.md
write_template(".github/ISSUE_TEMPLATE/safety_concern.md", """---
name: Agricultural Safety Concern
about: Report a prescriptive advice issue, safety kernel bypass, or incorrect agronomic dosage.
title: "[SAFE] "
labels: safety-kernel
---

## Safety Breach Description
Describe the prescriptive action (e.g. chemical/fertilizer dosage) that bypassed safety audits or returned dangerous values.

## Affected Advisor Agent
- [ ] Pathologist
- [ ] Irrigation Advisor
- [ ] NPK Expert
- [ ] Coordinator

## Recommendations
Describe correction requirements in the Agricultural Safety Kernel.
""")

# 6. model_eval.md
write_template(".github/ISSUE_TEMPLATE/model_eval.md", """---
name: Model Evaluation Issue
about: Report failures in Gemma local LLM or TFLite pathology models.
title: "[EVAL] "
labels: model-evaluation
---

## Model Issue Details
Describe model response discrepancies, accuracy drops, WebGPU crashes, or classification failures.

## Test Context
- Model: [Gemma-2B / TFLite plant disease classifier]
- Input context (Image URL / Text prompt):
""")

# 7. localization_defect.md
write_template(".github/ISSUE_TEMPLATE/localization_defect.md", """---
name: Localization Defect
about: Report raw keys, mixed scripts, or language translation mistakes.
title: "[LOC] "
labels: localization
---

## Localization Bug Details
- Offending String:
- Screen / Schema:
- Expected Translation:

## Script Separation Audit
- [ ] Accidental Telugu characters in Hindi mode
- [ ] Accidental Devanagari in Telugu mode
- [ ] User-entered farmer name translated
""")
