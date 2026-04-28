# ACEest Fitness & Gym DevOps Pipeline

ACEest is a Flask API packaged for a university DevOps assignment. The repository now includes:

- a modular Flask application
- Pytest tests with coverage
- a Jenkins pipeline in `Jenkinsfile`
- SonarQube project configuration
- a production-oriented Dockerfile
- Kubernetes manifests for rolling, blue-green, canary, A/B, and shadow deployment strategies

## Project structure

- `app.py`: runtime entry point
- `aceest/`: Flask package and routes
- `tests/`: Pytest test suite
- `Dockerfile`: production image build
- `Jenkinsfile`: CI/CD pipeline definition
- `sonar-project.properties`: SonarQube scanner settings
- `k8s/`: Kubernetes base manifests and deployment strategies
- `scripts/`: helper automation scripts for Kubernetes deployment
- `versions/`: assignment source history

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

Default URL:

```text
http://127.0.0.1:5000
```

Useful endpoints:

- `/`
- `/healthz`
- `/version`
- `/programs`
- `/clients`

## Testing

Run tests:

```powershell
python -m pytest -v
```

Run tests with coverage:

```powershell
python -m pytest --cov=aceest --cov-report=term-missing --cov-report=xml:coverage.xml -v
```

## Jenkins pipeline

The Jenkins pipeline supports these stages:

1. Checkout
2. Install dependencies
3. Run tests and generate coverage + JUnit reports
4. Optional SonarQube analysis
5. Optional Docker image build and push
6. Optional Kubernetes deployment

Recommended Jenkins prerequisites:

- Python available at the path used in `Jenkinsfile`
- SonarQube server configured in Jenkins as `SonarQubeServer`
- SonarScanner tool configured in Jenkins as `SonarScanner`
- Docker Hub credentials stored as `dockerhub-creds`
- `kubectl` configured to access Minikube or your target cluster

## Docker

Build the image:

```powershell
docker build -t aceest-fitness-gym:latest .
```

Run the container:

```powershell
docker run --rm -p 5000:5000 -e APP_VERSION=v1.0.0 aceest-fitness-gym:latest
```

## Kubernetes

Apply the rolling deployment:

```powershell
kubectl apply -f k8s/base
kubectl apply -f k8s/strategies/rolling
```

Apply a different strategy:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\deploy-k8s.ps1 -Strategy canary -Image docker.io/<dockerhub-user>/aceest-fitness-gym:v1.0.0
```

Expose the application in Minikube:

```powershell
minikube service aceest-service -n aceest-devops --url
```

## Report starter points

- CI validates every commit with Jenkins and Pytest coverage.
- SonarQube adds static analysis and quality gate enforcement.
- Docker provides consistent packaging across environments.
- Kubernetes manifests demonstrate multiple release strategies with rollback-friendly patterns.
