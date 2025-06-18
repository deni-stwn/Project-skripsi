.PHONY: help build up down logs clean dev status

# Default target
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development commands
dev: ## Start development environment
	docker-compose up --build

dev-d: ## Start development environment in detached mode
	docker-compose up --build -d

dev-logs: ## Show development logs
	docker-compose logs -f

dev-down: ## Stop development environment
	docker-compose down

# Build commands
build: ## Build all images
	docker-compose build

build-no-cache: ## Build images without cache
	docker-compose build --no-cache

# Maintenance commands
up: ## Start services
	docker-compose up -d

down: ## Stop services
	docker-compose down

logs: ## Show logs
	docker-compose logs -f

status: ## Show container status
	docker-compose ps

restart: ## Restart all services
	docker-compose restart

restart-app: ## Restart only app service
	docker-compose restart codescan-app

# Utility commands
shell: ## Open shell in app container
	docker-compose exec codescan-app bash

clean: ## Clean up containers and volumes
	docker-compose down -v
	docker system prune -f

# Health check
health: ## Check health of services
	@echo "Checking service health..."
	@docker-compose ps
	@echo "\nTesting app endpoint..."
	@curl -f http://localhost:5000/health || echo "App health check failed"