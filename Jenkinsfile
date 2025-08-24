pipeline {
  agent any 

  tools {
    gradle "gradle-8.14"
  }

  environment {
    IMAGE_VERSION = "1.0.0"
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
          withCredentials([
            usernamePassword(credentialsId: 'Docker_Credential', usernameVariable: USER, passwordVariable: PASSWORD)
          ]) {
            // sh "docker build -t nguyenmanhtrinh/demo-app:java-gradle-${IMAGE_VERSION} ."
            // sh "docker login -u ${USER} -p ${PASSWORD}"

            sh "echo ${USER} ${PASSWORD}"
          }
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