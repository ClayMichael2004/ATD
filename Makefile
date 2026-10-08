.PHONY: help install install-dev run test clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install       Install production dependencies"
	@echo "  make install-dev   Install development and test dependencies"
	@echo "  make run           Run FastAPI development server with reload"
	@echo "  make test          Run pytest test suite"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-up     Start container via docker compose"
	@echo "  make docker-down   Stop docker compose containers"
	@echo "  make clean         Remove Python cache and temporary files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest -v tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete
	rm -rf .pytest_cache .coverage htmlcov

docker-build:
	docker build -t atd-api:latest .

docker-up:
	docker compose up -d

docker-down:
	docker compose down
