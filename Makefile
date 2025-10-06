# Python 2.7 C-API Extension Project Makefile

DOCKER_COMPOSE = docker compose

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo "Python 2.7 C-API Extension Project"
	@echo "=================================="
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Primary development targets
.PHONY: dev
dev: ## Build and test in Docker container
	$(DOCKER_COMPOSE) up pycapi-build

.PHONY: jupyter
jupyter: ## Start Jupyter notebook server
	$(DOCKER_COMPOSE) up jupyter

.PHONY: shell
shell: ## Interactive development shell
	$(DOCKER_COMPOSE) run --rm pycapi-dev

# Container management
.PHONY: up
up: ## Start services in background
	$(DOCKER_COMPOSE) up -d

.PHONY: down
down: ## Stop and remove containers
	$(DOCKER_COMPOSE) down

.PHONY: build
build: ## Build Docker images
	$(DOCKER_COMPOSE) build

.PHONY: logs
logs: ## Show container logs
	$(DOCKER_COMPOSE) logs -f

# Container-based operations
.PHONY: test
test: ## Run all test suites in container
	$(DOCKER_COMPOSE) run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python tests/run_all_tests.py"

.PHONY: test-basics
test-basics: ## Run basics_module tests
	$(DOCKER_COMPOSE) run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python tests/test_basics_module.py"

.PHONY: test-objects
test-objects: ## Run objects_module tests
	$(DOCKER_COMPOSE) run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python tests/test_objects_module.py"

.PHONY: test-memory
test-memory: ## Run memory_module tests
	$(DOCKER_COMPOSE) run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python tests/test_memory_module.py"

.PHONY: test-exceptions
test-exceptions: ## Run exceptions_module tests
	$(DOCKER_COMPOSE) run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python tests/test_exceptions_module.py"

.PHONY: test-advanced
test-advanced: ## Run advanced_module tests
	$(DOCKER_COMPOSE) run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python tests/test_advanced_module.py"

.PHONY: test-example
test-example: ## Run original example_module test
	$(DOCKER_COMPOSE) run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python examples/test_module.py"

.PHONY: debug
debug: ## Run diagnostic script in container
	$(DOCKER_COMPOSE) run --rm pycapi-dev python test_import.py

.PHONY: profile
profile: ## Run performance profiling in container
	$(DOCKER_COMPOSE) run --rm pycapi-dev python -c "import example_module; import time; start=time.time(); [example_module.add_numbers(i,i+1) for i in range(100000)]; print('Time: %.4f seconds' % (time.time()-start))"

# Maintenance
.PHONY: clean
clean: ## Clean build artifacts and Docker resources
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

.PHONY: rebuild
rebuild: clean build ## Full rebuild of Docker images

# Git and code quality
.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

.PHONY: setup-git
setup-git: ## Setup git repository with pre-commit hooks
	git init
	uv tool install pre-commit
	pre-commit install

# CI/CD and GitHub Actions
.PHONY: ci-test
ci-test: ## Run CI tests locally (mimics GitHub Actions)
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE) run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python examples/test_module.py"

.PHONY: security-scan
security-scan: ## Run security scan with Trivy
	docker build -t pycapi:security .
	docker run --rm -v $(PWD):/app aquasecurity/trivy fs /app

.PHONY: publish-dry-run
publish-dry-run: ## Test Docker image publishing (dry run)
	$(DOCKER_COMPOSE) build
	docker tag pycapi-python27 ghcr.io/$(USER)/pycapi:test
	@echo "Would push: ghcr.io/$(USER)/pycapi:test"
