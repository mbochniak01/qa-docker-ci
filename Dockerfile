# Base image: slim Python with minimal OS footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install only necessary system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jdk \
        unzip \
        bash \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest allure-pytest pytest-xdist

# Copy project code
COPY . .

# Create Allure results folder with proper permissions
RUN mkdir -p /usr/src/app/allure-results && chmod 777 /usr/src/app/allure-results

# Use ENTRYPOINT for flexibility in overriding commands
ENTRYPOINT ["pytest"]
CMD ["-v", "-n", "auto", "--dist=loadfile", "--alluredir=/usr/src/app/allure-results/$PYTEST_XDIST_WORKER"]
