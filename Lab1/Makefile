help:
	@echo "Usage:"
	@echo "    make init          Install dependencies and set up hooks"
	@echo "    make check         Run pre-commit check on all files"
	@echo "    make hooks         Run pre-commit hooks on all files"

init:
	poetry install
	poetry run pre-commit install
	poetry run mypy --install-types
	cp .env.example .env

check:
	poetry run black .
	poetry run mypy .
	poetry run isort .
	poetry run flake8 .
	poetry run python -m unittest discover .

hooks:
	poetry run pre-commit run --all-files
