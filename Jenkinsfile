pipeline {
    agent any

    stages {
      stage('checkout') {
        steps {
          git branch: 'develop', credentialsId: 'git_login', url: 'https://github.com/byte-crunchers/ss-utopia-producers.git'
        }
      }
      stage('prep python') {
        steps{
          /*sh '''pip install JayDeBeApi
                pip install mysql
                pip install Faker
                pip install bcrypt
                pip install coverage
                pip install -U pytest
                pip install random-username
                pip install mysql-connector-python
                pip install numpy
                pip install pyzipcode
                '''
                */
                echo 'only needed to set up machine once'
        
        }
      }
      stage('start h2 server') {
        steps{
          sh 'python fill_db.py h2'
          //sh 'cd ..'
        }
      }
      
      stage('run account test')
      {
        steps{
            dir('account_producer') {
                sh 'coverage run -m pytest'
                sh 'coverage xml'
            }
        }
      }
      stage('run branch test')
      {
        steps{
           dir('branch_producer') {
                sh 'coverage run -m pytest'
                sh 'coverage xml'
            }
        }
      }
      stage('run card test')
      {
        steps{
           dir('card_producer') {
                sh 'coverage run -m pytest'
                sh 'coverage xml'
            }
        }
      }
      stage('run loan payment test')
      {
        steps{
           dir('loan_payment_producer') {
                sh 'coverage run -m pytest'
                sh 'coverage xml'
            }
        }
      }
      stage('run loan  test')
      {
        steps{
           dir('loan_producer') {
                sh 'coverage run -m pytest'
                sh 'coverage xml'
            }
        }
      }
      stage('run stock test')
      {
        steps{
           dir('stock_producer') {
                sh 'coverage run -m pytest'
                sh 'coverage xml'
            }
        }
      }
      stage('run transaction test')
      {
        steps{
           dir('transaction_producer') {
                sh 'coverage run -m pytest'
                sh 'coverage xml'
            }
        }
      }
      stage('run user test')
      {
        steps{
           dir('user_producer') {
                sh 'coverage run -m pytest'
                sh 'coverage xml'
            }
        }
      }
        
        stage("SonarQube analysis") {
            steps {
                dir('account_producer') {
                   script {
                        scannerHome = tool 'SonarQubeScanner';
                        echo  "${scannerHome}"
                    
              
                    withSonarQubeEnv('SonarQube') {
                        bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers-account-producer -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                   }
                    
                }
                dir('branch_producer') {
                   script {
                        scannerHome = tool 'SonarQubeScanner';
                        echo  "${scannerHome}"
                    
              
                    withSonarQubeEnv('SonarQube') {
                        bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers-branch-producer -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                   }
                    
                }
                dir('card_producer') {
                   script {
                        scannerHome = tool 'SonarQubeScanner';
                        echo  "${scannerHome}"
                    
              
                    withSonarQubeEnv('SonarQube') {
                        bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers-card-producer -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                   }
                    
                }
                dir('loan_payment_producer') {
                   script {
                        scannerHome = tool 'SonarQubeScanner';
                        echo  "${scannerHome}"
                    
              
                    withSonarQubeEnv('SonarQube') {
                        bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers-loan_payment-producer -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                   }
                    
                }
                dir('loan_producer') {
                   script {
                        scannerHome = tool 'SonarQubeScanner';
                        echo  "${scannerHome}"
                    
              
                    withSonarQubeEnv('SonarQube') {
                        bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers-loan-producer -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                   }
                    
                }
                dir('stock_producer') {
                   script {
                        scannerHome = tool 'SonarQubeScanner';
                        echo  "${scannerHome}"
                    
              
                    withSonarQubeEnv('SonarQube') {
                        bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers-stock-producer -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                   }
                    
                }
                dir('transaction_producer') {
                   script {
                        scannerHome = tool 'SonarQubeScanner';
                        echo  "${scannerHome}"
                    
              
                    withSonarQubeEnv('SonarQube') {
                        bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers-transaction-producer -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                   }
                    
                }
                dir('user_producer') {
                   script {
                        scannerHome = tool 'SonarQubeScanner';
                        echo  "${scannerHome}"
                    
              
                    withSonarQubeEnv('SonarQube') {
                        bat "${scannerHome}/bin/sonar-scanner.bat -Dsonar.projectKey=ss-utopia-producers-user-producer -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                   }
                    
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