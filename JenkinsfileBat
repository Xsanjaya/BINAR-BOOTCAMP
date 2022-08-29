pipeline {
  agent {
    label 'WindowsAWS1'
  }
  stages {
    stage('PREPARATION') {
      steps {
        bat '''
        @echo "STARTING DEPLOYMENT %JOB_NAME%"
        pip install -r requirements.txt
        Xcopy /y * "C:\\APP\\FlaskAPI" /E /C /I
        '''
      }
    }
    stage('Runing APP') {
      steps {
        bat '''
        cd C:\\APP\\FlaskAPI
        flask db init
        flask db migrate
        flask db upgrade
        nssm restart flask-api
        '''
      }
    }
  }  
}
