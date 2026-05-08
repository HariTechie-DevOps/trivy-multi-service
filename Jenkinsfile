pipeline {

    agent any

    environment {

        IMAGE_TAG  = "${BUILD_NUMBER}"
        REPORT_DIR = "reports"

        SERVICES = """
        auth-service
        payment-service
        user-service
        notification-service
        """
    }

    options {
        timestamps()
        timeout(time: 45, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // =====================================================
        // 📥 CHECKOUT SOURCE CODE
        // =====================================================
        stage('Checkout') {
            steps {

                checkout scm

                sh '''
                    echo "Repository cloned successfully"

                    mkdir -p ${REPORT_DIR}

                    echo "Workspace:"
                    pwd

                    ls -la
                '''
            }
        }

        // =====================================================
        // 🐳 BUILD ALL MICROSERVICE IMAGES
        // =====================================================
        stage('Build Docker Images') {

            steps {

                sh '''

                    for service in ${SERVICES}; do

                        echo "======================================="
                        echo "Building Docker Image: $service"
                        echo "======================================="

                        docker build \
                            -t $service:${IMAGE_TAG} \
                            ./services/$service

                    done
                '''
            }
        }

        // =====================================================
        // 🔍 TRIVY SECURITY SCAN
        // =====================================================
        stage('Trivy Scan') {

            steps {

                sh '''

                    mkdir -p ${REPORT_DIR}

                    for service in ${SERVICES}; do

                        echo "======================================="
                        echo "Scanning: $service"
                        echo "======================================="

                        trivy image \
                            --severity HIGH,CRITICAL,MEDIUM,LOW \
                            --format json \
                            --output ${REPORT_DIR}/${service}.json \
                            $service:${IMAGE_TAG}

                    done
                '''
            }
        }

        // =====================================================
        // 📂 VERIFY REPORTS
        // =====================================================
        stage('Verify Reports') {

            steps {

                sh '''

                    echo "Generated Reports:"

                    ls -lh ${REPORT_DIR}

                '''
            }
        }

        // =====================================================
        // 🚀 DEPLOY FULL STACK
        // =====================================================
        stage('Deploy Stack') {

            steps {

                sh '''

                    echo "Stopping existing containers..."

                    docker compose down || true

                    echo "Starting full DevSecOps stack..."

                    docker compose up -d --build

                    echo "Containers Running:"
                    docker ps

                '''
            }
        }

        // =====================================================
        // 📊 VERIFY PROMETHEUS METRICS
        // =====================================================
        stage('Verify Metrics') {

            steps {

                sh '''

                    echo "Waiting exporter startup..."

                    sleep 20

                    echo "Testing exporter metrics..."

                    curl http://localhost:8000/metrics || true

                '''
            }
        }
    }

    // =========================================================
    // 📦 POST ACTIONS
    // =========================================================
    post {

        success {

            echo "======================================="
            echo "✅ PIPELINE COMPLETED SUCCESSFULLY"
            echo "======================================="

            echo "Grafana : http://98.87.239.189:3000"
            echo "Prometheus : http://98.87.239.189:9090"
        }

        failure {

            echo "======================================="
            echo "❌ PIPELINE FAILED"
            echo "======================================="
        }

        always {

            archiveArtifacts artifacts: 'reports/*.json',
                             fingerprint: true

            sh '''

                echo "Cleaning dangling images..."

                docker image prune -f || true

            '''
        }
    }
}
