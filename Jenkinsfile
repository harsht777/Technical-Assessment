pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "pulling code"
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "installing dependencies"
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo "running tests"
                bat 'python -m pytest tests/'
            }
        }

        stage('Docker Build') {
            steps {
                echo "building docker image"
                bat 'docker build -t sre-api .'
            }
        }

        stage('Deploy') {
            steps {
                echo "deploying with compose"
                bat 'docker compose down'
                bat 'docker compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                echo "checking if api is up"
                bat 'timeout /t 5'
                bat 'curl http://localhost/health'
            }
        }
    }
}
