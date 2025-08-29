pipeline {
  agent any 

  environment {
    IMAGE_VERSION = "1.0.1"
    IMAGE_NAME = "java-gradle"
  }

  stages {
    stage("Increment Version") {
      steps {
        script {
          echo "Increment Version"
        }
      }
    }

    stage("Test") {
      steps {
        script {
          echo "Test 111"
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