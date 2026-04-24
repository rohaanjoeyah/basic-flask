def flag = true 

pipeline {
    agent any
    
    environment {
        // Variables defined here can be used by any stage
        NEW_VERSION = '1.3.0'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Project'
                // Using environment variable. Use double quotes to output the value!
                echo "Building version ${NEW_VERSION}"
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
