pipeline {
    agent none
    stages {

        stage('Backend') {
            agent {
                docker { image 'python:3.10-alpine3.14' }
            }
            steps {
                sh 'cd back && ls && pip install -r requirements.txt'
                sh 'python manage.py runserver'
                sh 'python manage.py test'
            }
        }
        stage('Forntend') {
            agent {
                docker { image 'node:14-alpine' }
            }
            steps {
                sh 'cd front && npm install'
                sh 'npm run build'
                sh 'npm run test:unit'
            }
        }
    }
}


// pipeline {
//     agent any
//     stages {
//         stage('docker Install') {
//             steps {
//                 sh 'docker-compose up'
//             }
//         }
//         stage('Backend Install') {
//             agent {
//                     docker { image 'python:3.10-alpine3.14' }
//             //         docker { image 'node:14-alpine' }
//                 }
//             steps {
//                 sh 'cd back && ls && pip install -r requirements.txt'
//             }
//         }
//
//         stage('Backend Build') {
//             steps {
//                 sh 'cd back && python manage.py runserver'
//             }
//         }
//         stage('Backend Test') {
//             steps {
//                 sh 'cd back && python manage.py test'
//             }
//         }
//         stage('Frontend Install') {
//             steps {
//                 sh 'cd front && npm install'
//             }
//         }
//         stage('Frontend Build') {
//             steps {
//                 sh 'cd front && npm run build'
//             }
//         }
//         stage('Frontend Test') {
//             steps {
//                 sh 'cd front && npm run test:unit'
//             }
//         }
//     }
// }
