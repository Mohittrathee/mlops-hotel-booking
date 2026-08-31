pipeline{
    agent any
    stages{
        steps{
            script{
                echo 'cloning code from github repo'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-1', url: 'https://github.com/Mohittrathee/mlops-hotel-booking.git']])
                echo 'code cloned successfully'
                
            }
        }
    }
}