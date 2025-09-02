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
      steps {
        script {
          sh '''
          cd monitoring-python
          source app-monitoring/bin/activate
          app-monitoring/bin/pip install boto3
          app-monitoring/bin/python3 python-jenkins.py
          '''
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