pipeline {
    agent any
    stages {
//         stage('Database'){
//             steps{
//                 step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker-compose.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: false])
//             }
//         }

        stage('Backend') {
            agent {
                docker {
                    image 'python:3.10-alpine3.14'
                }
            }
//             environment {
//                 DATABASE_NAME = 'postgresql'
//                 DATABASE_USER = 'admin'
//                 DATABASE_PASSWORD = 'admin'
//                 DATABASE_HOST = "127.0.0.1"
//                 DATABASE_PORT = "5432"
//             }
            steps {
//                 sh 'python --version'
                sh 'apk add --no-cache gcc musl-dev'
                sh 'apk add --no-cache postgresql-dev'
//                 sh 'pip install psycopg2-binary==2.9.2'
                sh 'cd back && ls && pip install -r requirements.txt'
//                 sh 'cd back && ls && python manage.py runserver'
//                 sh 'cd back && ls && python manage.py test'
            }
        }
        stage('Frontend') {
            agent {
                docker { image 'node:14-alpine' }
            }
            steps {
                sh 'cd front && npm install'
                //sh 'cd front && npm run build'
                sh 'cd front && npm run test:unit'
            }
        }
    }
//     post {
//         always {
//             step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker-compose.yml', option: [$class: 'StopAllServices'], useCustomDockerComposeFile: false])
//         }
//     }
}
