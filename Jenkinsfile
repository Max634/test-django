```groovy
pipeline {
  agent any

  environment {
    AWS_REGION      = 'us-east-1'
    AWS_CREDENTIALS = 'aws-creds'
    ECR_ACCOUNT     = '842112866380'
    REPO_URI        = "${ECR_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    IMAGE_NAME      = 'test:django'
    IMAGE_TAG       = "${REPO_URI}/${IMAGE_NAME}"
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/Max634/test-django'
      }
    }

    stage('Install AWS CLI') {
      steps {
        powershell '''
          Write-Output "Downloading AWS CLI MSI..."
          $msi = "$Env:TEMP\\AWSCLIV2.msi"
          Invoke-WebRequest -Uri "https://awscli.amazonaws.com/AWSCLIV2.msi" -OutFile $msi

          Write-Output "Installing AWS CLI..."
          Start-Process msiexec.exe -Wait -ArgumentList "/i", $msi, "/qn"

          Remove-Item $msi

          Write-Output "AWS CLI version:"
          aws --version
        '''
      }
    }

    stage('Login to ECR') {
      steps {
        withAWS(region: "${AWS_REGION}", credentials: "${AWS_CREDENTIALS}") {
          powershell '''
            Write-Output "Logging into ECR..."
            $password = aws ecr get-login-password --region $Env:AWS_REGION
            docker login --username AWS --password $password $Env:REPO_URI
          '''
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        powershell '''
          docker build -t $Env:IMAGE_NAME .
          docker tag $Env:IMAGE_NAME $Env:IMAGE_TAG
        '''
      }
    }

    stage('Push Docker Image') {
      steps {
        powershell '''
          docker push $Env:IMAGE_TAG
        '''
      }
    }
  }

  post {
    success {
      echo "✅ Successfully built & pushed: ${IMAGE_TAG}"
    }
    failure {
      echo "❌ Pipeline failed—check the console logs for details."
    }
  }
}
```
