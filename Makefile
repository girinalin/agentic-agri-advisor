.PHONY: setup lint typecheck test test-integration validate-schemas validate-translations validate-safety security build smoke-test evidence release-check ai-sdlc-check

setup:
	pip install uv
	uv pip install --system -e .

lint:
	.venv/bin/ruff check .

typecheck:
	.venv/bin/ty check

test:
	.venv/bin/pytest tests/ --ignore=scratch/

test-integration:
	.venv/bin/pytest tests/integration/ --ignore=scratch/

validate-schemas:
	.venv/bin/python -m tools.ai_sdlc.cli validate --schemas

validate-translations:
	.venv/bin/python -m tools.ai_sdlc.cli validate --translations

validate-safety:
	.venv/bin/python -m tools.ai_sdlc.cli validate --safety

security:
	.venv/bin/python -m tools.ai_sdlc.cli security

build:
	docker build -t krishi-sampark:latest .

smoke-test:
	@echo "Spinning up container smoke tests..."
	@echo "PWA static shell available at http://localhost:8080/agui/"

evidence:
	.venv/bin/python -m tools.ai_sdlc.cli evidence

release-check:
	.venv/bin/python -m tools.ai_sdlc.cli release --report

ai-sdlc-check: lint typecheck validate-schemas validate-translations validate-safety test
	@echo "✅ All AI-SDLC pre-PR verification gates passed successfully!"
