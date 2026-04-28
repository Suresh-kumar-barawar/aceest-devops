# ACEest Fitness & Gym CI/CD Pipeline Report

## 1. CI/CD architecture overview

The ACEest Fitness & Gym application was refactored into a modular Flask project and connected to a Git-based DevOps workflow. Source code is managed in GitHub with a dedicated `devops-cicd` branch and release tags such as `v1.0.0`. Jenkins is used as the primary CI/CD server and reads the repository `Jenkinsfile` directly from GitHub, which keeps the build pipeline version-controlled and reproducible.

The pipeline installs Python dependencies, executes Pytest test cases, generates coverage reports, and can optionally trigger SonarQube analysis, Docker image build and push, and Kubernetes deployment. Docker packages the Flask application into a consistent container image, while Kubernetes manifests support deployment in Minikube with multiple rollout strategies including rolling update, blue-green, canary, A/B testing, and shadow deployment.

## 2. Challenges faced and mitigation strategies

One major challenge was migrating from a Jenkins Freestyle job to Pipeline-as-Code. Initially Jenkins still executed old batch commands, so the solution was to create a dedicated Pipeline job that loads the `Jenkinsfile` from GitHub. Another issue came from the Jenkins Windows service environment, where `python` and `py` were not available in PATH. This was fixed by using the absolute Python executable path in the pipeline.

Another challenge was preparing the application for containerized and orchestrated deployment. The Flask app was updated with `/healthz` and `/version` endpoints so Docker and Kubernetes can perform health checks and identify application versions. Additional Kubernetes manifests were prepared to demonstrate advanced deployment strategies required by the assignment, while keeping the core service definition reusable.

## 3. Key automation outcomes

The final solution provides automated test execution with 100% coverage for the `aceest` package, a Jenkins pipeline with optional quality and deployment stages, a production-ready Docker image definition, and Kubernetes resources for multi-strategy deployment. This improves reliability because every code change can be validated before packaging or release.

From a DevOps perspective, the project demonstrates continuous integration through automated build and test validation, continuous delivery through Docker image creation and optional registry push, and continuous deployment readiness through scripted Kubernetes rollout support. The repository now contains all major deliverables expected in the assignment: modular Flask application, Git history and versioning, Jenkinsfile, test suite, SonarQube configuration, Dockerfile, Kubernetes YAML files, and rollout strategy implementation.
