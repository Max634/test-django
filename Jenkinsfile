pipeline {
  agent any

  environment {
    // Jenkins AWS credential ID
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
        git branch: 'main',
            url: 'https://github.com/Max634/test-django'
      }
    }

    stage('Login to ECR') {
      steps {
        // withAWS only injects keys—does not install aws cli or modules
        withAWS(region: "${AWS_REGION}", credentials: "${AWS_CREDENTIALS}") {
          powershell '''
            # Ensure PSGallery is trusted & NuGet provider is available (non-interactive)
            Set-PSRepository -Name PSGallery -InstallationPolicy Trusted -ErrorAction SilentlyContinue
            if (-not (Get-PackageProvider -Name NuGet -ErrorAction SilentlyContinue)) {
              Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force -Scope CurrentUser
            }

            # Install AWS.Tools.ECR without prompting
            Install-Module -Name AWS.Tools.ECR -Force -AllowClobber -Scope CurrentUser -AcceptLicense

            # Import and run the login cmdlet
            Import-Module AWS.Tools.ECR
            $pw = Get-ECRLoginPassword -Region $Env:AWS_REGION
            docker login --username AWS --password $pw $Env:ECR_REPO
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
      echo "✅ Successfully built & pushed: ${FULL_TAG}"
    }
    failure {
      echo "❌ Pipeline failed—check the console output above for details."
    }
  }
}
