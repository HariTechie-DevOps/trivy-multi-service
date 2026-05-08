pipeline {

    agent any

    environment {
        REGISTRY = "docker.io"
        IMAGE_TAG = "${BUILD_NUMBER}"
        REPORT_DIR = "reports"
        SERVICES = "auth-service payment-service user-service notification-service"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 45, unit: 'MINUTES')
    }

    stages {

        // =========================
        // 🔄 CHECKOUT CODE
        // =========================
        stage('Checkout Code') {
            steps {
                checkout scm
                sh '''
                    echo "Repo cloned successfully"
                    mkdir -p ${REPORT_DIR}
                '''
            }
        }

        // =========================
        // 🐳 BUILD DOCKER IMAGES
        // =========================
        stage('Build Docker Images') {
            steps {
                sh '''
                    for service in $SERVICES; do
                        echo "Building $service..."
                        docker build -t $service:${IMAGE_TAG} ./services/$service
                    done
                '''
            }
        }

        // =========================
        // 🔍 TRIVY SCAN (SECURITY)
        // =========================
        stage('Trivy Scan') {
            steps {
                sh '''
                    mkdir -p ${REPORT_DIR}

                    for service in $SERVICES; do
                        echo "Scanning $service..."

                        trivy image \
                            --format json \
                            --output ${REPORT_DIR}/${service}.json \
                            $service:${IMAGE_TAG}
                    done
                '''
            }
        }

        // =========================
        // 📊 CONVERT METRICS (READY FOR PROMETHEUS PIPELINE)
        // =========================
        stage('Generate Security Metrics') {
            steps {
                sh '''
                    echo "Preparing metrics for future Prometheus integration"

                    for file in ${REPORT_DIR}/*.json; do
                        echo "Processed: $file"
                    done
                '''
            }
        }

        // =========================
        // 🚀 DOCKER COMPOSE DEPLOY
        // =========================
        stage('Deploy Stack') {
            steps {
                sh '''
                    docker compose down || true
                    docker compose up -d --build
                '''
            }
        }
    }

    post {

        success {
            echo "✅ Pipeline completed successfully"
            mail to: 'harisankar.doodleblue@gmail.com@gmail.com',
                 subject: "SUCCESS: Trivy Multi-Service Build ${BUILD_NUMBER}",
                 body: "Build completed. Check reports folder."
        }

        failure {
            echo "❌ Pipeline failed"
            mail to: 'harisankar.doodleblue@gmail.com@gmail.com',
                 subject: "FAILED: Trivy Multi-Service Build ${BUILD_NUMBER}",
                 body: "Check Jenkins logs."
        }

        always {
            sh '''
                echo "Cleaning unused images..."
                docker system prune -f || true
            '''
        }
    }
}
