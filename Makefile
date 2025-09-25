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
test: ## Run tests in container
	$(DOCKER_COMPOSE) run --rm pycapi-dev python examples/test_module.py

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
