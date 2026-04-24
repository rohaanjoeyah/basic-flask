pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building Project'
            }
        }
        stage('Test') {
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
    // The conditions here will execute after the build is done
    post {
        always {
            // This action will happen always regardless of the result of build
            echo 'Post Build condition running'
        }
        failure {
            // This action will happen only if the build has failed
            echo 'Post action if Build Fails'
        }
    }
}
