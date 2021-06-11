.DEFAULT: run
.PHONY: run

run:
	@uvicorn keycloak_collective_portal:app --reload
