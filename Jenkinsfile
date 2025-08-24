pipeline {
  agent any 

  tools {
    gradle "gradle-9.1.0-rc-1"
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

    stage("Build Artifact") {
      steps {
        script {
          sh "gradle clean build"
        }
      }
    }

    stage("Build Docker Image then Push to ECR") {
      steps {
        script {
          echo "Docker Image"
        }
      }
    }

    stage("Deploy with K8s") {
      steps {
        script {
          echo "Deploy"
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