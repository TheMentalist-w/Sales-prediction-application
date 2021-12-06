pipeline {
    agent any
//     environment {
//         DATABASE_NAME = 'postgresql'
//         DATABASE_USER = 'admin'
//         DATABASE_PASSWORD = 'admin'
//         DATABASE_HOST = "127.0.0.1"
//         DATABASE_PORT = "5432"
//     }
    stages {
        stage('Database'){
            steps{
                step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker-compose.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: false])
            }
        }

        stage('Backend') {
            agent {
                docker {
                    image 'python:3.10-alpine3.14'
                    args '--network="host"'
                }
            }
            environment {
                DATABASE_NAME = 'postgresql'
                DATABASE_USER = 'admin'
                DATABASE_PASSWORD = 'admin'
                DATABASE_HOST = "127.0.0.1"
                DATABASE_PORT = "5432"
            }
            steps {
                sh 'python --version'
                sh 'pip install psycopg2-binary'
                sh 'cd back && ls && pip install -r requirements.txt'
                sh 'cd back && ls && python manage.py runserver'
                //sh 'cd back && ls && python manage.py test'
            }
        }
        stage('Forntend') {
            agent {
                docker { image 'node:14-alpine' }
            }
            steps {
                sh 'cd front && npm install'
                //sh 'cd front && npm run build'
                //sh 'cd front && npm run test:unit'
            }
        }
    }
    post {
        always {
            step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker-compose.yml', option: [$class: 'StopAllServices'], useCustomDockerComposeFile: false])
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
