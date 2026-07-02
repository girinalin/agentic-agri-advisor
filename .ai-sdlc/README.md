# AI-Enabled Software Development Life Cycle (AI-SDLC)

This folder houses the metadata, guidelines, personas, skills, workflows, evidence logs, and scorecards governing the AI-assisted development of **Krishi Sampark**.

## Directory Layout

- `manifest.yaml`: Core project parameters, quality/security gates, and human approval boundaries.
- `agents/`: Declarative definitions of AI agent personas assisting the SDLC stages.
- `skills/`: Reusable, schema-validated execution directories for AI tasks.
- `workflows/`: YAML definitions of development loops (feature delivery, bug fixing, reviews).
- `evidence/`: Permanent logs of test runs, code scans, safety reviews, and release sign-offs.
- `reports/`: Generated quality scorecards and release-readiness reports.

## AI-SDLC Validation CLI

A unified Python CLI is available at the root to validate all development gates:

```bash
# Verify schemas, translations, and safety rules
python -m tools.ai_sdlc.cli validate --all

# Run all test suites and export evidence
python -m tools.ai_sdlc.cli test --evidence

# Generate a release-readiness report
python -m tools.ai_sdlc.cli release --version 1.0.0
```

Refer to `AGENTS.md` at the root for overall rules on how coding LLMs and assistants must operate within this repository.
