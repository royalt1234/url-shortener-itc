pipeline {
    agent any

    environment {
        // Defines the generic placeholder for the Jenkins SonarQube Server configuration name
        SONAR_SERVER = 'sq-server'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Dependencies') {
            steps {
                dir('backend') {
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests and Coverage') {
            steps {
                dir('backend') {
                    sh '''
                    . venv/bin/activate
                    # Run tests and generate coverage.xml
                    pytest tests/ --cov=. --cov-report=xml
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(env.SONAR_SERVER) {
                    sh '''
                    # Execute SonarScanner (expecting sonar-scanner CLI installed on agent)
                    sonar-scanner
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    // This pauses until Sonar computes the quality gate
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace if needed
            cleanWs()
        }
    }
}
