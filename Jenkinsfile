def image_versions = []

pipeline {
  agent any 

  environment{
    IMAGE_VERSION = '1.0'
  }
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
          def raw = sh(
            script: '''
              set -e
              cd monitoring-python
              python3 python-jenkins.py
            ''',
            returnStdout: true
          ).trim()

          image_versions = raw
            .replace('[','').replace(']','')   // remove brackets
            .replace("'", '')                  // remove single quotes
            .split(',')                        // split by comma
            .collect { it.trim() }
        }
      }
    }

    stage("Deploy") {
      input {
        message "Choose version to deploy"
        ok "Done"
        parameters {
          choice(name: 'ImageVersion', choices: image_versions , description: '')
        }
      }
      steps {
        script {
          echo "Choose ${ImageVersion}"
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