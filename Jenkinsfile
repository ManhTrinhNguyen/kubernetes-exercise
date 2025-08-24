pipeline {
  agent any 

  tools {
    gradle "gradle-8.14"
  }

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

    stage("Build Artifact") {
      steps {
        script {
          sh "gradle clean build"
        }
      }
    }

    stage("Build Docker Image then Push to Dockerhub") {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: 'Docker_Credential', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
            sh "docker build -t nguyenmanhtrinh/demo-app:${IMAGE_NAME}-${IMAGE_VERSION} ."

            sh "echo ${PASSWORD} | docker login -u ${USERNAME} --password-stdin"

            sh "docker push nguyenmanhtrinh/demo-app:${IMAGE_NAME}-${IMAGE_VERSION}"
          }
        }
      }
    }

    stage("Deploy with K8s") {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        APP_NAME = "${IMAGE_NAME}-${IMAGE_VERSION}"
      }
      steps {
        script {
          sh "envsubst < kubernetes/java-helm-chart/values.yaml | helm upgrade --install java-app kubernetes/java-helm-chart -f -"
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