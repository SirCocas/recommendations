pipeline{
    agent any
    stages{
        stage("Recommendation"){
            steps{
                checkout scm
                sh "python3 imdb.py"
            }
        }
    }
    post {
        always {
            // Archive both the script and its output
            archiveArtifacts artifacts: 'imdb_recommendations.txt', fingerprint: true
            deleteDir()
        }
    }
}