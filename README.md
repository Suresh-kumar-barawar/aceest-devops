# ACEest DevOps Project

## Project Overview

This project demonstrates a complete DevOps pipeline for ACEest Fitness & Gym application using Flask, Docker, GitHub Actions, and Jenkins.

## Technologies Used

* Python (Flask)
* Git & GitHub
* Docker
* GitHub Actions
* Jenkins

## Application Features

* REST API built using Flask
* Multiple endpoints for gym management
* Unit tested using Pytest

## Local Setup Instructions

### 1. Clone the Repository

git clone https://github.com/Suresh-kumar-barawar/aceest-devops.git

### 2. Navigate to Project Folder

cd aceest-devops

### 3. Create Virtual Environment

python -m venv venv

### 4. Activate Virtual Environment

venv\Scripts\activate

### 5. Install Dependencies

pip install -r requirements.txt

### 6. Run Application

python app.py

Application will run on:
http://127.0.0.1:5000

---

## Running Tests

Run the following command:
pytest

All tests should pass successfully.

---

## Docker Setup

### Build Docker Image

docker build -t aceest-app .

### Run Docker Container

docker run -p 5000:5000 aceest-app

---

## CI/CD Pipeline (GitHub Actions)

This project uses GitHub Actions to automate the CI/CD pipeline.

### Pipeline Stages:

1. Lint Check
2. Docker Image Build
3. Run Pytest

The pipeline is triggered on every push and pull request.

---

## Jenkins Integration

Jenkins is used as a build server to validate the project.

### Jenkins Workflow:

1. Pull latest code from GitHub
2. Install dependencies
3. Run Pytest
4. Verify build success

This ensures code quality before deployment.

---

## Conclusion

This project demonstrates a complete DevOps lifecycle including development, testing, containerization, and CI/CD automation using modern tools.
