pipeline {
    agent any
    stages {
        stage("Recommendation") {
            steps {
                checkout scm
                sh "python3 imdb.py"
                sh "ls -l"
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts: 'imdb_recommendations.txt', fingerprint: true
        }
        always {
            deleteDir()
        }
    }
}