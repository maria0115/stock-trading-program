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
                chcp 65001 > nul
                cd ${BUILD_DIR}\\frontend
                if not exist src\\index.js (
                    echo "ERROR: src/index.js is missing!"
                ) else ( 
                    echo "OK: src/index.js exists." 
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
                echo "Frontend Build Path: ${FRONTEND_BUILD_DIR}"
                if not exist ${FRONTEND_BUILD_DIR} (
                    echo "❌ ERROR: Frontend build folder not found!"
                    exit 1
                ) else (
                    echo "✅ Frontend build folder found!"
                )
                """
                bat """
                echo "Copying frontend build to backend..."
                mkdir ${BACKEND_BUILD_DIR}\\frontend_build || echo "ℹ️ INFO: Directory already exists."
                robocopy ${FRONTEND_BUILD_DIR} ${BACKEND_BUILD_DIR}\\frontend_build /E

                :: 복사된 파일 확인
                if exist ${BACKEND_BUILD_DIR}\\frontend_build\\index.html (
                    echo "✅ Frontend build successfully copied to backend."
                ) else (
                    echo "❌ ERROR: Frontend build was not copied correctly!"
                    exit 1
                )
                """
            }
        }


        stage('Setup Python Virtual Environment') {  // ✅ venv 설정 단계 추가
            steps {
                script {
                    echo "Setting up Python Virtual Environment..."
                }
                bat """
                chcp 65001 > nul
                cd ${BACKEND_BUILD_DIR}
                :: Conda 환경 활성화 및 Python 확인
                call conda activate stock-recommendation || exit /b 1
                python --version || (echo "❌ ERROR: Python is not installed or not in PATH" & exit /b 1)

                :: venv가 없으면 새로 생성
                if not exist venv (
                    echo "Creating Python Virtual Environment..."
                    python -m venv venv || (echo "❌ ERROR: Failed to create venv" & exit /b 1)
                )
                :: venv 활성화 후 패키지 설치
                call venv\\Scripts\\activate || (echo "❌ ERROR: Failed to activate venv" & exit /b 1)
                echo "✅ Virtual Environment activated successfully."

                pip install --upgrade pip || (echo "❌ ERROR: Failed to upgrade pip" & exit /b 1)
                pip install -r requirements.txt || (echo "❌ ERROR: Failed to install dependencies" & exit /b 1)
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
