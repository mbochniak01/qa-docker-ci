# QA Test Automation Framework

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/pytest-tested-green)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Allure](https://img.shields.io/badge/allure-reports-red)](https://docs.qameta.io/allure/)

This repository contains a Python-based test automation framework using **pytest**, **Playwright**, and **Allure**. It also includes a **Docker setup** for containerized test execution.

---

## Table of Contents

1. [Setup Test Framework](#1-setup-test-framework)  
2. [Running Tests Locally with Allure](#2-running-tests-locally-with-allure)  
3. [Running Tests in Docker with Allure](#3-running-tests-in-docker-with-allure)  
4. [Dockerfile Overview](#4-running-tests-in-docker-with-allure)  

---

## 1. Setup Test Framework

### Prerequisites

- Python 3.11+
- Git 
- Allure CLI 
- Docker

### Install dependencies

1. Clone the repository:

```bash
git clone <repo_url>
cd <repo_folder>
```
Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
```
Activate the virtual environment:

Windows:

```powershell
.venv\Scripts\activate
```
Mac/Linux:

```bash
source .venv/bin/activate
```
Install Python dependencies:

```bash
pip install -r requirements.txt
# or manually
pip install pytest pytest-playwright allure-pytest assertpy
```
Install Playwright browsers:

```bash
playwright install
```
## 2. Running Tests Locally with Allure
Run all tests and generate Allure results:

```bash
pytest tests/ --alluredir=allure-results -v
tests/ → folder containing test files

--alluredir=allure-results → output folder for Allure JSON
```
Serve Allure report:

```bash
allure serve allure-results
```
Opens the interactive Allure report in your browser

Shows features, stories, steps, and test results

Run a single test:
```bash
pytest tests/test_math.py::test_addition
```
Verbose output with step logging:

```bash
pytest tests/ -v
```
## 3. Running Tests in Docker with Allure
The repository includes a Dockerfile for containerized test execution.

3.1 Build Docker Image

```bash
docker build -t my-python-tests .
my-python-tests → name of the Docker image
```
3.2 Create Allure Results Folder
On Windows PowerShell:

```powershell
mkdir allure-results
```
This folder will be mounted into the container so you can access the results locally.

3.3 Run Tests in Container
PowerShell:

```powershell

docker run --rm -it -v ${PWD}/allure-results:/usr/src/app/allure-results my-python-tests

--rm → remove container after execution

-it → interactive terminal to see live logs

${PWD}/allure-results → maps local folder to container
```
Alternative (full absolute path):

```powershell
docker run --rm -it -v C:\Users\Praca\qa-docker-ci\allure-results:/usr/src/app/allure-results my-python-tests
```
3.4 View Allure Report
After the container finishes:

```bash
allure serve allure-results
```
Opens interactive Allure report with test results from the Docker run


## 4. Dockerfile Overview

- Base image: Uses python:3.11-slim for a lightweight Python environment.

- Working directory: Sets ```/usr/src/app``` as the container working directory.

- System dependencies: Installs ```default-jdk``` (needed for Allure) and python3-pip.

- Python dependencies: Installs ```pytest``` and ```allure-pytest``` plugin via pip.

- Project code: Copies the entire repository into the container.

- Allure results folder: Creates ```/usr/src/app/allure-results``` and sets permissions so both local and CI runs can write results.

- Default command: Runs pytest with verbosity and outputs Allure JSON results to ```/usr/src/app/allure-results```.