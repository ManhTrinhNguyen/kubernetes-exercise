
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
          def result = sh(
            script: '''
              set -e
              cd monitoring-python
              python3 python-jenkins.py
            ''',
            returnStdout: true
          ).trim()
          
          def jsonish = result.replaceAll("'", '"')

          availableVersions = new groovy.json.JsonSlurperClassic().parseText(jsonish) as List

          echo "${availableVersions}"

          version_to_deploy = input message: 'Select version to deploy', ok: 'Deploy', parameters: [choice(name: 'Select version', choices: availableVersions)]
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