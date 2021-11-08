pipeline {
    agent {
        docker { image 'node:14-alpine' }
    }
    stages {
        stage('Not ready Backend Install') {
            steps {
                sh 'echo not yet...'
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