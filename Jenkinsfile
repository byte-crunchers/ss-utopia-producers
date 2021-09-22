pipeline {
    agent any

    stages {
      stage('checkout') {
        steps {
          git branch: 'feature_jenkins', credentialsId: 'git_login', url: 'https://github.com/byte-crunchers/ss-utopia-producers.git'
        }
      }
        
        stage("SonarQube analysis") {
            agent any
            steps {
              script  {
                scannerHome = tool 'SonarQubeScanner';
                }
              
              withSonarQubeEnv('SonarQube') {
                bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers"
              }
            }
          }
          stage("Quality Gate") {
            steps {
              echo message: "can not do on local machine "
             /* timeout(time: 5, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
              }*/
            }
          }
          stage('Build') {
            steps {
                  echo message: "dockefile not ready yet"
                  //sh 'docker build . -t jbnilles/ss-utopia-auth:latest'
            }
        }
        stage('Deploy') {
            steps {
              echo message: "docker not ready yet"
                //sh 'docker push jbnilles/ss-utopia-auth:latest'
            }
        }
    }

}