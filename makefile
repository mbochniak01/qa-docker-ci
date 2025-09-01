# Makefile for QA Docker CI

# Docker image name
IMAGE_NAME := qa-test

# Default target: build and run tests locally
.PHONY: all
all: build test

# Build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Run tests in Docker with Allure results (parallel safe)
.PHONY: test
test:
	@echo "Ensuring base folder tmp/allure-results exists..."
	python -c "import os; os.makedirs('tmp/allure-results', exist_ok=True)"

	@echo "Running Docker tests..."
	docker run --rm -v "$(PWD)/tmp/allure-results:/usr/src/app/allure-results" $(IMAGE_NAME) || exit 0

	@echo "Merging worker shards into tmp/allure-merged..."
	python -c "import os, shutil, glob; os.makedirs('tmp/allure-merged', exist_ok=True); [shutil.copytree(f, 'tmp/allure-merged', dirs_exist_ok=True) for f in glob.glob('tmp/allure-results/*') if os.path.isdir(f)]"

# Open Allure report locally (requires Allure CLI installed)
.PHONY: report
report:
	allure open tmp/allure-merged

# Clean temporary files and Docker image
.PHONY: clean
clean:
	@echo "Cleaning tmp folders..."
	python -c "import shutil; shutil.rmtree('tmp/allure-results', ignore_errors=True); shutil.rmtree('tmp/allure-merged', ignore_errors=True)"
	docker rmi -f $(IMAGE_NAME) || exit 0

# Trigger GitHub Actions workflow
.PHONY: ci
ci:
	@echo "Triggering GitHub Actions workflow..."
	gh workflow run ci.yml --ref main
