pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    parameters {
        booleanParam(name: 'RUN_SONARQUBE', defaultValue: false, description: 'Run SonarQube analysis using Jenkins SonarQube configuration')
        booleanParam(name: 'BUILD_DOCKER_IMAGE', defaultValue: false, description: 'Build the Docker image after tests pass')
        booleanParam(name: 'PUSH_DOCKER_IMAGE', defaultValue: false, description: 'Push the built Docker image to Docker Hub')
        booleanParam(name: 'DEPLOY_TO_K8S', defaultValue: false, description: 'Deploy the selected version to Kubernetes')
        string(name: 'DOCKERHUB_USERNAME', defaultValue: '', description: 'Docker Hub username or organization for image tagging')
        password(name: 'DOCKERHUB_TOKEN', defaultValue: '', description: 'Docker Hub access token used when push is enabled')
        string(name: 'IMAGE_NAME', defaultValue: 'aceest-fitness-gym', description: 'Docker image repository name')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Image tag to build and deploy')
        string(name: 'SONAR_HOST_URL', defaultValue: 'http://host.docker.internal:9000', description: 'Reachable SonarQube URL from Jenkins')
        password(name: 'SONAR_TOKEN', defaultValue: '', description: 'SonarQube user token')
        choice(name: 'DEPLOYMENT_STRATEGY', choices: ['rolling', 'blue-green', 'canary', 'ab-testing', 'shadow'], description: 'Kubernetes deployment strategy to apply')
    }

    environment {
        PYTHON_EXE = 'C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        K8S_NAMESPACE = 'aceest-devops'
        FULL_IMAGE_NAME = ''
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Build Metadata') {
            steps {
                script {
                    env.FULL_IMAGE_NAME = params.DOCKERHUB_USERNAME?.trim() ? "docker.io/${params.DOCKERHUB_USERNAME}/${params.IMAGE_NAME}" : params.IMAGE_NAME
                    currentBuild.displayName = "#${env.BUILD_NUMBER} ${params.IMAGE_TAG}"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "\"%PYTHON_EXE%\" -m pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                bat "\"%PYTHON_EXE%\" -m pytest --cov=aceest --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml:coverage.xml --junitxml=pytest-report.xml -v"
            }
        }

        stage('SonarQube Analysis') {
            when {
                expression { return params.RUN_SONARQUBE && params.SONAR_TOKEN?.trim() }
            }
            steps {
                bat "docker run --rm -e SONAR_HOST_URL=${params.SONAR_HOST_URL} -e SONAR_TOKEN=${params.SONAR_TOKEN} -v \"%CD%:/usr/src\" sonarsource/sonar-scanner-cli"
            }
        }

        stage('Build Docker Image') {
            when {
                expression { return params.BUILD_DOCKER_IMAGE }
            }
            steps {
                bat "docker build -t %FULL_IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Push Docker Image') {
            when {
                allOf {
                    expression { return params.BUILD_DOCKER_IMAGE }
                    expression { return params.PUSH_DOCKER_IMAGE }
                    expression { return params.DOCKERHUB_USERNAME?.trim() }
                    expression { return params.DOCKERHUB_TOKEN?.trim() }
                }
            }
            steps {
                bat 'echo %DOCKERHUB_TOKEN% | docker login -u %DOCKERHUB_USERNAME% --password-stdin'
                bat 'docker push %FULL_IMAGE_NAME%:%IMAGE_TAG%'
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression { return params.DEPLOY_TO_K8S }
            }
            steps {
                powershell """
                ./scripts/deploy-k8s.ps1 `
                  -Strategy '${params.DEPLOYMENT_STRATEGY}' `
                  -Namespace '${env.K8S_NAMESPACE}' `
                  -Image '${env.FULL_IMAGE_NAME}:${params.IMAGE_TAG}'
                """
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'pytest-report.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'coverage.xml, sonar-project.properties, k8s/**/*.yaml'
        }
    }
}
