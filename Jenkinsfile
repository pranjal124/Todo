pipeline {
    agent any
      environment {
        IMAGE_NAME = "todo-app"
        CONTAINER_NAME = "todo-container"
        HOST_PORT = "8081"
        CONTAINER_PORT = "5000"
        // AWS Configuration
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        AWS_DEFAULT_REGION = "ap-south-1"
        AWS_ACCOUNT_ID = "905418382935" // Replace with your AWS Account ID
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
        ECR_REPOSITORY = "todo-app"
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                git branch: 'feature/todo-pipeline', 
                    url: 'https://github.com/pranjal124/Todo.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}"
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"
                }
            }
        }
        
        stage('Login to ECR') {
            steps {
                echo 'Logging into AWS ECR...'
                script {
                    sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                }
            }
        }
        
        stage('Push to ECR') {
            steps {
                echo 'Pushing Docker image to ECR...'
                script {
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}"
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"
                }
            }
        }
        
        stage('Stop Previous Container') {
            steps {
                echo 'Stopping previous container...'
                script {
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                }
            }
        }
        
        stage('Run Container') {
            steps {
                echo 'Running Docker container from ECR image...'
                script {                    sh """
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p ${HOST_PORT}:${CONTAINER_PORT} \
                            -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
                            -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
                            -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
                            ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                script {
                    sh "sleep 10"
                    sh "docker ps | grep ${CONTAINER_NAME}"
                    sh "curl -f http://localhost:${HOST_PORT} || exit 1"
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Pipeline succeeded! Application is running at http://localhost:8081'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}
