pipeline {
    agent any

    environment {
        // Hardcoding exact paths so Windows doesn't get confused by PATH variables
        PYTHON_CMD = 'C:\\Users\\harsh\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
        DOCKER_CMD = 'C:\\Users\\harsh\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }

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
                bat '"%PYTHON_CMD%" -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo "running tests"
                bat '"%PYTHON_CMD%" -m pytest tests/'
            }
        }

        stage('Docker Build') {
            steps {
                echo "building docker image"
                bat '"%DOCKER_CMD%" build -t sre-api .'
            }
        }

        stage('Deploy') {
            steps {
                echo "deploying with compose"
                bat '"%DOCKER_CMD%" compose down'
                bat '"%DOCKER_CMD%" compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                echo "checking if api is up"
                bat 'timeout /t 5'
                bat 'curl -f http://localhost/health'
            }
        }
    }
}
