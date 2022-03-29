freeze:
	poetry export --format requirements.txt --output requirements

run:
	poetry run uvicorn api.main:app --reload

secret_key:
	openssl rand -hex 32
