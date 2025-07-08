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
          Write-Output "Downloading AWS CLI ZIP..."
          $zip = "$Env:TEMP\\awscli.zip"
          Invoke-WebRequest -Uri "https://awscli.amazonaws.com/awscli-exe-windows-x86_64.zip" -OutFile $zip

          Write-Output "Extracting AWS CLI..."
          Expand-Archive -Path $zip -DestinationPath "$Env:TEMP\\awscli" -Force
          Remove-Item $zip

          # Point to the extracted aws.exe
          $Env:AWS_CLI_EXE = "$Env:TEMP\\awscli\\aws\\aws.exe"
          Write-Output "AWS CLI version:"
          & $Env:AWS_CLI_EXE --version
        '''
      }
    }

    stage('Login to ECR') {
      steps {
        withAWS(region: "${AWS_REGION}", credentials: "${AWS_CREDENTIALS}") {
          powershell '''
            Write-Output "Logging into ECR..."
            & $Env:AWS_CLI_EXE ecr get-login-password --region $Env:AWS_REGION |
              docker login --username AWS --password-stdin $Env:REPO_URI
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
