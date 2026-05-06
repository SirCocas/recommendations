pipeline {
    agent { label "${params.AGENT_LABEL}" }
    stages {
        stage("Recommendation") {
            steps {
                checkout scm
                sh "python3 imdb.py"
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts: 'imdb_recommendations.txt', fingerprint: true
            deleteDir()
        }
        failure {
            deleteDir()
        }
        aborted {
            deleteDir()
        }
    }
}
