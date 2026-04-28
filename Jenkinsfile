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
        string(name: 'IMAGE_NAME', defaultValue: 'aceest-fitness-gym', description: 'Docker image repository name')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Image tag to build and deploy')
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
                bat "\"%PYTHON_EXE%\" -m pytest --cov=aceest --cov-report=term-missing --cov-report=xml:coverage.xml --junitxml=pytest-report.xml -v"
            }
        }

        stage('SonarQube Analysis') {
            when {
                expression { return params.RUN_SONARQUBE }
            }
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQubeServer') {
                        bat "\"${scannerHome}\\bin\\sonar-scanner.bat\""
                    }
                }
            }
        }

        stage('Quality Gate') {
            when {
                expression { return params.RUN_SONARQUBE }
            }
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
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
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push %FULL_IMAGE_NAME%:%IMAGE_TAG%'
                }
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
