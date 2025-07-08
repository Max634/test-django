pipeline {
  agent any

  environment {
    // Make sure your AWS credentials ID matches what you have in Jenkins
    AWS_CREDENTIALS = 'aws-creds'
    AWS_REGION      = 'us-east-1'
    ECR_ACCOUNT     = '842112866380'
    IMAGE_NAME      = 'test:django'
    ECR_REPO        = "${ECR_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    FULL_TAG        = "${ECR_REPO}/${IMAGE_NAME}"
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/Max634/test-django'
      }
    }

    stage('Login to ECR') {
      steps {
        withAWS(region: "${AWS_REGION}", credentials: "${AWS_CREDENTIALS}") {
          powershell '''
            # Install just the ECR cmdlet into the current user context
            Install-Module -Name AWS.Tools.ECR -Force -Scope CurrentUser -AllowClobber

            # Load the module
            Import-Module AWS.Tools.ECR

            # Fetch a login password and authenticate Docker
            $password = Get-ECRLoginPassword -Region $Env:AWS_REGION
            docker login --username AWS --password $password $Env:ECR_REPO
          '''
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        powershell """
          docker build -t ${IMAGE_NAME} .
          docker tag ${IMAGE_NAME} ${FULL_TAG}
        """
      }
    }

    stage('Push Docker Image') {
      steps {
        powershell """
          docker push ${FULL_TAG}
        """
      }
    }
  }

  post {
    success {
      echo "✅ Build and push succeeded: ${FULL_TAG}"
    }
    failure {
      echo "❌ Build or push failed—check console output for errors."
    }
  }
}
