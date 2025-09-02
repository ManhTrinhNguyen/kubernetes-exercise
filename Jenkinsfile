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
        AWS_ACCESS_KEY_ID = credentials('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = credentials('aws_secret_access_key')
      }
      steps {
        script {
          sh '''
          cd monitoring-python 
          python3 python-jenkins.py
          '''
        }
      }
    }

    stage("Deploy") {
      input {
        message "Choose version to deploy"
        ok "Done"
        parameters {
          choice(name: 'ImageVersion', choices: ['1.0', '2.0', '3.0'], descriptions: '')
        }
      }
      steps {
        script {
          echo "Choost ${ImageVersion}"
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