pipeline {
    agent {
        //docker { image 'node:14-alpine' }
        docker { image 'nikolaik/python-nodejs' }
    }
    stages {
        stage('Backend Install') {
            steps {
                sh 'cd back && python3 pip install -r requirements.txt'
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
