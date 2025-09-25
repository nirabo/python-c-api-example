# Python 2.7 C-API Extension Project Makefile

# Variables
PYTHON = python2.7
DOCKER_COMPOSE = docker compose
SERVICE_DEV = pycapi-dev
SERVICE_BUILD = pycapi-build
SERVICE_JUPYTER = jupyter
PROJECT_NAME = pycapi

# Default target
.DEFAULT_GOAL := help

# Help target
.PHONY: help
help: ## Show this help message
	@echo "Python 2.7 C-API Extension Project"
	@echo "=================================="
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development targets
.PHONY: build
build: ## Build the C extension module locally
	$(PYTHON) setup.py build_ext --inplace

.PHONY: clean
clean: ## Clean build artifacts
	$(PYTHON) setup.py clean --all
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "*.so" -delete
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

.PHONY: test
test: build ## Run the example test script
	$(PYTHON) examples/test_module.py

.PHONY: debug
debug: ## Run diagnostic import test
	$(PYTHON) test_import.py

# Docker targets
.PHONY: docker-build
docker-build: ## Build Docker image
	$(DOCKER_COMPOSE) build

.PHONY: docker-dev
docker-dev: ## Start interactive development container
	$(DOCKER_COMPOSE) run --rm $(SERVICE_DEV)

.PHONY: docker-shell
docker-shell: ## Get shell in running dev container
	$(DOCKER_COMPOSE) exec $(SERVICE_DEV) /bin/bash

.PHONY: docker-build-test
docker-build-test: ## Build and test C extension in Docker
	$(DOCKER_COMPOSE) up $(SERVICE_BUILD)

.PHONY: jupyter
jupyter: ## Start Jupyter notebook server
	$(DOCKER_COMPOSE) up $(SERVICE_JUPYTER)

.PHONY: jupyter-build
jupyter-build: ## Rebuild and start Jupyter notebook server
	$(DOCKER_COMPOSE) up --build $(SERVICE_JUPYTER)

.PHONY: jupyter-logs
jupyter-logs: ## Show Jupyter container logs
	$(DOCKER_COMPOSE) logs -f $(SERVICE_JUPYTER)

.PHONY: jupyter-stop
jupyter-stop: ## Stop Jupyter server
	$(DOCKER_COMPOSE) down

.PHONY: jupyter-restart
jupyter-restart: jupyter-stop jupyter ## Restart Jupyter server

# Container management
.PHONY: docker-up
docker-up: ## Start all services in background
	$(DOCKER_COMPOSE) up -d

.PHONY: docker-down
docker-down: ## Stop and remove all containers
	$(DOCKER_COMPOSE) down

.PHONY: docker-restart
docker-restart: docker-down docker-up ## Restart all services

.PHONY: docker-ps
docker-ps: ## Show running containers
	$(DOCKER_COMPOSE) ps

.PHONY: docker-logs
docker-logs: ## Show logs from all services
	$(DOCKER_COMPOSE) logs -f

# Maintenance targets
.PHONY: docker-clean
docker-clean: docker-down ## Clean Docker resources
	docker system prune -f
	docker volume prune -f

.PHONY: docker-rebuild
docker-rebuild: docker-clean docker-build ## Clean rebuild of Docker images

# Quick development workflow
.PHONY: dev
dev: build test ## Quick development cycle: build and test locally

.PHONY: dev-docker
dev-docker: docker-build-test ## Quick development cycle: build and test in Docker

# Installation targets (for local development)
.PHONY: install-deps-ubuntu
install-deps-ubuntu: ## Install development dependencies on Ubuntu
	sudo apt-get update
	sudo apt-get install -y python2.7 python2.7-dev python-pip build-essential gcc

.PHONY: install-deps-macos
install-deps-macos: ## Install development dependencies on macOS
	brew install python@2

# Project setup
.PHONY: setup
setup: ## Initial project setup
	@echo "Setting up Python 2.7 C-API development environment..."
	@echo "Run 'make install-deps-ubuntu' or 'make install-deps-macos' first"
	@echo "Then run 'make dev' to build and test locally"
	@echo "Or 'make jupyter' to start Jupyter notebook server"

# Advanced targets
.PHONY: profile
profile: build ## Run performance profiling
	$(PYTHON) -c "import example_module; import time; start=time.time(); [example_module.add_numbers(i,i+1) for i in range(100000)]; print('Time: %.4f seconds' % (time.time()-start))"

.PHONY: valgrind
valgrind: build ## Run with Valgrind (requires valgrind installation)
	valgrind --tool=memcheck --leak-check=full $(PYTHON) examples/test_module.py

.PHONY: gdb
gdb: build ## Debug with GDB
	gdb --args $(PYTHON) examples/test_module.py

# Notebook management
.PHONY: notebook-trust
notebook-trust: ## Trust Jupyter notebooks
	$(DOCKER_COMPOSE) exec $(SERVICE_JUPYTER) jupyter trust notebooks/*.ipynb

.PHONY: notebook-convert
notebook-convert: ## Convert notebooks to Python scripts
	$(DOCKER_COMPOSE) exec $(SERVICE_JUPYTER) jupyter nbconvert --to python notebooks/*.ipynb

# Git and pre-commit targets
.PHONY: git-init
git-init: ## Initialize git repository with pre-commit hooks
	git init
	uv tool install pre-commit
	pre-commit install
	pre-commit migrate-config

.PHONY: pre-commit-run
pre-commit-run: ## Run pre-commit hooks on all files
	pre-commit run --all-files

.PHONY: pre-commit-update
pre-commit-update: ## Update pre-commit hook versions
	pre-commit autoupdate

# Check targets
.PHONY: check-python
check-python: ## Check Python installation
	$(PYTHON) --version
	$(PYTHON) -c "import distutils.core; print('distutils available')"

.PHONY: check-docker
check-docker: ## Check Docker installation
	docker --version
	$(DOCKER_COMPOSE) version

.PHONY: check-deps
check-deps: check-python check-docker ## Check all dependencies
