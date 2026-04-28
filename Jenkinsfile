pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pytest --cov=aceest --cov-report=term-missing -v'
            }
        }
    }
}
