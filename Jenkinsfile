pipeline {
    agent any

    environment {
        EXE_NAME = "stock-trading.exe"
        BUILD_DIR = "C:\\Project\\stock\\stock-recommendation\\stock-trading-program"
        FRONTEND_BUILD_DIR = "C:\\Project\\stock\\stock-recommendation\\stock-trading-program\\frontend\\build"
        BACKEND_BUILD_DIR = "C:\\Project\\stock\\stock-recommendation\\stock-trading-program\\backend"
        WEB_SERVER_PATH = "C:\\inetpub\\wwwroot\\downloads"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/maria0115/stock-trading-program.git'
            }
        }

        stage('Build Frontend') {
            steps {
                bat "cd %BUILD_DIR%\\frontend && npm install && npm run build"
            }
        }

        stage('Prepare Backend') {
            steps {
                bat "mkdir %BACKEND_BUILD_DIR%\\frontend_build"
                bat "xcopy /E /I /Y %FRONTEND_BUILD_DIR% %BACKEND_BUILD_DIR%\\frontend_build"
            }
        }

        stage('Build Backend EXE') {
            steps {
                bat "cd %BACKEND_BUILD_DIR% && nuitka --standalone --mingw64 --output-dir=dist app/main.py"
            }
        }

        stage('Upload to Web Server') {
            steps {
                bat "copy %BACKEND_BUILD_DIR%\\dist\\%EXE_NAME% %WEB_SERVER_PATH%\\"
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    echo "EXE 다운로드 링크: http://localhost/downloads/${EXE_NAME}"
                }
            }
        }
    }
}
