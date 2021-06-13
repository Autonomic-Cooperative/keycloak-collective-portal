.DEFAULT: run
.PHONY: run redis

run:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv && \
		.venv/bin/pip install -U pip setuptools wheel poetry && \
		.venv/bin/poetry install --dev; \
	fi
	.venv/bin/poetry run uvicorn keycloak_collective_portal.main:app --reload

redis:
	@docker run -p 6379:6379 --name redis -d redis:6-alpine
