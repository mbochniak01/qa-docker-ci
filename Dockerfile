# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        default-jdk \
        python3-pip \
        unzip \
        wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest allure-pytest pytest-xdist

# Copy static data and project code
COPY data/ ./data/
COPY . .

# Create base Allure results folder
RUN mkdir -p /usr/src/app/allure-results && chmod 777 /usr/src/app/allure-results

# Default command: run pytest in parallel, each worker writes to its own shard
CMD ["bash", "-c", "pytest -v -n auto --dist=loadfile --alluredir=/usr/src/app/allure-results/$PYTEST_XDIST_WORKER"]
