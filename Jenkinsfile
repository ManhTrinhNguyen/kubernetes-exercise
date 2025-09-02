
pipeline {
  agent any 

  environment{
    ECR_REGISTRY = "660753258283.dkr.ecr.us-west-1.amazonaws.com"
    ECR_REPO = "java-gradle"
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
          
          versions = result
            .replace('[','').replace(']','')   // remove brackets
            .replace("'", '')                  // remove single quotes
            .split(',')                        // split by comma
            .collect { it.trim()}  
            .join('\n')

          if (!versions) {
            error 'No versions returned by python-jenkins.py'
          }

          version_to_deploy = input message: 'Select version to deploy', ok: 'Deploy', parameters: [choice(name: 'Select version', choices: versions)]
          env.DOCKER_IMAGE = "${ECR_REGISTRY}/${ECR_REPO}:${version_to_deploy}"

          echo env.DOCKER_IMAGE
        }
      }
    }
  }
}