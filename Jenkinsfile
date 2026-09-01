pipeline{
    agent any
    environment{
        VENV_DIR="venv"
        GCP-PROJECT="project-33e67f8a-e18a-4bbc-b7a"
        GCLOUD-PATH="/var/jenkins_home/google-cloud-project/bin"
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

        stage('building and pushing the docker image to gcr'){
            steps{
                withCredentials([file(credentialsId:'gcp-key'), var:'google_cloud_credentials'])
                script{
                    echo 'building and pushing the docker image to gcr'
                    sh '''
                    export PATH $PATH:${GCLOUD_PATH}

                    gcloud auth service-account-activate --key-file=${google_cloud_credentials}

                    gcloud config set-project=${GCP-PROJECT}

                    gcloud auth configure-docker --quiet

                    docker build -t gcr.io${GCP-PROJECT}/mlops-project-1 .

                    docker push gcr.io${GCP-PROJECT}/mlops-project-1

                    '''
                }
            }
        }

        stage('deploy the docker image to gcr'){
            steps{
                withCredentials([file(credentialsId:'gcp-key'), var:'google_cloud_credentials'])
                script{
                    echo 'deploy the docker image to gcr'
                    sh '''
                    export PATH $PATH:${GCLOUD_PATH}

                    gcloud auth service-account-activate --key-file=${google_cloud_credentials}

                    gcloud config set-project=${GCP-PROJECT}

                    gcloud auth configure-docker --quiet

                    gcloud run deploy mlops-project-1 \
                        --image=gcr.io${GCP-PROJECT}/mlops-project-1 \
                        --platform=managed \
                        --region=us-central1 \
                        --access=unauthenticated
                    '''
                }
            }
        }
    }
}