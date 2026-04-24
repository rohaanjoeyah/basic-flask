def flag = true 

pipeline {
    agent any
    
    tools {
        // Make sure 'Maven' matches the exact name in your Jenkins Tools configuration
        maven 'Maven' 
    }
    
    environment {
        NEW_VERSION = '1.3.0'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Project'
                echo "Building version ${NEW_VERSION}"
                // Using bat for Windows instead of sh
                bat "mvn -version" 
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
