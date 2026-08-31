pipeline{
    agent any
    environment{
        VENV_DIR="venv"
    }
    stages{
        stage('Clone Github repo'){
            steps{
                script{
                    echo 'cloning code from github repo'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-1', url: 'https://github.com/Mohittrathee/mlops-hotel-booking.git']])
                    echo 'code cloned successfully'
                }
            }
        }
        stage('Setup virtual environment'){
            steps{
                script{
                    echo 'setting up virtual environment'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    '''
                    echo 'virtual environment created successfully'
                }
            }
        }
        stage('Install dependencies'){
            steps{
                script{
                    echo 'installing dependencies'
                    sh "${VENV_DIR}/bin/pip install --no-cache-dir -r requirements.txt"
                    echo 'dependencies installed successfully'
                }
            }
        }
        stage('Run training pipeline'){
            steps{
                script{
                    echo 'running training pipeline'
                    sh "${VENV_DIR}/bin/python pipeline/training_pipeline.py"
                    echo 'training pipeline completed successfully'
                }
            }
        }
    }
}