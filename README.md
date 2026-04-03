# ACEest DevOps Project

## Project Overview

This repository contains the ACEest Fitness & Gym Flask application and the DevOps pipeline required for the assignment. The project demonstrates version control with Git and GitHub, automated testing with Pytest, containerization with Docker, CI/CD with GitHub Actions, and build validation with Jenkins.

## Repository Contents

- `app.py`: Flask REST API for ACEest Fitness & Gym
- `requirements.txt`: Python dependencies
- `test_app.py`: Pytest test suite for the Flask endpoints
- `Dockerfile`: Container definition for the application
- `.github/workflows/main.yml`: GitHub Actions workflow
- `versions/`: Assignment-provided application source versions kept for version-history evidence

## Application Features

- Home endpoint to verify service health
- Program listing and program detail endpoints
- Calorie calculation endpoint
- Client creation and retrieval endpoints
- JSON API responses suitable for testing and containerized execution

## Local Setup and Execution

### 1. Clone the repository

```powershell
git clone https://github.com/Suresh-kumar-barawar/aceest-devops.git
cd aceest-devops
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the Flask application

```powershell
python app.py
```

The application starts on:

```text
http://127.0.0.1:5000
```

## Manual Test Execution

Run the complete Pytest suite locally:

```powershell
python -m pytest -v
```

All tests should pass successfully before pushing changes or running container builds.

## Docker Usage

### Build the Docker image

```powershell
docker build -t aceest-app .
```

### Run the application container

```powershell
docker run --rm -p 5000:5000 aceest-app
```

### Run tests inside the Docker container

```powershell
docker run --rm aceest-app python -m pytest test_app.py -v
```

## GitHub Actions CI/CD Workflow

The workflow file is located at `.github/workflows/main.yml`.

### Trigger conditions

- Push to `main`
- Pull request targeting `main`

### Pipeline stages

1. `Build & Lint`
   - Checks out the code
   - Sets up Python
   - Installs Flask, Pytest, and Pyflakes
   - Runs syntax and lint validation on `app.py`

2. `Docker Image Assembly`
   - Builds the Docker image for the application

3. `Automated Testing`
   - Builds the Docker image again for the test job
   - Runs the Pytest suite inside the Docker container

This pipeline ensures that code is validated, containerized, and tested automatically for repository changes.

## Jenkins Integration

Jenkins is used as the secondary build validation environment for the assignment.

### Jenkins job purpose

The Jenkins job pulls the latest repository code and verifies that the project builds and tests successfully in a clean environment.

### Jenkins build logic

The Jenkins job is configured to:

```bat
pip install -r requirements.txt
pytest
```

### Jenkins validation flow

1. Jenkins pulls the project from GitHub
2. Dependencies are installed from `requirements.txt`
3. The Pytest suite is executed
4. Build success confirms the code is valid in the Jenkins environment

Together, GitHub Actions and Jenkins provide two layers of automated validation:

- GitHub Actions validates pull requests and pushes through CI/CD stages
- Jenkins validates that the repository can still be built and tested from an external build server

## Assignment Notes

- The `versions/` folder stores the assignment-provided application versions that were committed one by one to demonstrate Git version progression.
- The final deliverable application used for testing, Docker, GitHub Actions, and Jenkins is the Flask-based implementation in `app.py`.

## Conclusion

This project demonstrates the complete DevOps workflow requested in the assignment: application development, Git-based version tracking, automated testing, Docker containerization, GitHub Actions CI/CD automation, and Jenkins build validation.
