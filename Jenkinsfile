pipeline
{
  agent any
  stages{
    stage('Checkout'){
      steps{
        git branch: 'main', url: 'https://github.com/Max634/test-django'
      }
    }
    stage('Login to ECR'){
      steps{
        withAWS(region:'us-east-1',credentials: 'aws-cred'){
          powershell '''
          $password = aws ecr get-login-password --region us-east-1
          docker login --username AWS --password $password 842112866380.dkr.ecr.us-east-1.amazonaws.com
          '''
        }
      }
    }
    stage('Build Docker Image'){
      steps{
        powershell '''
        docker build -t test:django .
        docker tag test:django 842112866380.dkr.ecr.us-east-1.amazonaws.com/test:django
        '''
      }
    }
    stage('Push Docker Image'){
      steps{
        powershell '''
        docker push 842112866380.dkr.ecr.us-east-1.amazonaws.com/test:django
        '''
      }
    }
  }
}
