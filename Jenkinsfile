pipeline {
    agent any

    environment {
        EXE_NAME = "stock-trading.exe"
        BUILD_DIR = "${WORKSPACE}"
        FRONTEND_BUILD_DIR = "${WORKSPACE}\\frontend\\build"
        BACKEND_BUILD_DIR = "${WORKSPACE}\\backend"
        WEB_SERVER_PATH = "C:\\inetpub\\wwwroot\\downloads"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    echo "Building Frontend..."
                }
                bat """
                cd ${BUILD_DIR}\\frontend
                if not exist src\\index.js (
                    echo "ERROR: src/index.js is missing!"
                    exit 1
                )else(
                    echo ok src/index.js
                )
                if not exist node_modules (
                    echo "ERROR: node_modules folder not found! Running npm install..."
                    npm install
                )
                if not exist node_modules\\.bin\\react-scripts (
                    echo "ERROR: react-scripts not found! Installing manually..."
                    npm install react-scripts --save
                )
                call node_modules\\.bin\\react-scripts build
                """
            }
        }

        stage('Prepare Backend') {
            steps {
                script {
                    echo "Checking if frontend build exists..."
                }
                bat """
                if not exist ${FRONTEND_BUILD_DIR} (
                    echo "ERROR: Frontend build folder not found!"
                    exit 1
                )
                """
                bat """
                mkdir ${BACKEND_BUILD_DIR}\\frontend_build
                robocopy ${FRONTEND_BUILD_DIR} ${BACKEND_BUILD_DIR}\\frontend_build /E
                """
            }
        }

        stage('Setup Python Virtual Environment') {  // ✅ venv 설정 단계 추가
            steps {
                script {
                    echo "Setting up Python Virtual Environment..."
                }
                bat """
                cd ${BACKEND_BUILD_DIR}
                if not exist venv (
                    activate stock-recommendation || exit /b 1
                    python --version || exit /b 1
                    python -m venv venv
                )
                venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Install Backend Dependencies') {
            steps {
                script {
                    echo "Installing Backend dependencies..."
                }
                bat """
                cd ${BACKEND_BUILD_DIR}
                venv\\Scripts\\activate
                pip install -r requirements.txt
                """
            }
        }

        stage('Build Backend EXE') {
            steps {
                script {
                    echo "Building EXE with Nuitka..."
                }
                bat """
                cd ${BACKEND_BUILD_DIR}
                venv\\Scripts\\activate
                nuitka --standalone --mingw64 --nofollow-import-to=venv --output-dir=dist app/main.py
                """
            }
        }

        stage('Upload to Web Server') {
            steps {
                script {
                    echo "Uploading EXE to Web Server..."
                }
                bat """
                copy ${BACKEND_BUILD_DIR}\\dist\\${EXE_NAME} ${WEB_SERVER_PATH}\\
                """
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
