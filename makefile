# Docker image name
IMAGE_NAME := qa-test

# Allure directories
ALLURE_RESULTS := tmp/allure-results
ALLURE_MERGED  := tmp/allure-merged

# Default target: build image and run tests
.PHONY: all
all: build test report

# Build Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Run tests inside Docker (parallel) and collect Allure results
.PHONY: test
test:
	@echo "Creating base results folder..."
	mkdir -p $(ALLURE_RESULTS)

	@echo "Running tests in Docker (parallel)..."
	docker run --rm \
		-v "$(PWD)/$(ALLURE_RESULTS):/usr/src/app/allure-results" \
		$(IMAGE_NAME) || true

	@echo "Merging Allure results..."
	mkdir -p $(ALLURE_MERGED)
	python3 - <<EOF
import os, shutil, glob
os.makedirs("$(ALLURE_MERGED)", exist_ok=True)
for f in glob.glob("$(ALLURE_RESULTS)/*"):
    if os.path.isdir(f):
        shutil.copytree(f, "$(ALLURE_MERGED)", dirs_exist_ok=True)
EOF

# Open Allure report locally (requires Allure CLI installed)
.PHONY: report
report:
	allure open $(ALLURE_MERGED)

# Clean temporary folders and Docker image
.PHONY: clean
clean:
	@echo "Cleaning tmp folders..."
	rm -rf $(ALLURE_RESULTS) $(ALLURE_MERGED)
	docker rmi -f $(IMAGE_NAME) || true
