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
          python3 --version
          python3 -m pip install --upgrade pip
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