pipeline {
  agent any 

  stages {
    stage("Check if python installed") {
      steps {
        script {
          sh "python3 --version"
        }
      }
    }

    stage("Fetch all 3 images from the ECR repository (using Python)") {
      environment {
        aws_access_key_id = credentials('aws_access_key_id')
        aws_secret_access_key = credentials('aws_secret_access_key')
        region = 'us-west-1'
      }
      steps {
        script {
          sh '''
          cd monitoring-python 
          python3 python-jenkins.py'''
        }
      }
      
    }


    stage("commit to Git") {
      steps{
        script {
          echo "Commit to Git"
        }
      }
    }
  }
}