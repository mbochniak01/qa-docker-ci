# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        default-jdk \
        unzip \
        bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest allure-pytest pytest-xdist

# Copy project code
COPY . .

# Create base Allure results folder
RUN mkdir -p /usr/src/app/allure-results && chmod 777 /usr/src/app/allure-results

# Use ENTRYPOINT so additional args can be passed via docker run
ENTRYPOINT ["pytest"]
CMD ["-v", "-n", "auto", "--dist=loadfile", "--alluredir=/usr/src/app/allure-results/$PYTEST_XDIST_WORKER"]
