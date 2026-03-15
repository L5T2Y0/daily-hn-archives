.PHONY: help install install-dev test lint format type-check clean run search weekly monthly

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run flake8 linter"
	@echo "  make format       - Format code with black"
	@echo "  make type-check   - Run mypy type checker"
	@echo "  make clean        - Remove cache and build files"
	@echo "  make run          - Run daily archive script"
	@echo "  make search       - Run search tool"
	@echo "  make weekly       - Generate weekly summary"
	@echo "  make monthly      - Generate monthly summary"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	flake8 *.py --max-line-length=120 --exclude=venv,__pycache__,.git

format:
	black *.py --line-length=120

type-check:
	mypy *.py --ignore-missing-imports

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true

run:
	python main.py

search:
	python search.py

weekly:
	python weekly_summary.py

monthly:
	python monthly_summary.py
