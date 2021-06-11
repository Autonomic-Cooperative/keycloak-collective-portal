.DEFAULT: run
.PHONY: run

run:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv && \
		.venv/bin/pip install -U pip setuptools wheel poetry && \
		.venv/bin/poetry install --dev; \
	fi
	.venv/bin/poetry run uvicorn keycloak_collective_portal:app --reload
