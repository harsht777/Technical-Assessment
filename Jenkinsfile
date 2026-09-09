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
                script {
                    if (isUnix()) {
                        sh 'pip install -r requirements.txt || python3 -m pip install -r requirements.txt'
                    } else {
                        bat 'python -m pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo "running tests"
                script {
                    if (isUnix()) {
                        sh 'pytest tests/ || python3 -m pytest tests/'
                    } else {
                        bat 'python -m pytest tests/'
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "building docker image"
                script {
                    if (isUnix()) {
                        sh 'docker build -t sre-api .'
                    } else {
                        bat 'docker build -t sre-api .'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "deploying with compose"
                script {
                    if (isUnix()) {
                        sh 'docker compose down && docker compose up -d'
                    } else {
                        bat 'docker compose down'
                        bat 'docker compose up -d'
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                echo "checking if api is up"
                script {
                    if (isUnix()) {
                        sh 'sleep 5 && curl -f http://localhost/health || curl -f http://localhost:5050/health'
                    } else {
                        bat 'timeout /t 5'
                        bat 'curl http://localhost/health'
                    }
                }
            }
        }
    }
}
