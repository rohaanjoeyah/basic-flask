pipeline {
    agent any
    
    parameters {
        // These are types of parameters
        string(name: 'VERSION', defaultValue: '', description: 'Version to deploy on prod')
        choice(name: 'CHOICE_VERSION', choices: ['1.1.0', '1.2.0', '1.3.0'], description: '')
        booleanParam(name: 'executeTests', defaultValue: true, description: 'Check to run tests')
    }

    tools {
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
                bat "mvn -version"
            }
        }
        stage('Test') {
            when {
                // This checks the boolean parameter we defined above
                expression { params.executeTests == true }
            }
            steps {
                echo 'Testing Project'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying Project'
                // Printing out the string parameter the user typed in
                echo "Deploying user version: ${params.VERSION}" 
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
