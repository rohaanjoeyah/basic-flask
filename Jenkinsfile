def flag = false // Set to false to see the test stage get skipped

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building Project'
            }
        }
        stage('Test') {
            when {
                expression { flag == true }
            }
            steps {
                echo 'Testing Project'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying Project'
            }
        }
    }
    post {
        always {
            echo 'Post Build condition running'
        }
        failure {
            echo 'Post action if Build Fails'
        }
    }
}
