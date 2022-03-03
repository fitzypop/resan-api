freeze:
	poetry export --format requirements.txt --output requirements

run:
	poetry run uvicorn app.main:app --reload
