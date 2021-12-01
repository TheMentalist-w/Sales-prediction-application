pipeline {
    agent {
        docker { image 'python:3.10-alpine3.14' }
//         docker { image 'node:14-alpine' }
//         docker { image 'nikolaik/python-nodejs' }
    }
    stages {
        stage('Backend Install') {
            steps {
                sh 'cd back && ls && pip install -r requirements.txt'
            }
        }
        stage('Backend Build') {
            steps {
                sh 'cd back && python manage.py runserver'
            }
        }
        stage('Backend Test') {
            steps {
                sh 'cd back && python manage.py test'
            }
        }
        stage('Frontend Install') {
            steps {
                sh 'cd front && npm install'
            }
        }
        stage('Frontend Build') {
            steps {
                sh 'cd front && npm run build'
            }
        }
        stage('Frontend Test') {
            steps {
                sh 'cd front && npm run test:unit'
            }
        }
    }
}
