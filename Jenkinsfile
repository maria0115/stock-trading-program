pipeline {
    agent any

    environment {
        EXE_NAME = "stock-trading.exe"
        BUILD_DIR = "${WORKSPACE}"
        FRONTEND_BUILD_DIR = "${WORKSPACE}\\frontend\\build"
        BACKEND_BUILD_DIR = "${WORKSPACE}\\backend"
        WEB_SERVER_PATH = "C:\\inetpub\\wwwroot\\downloads"
        NUITKA_CACHE_DIR = "C:\\nuitka_cache"
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
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {  // 🚀 오류를 잡고 다음 스테이지로 진행
                    bat """
                    echo "Frontend Build Path: ${FRONTEND_BUILD_DIR}"
                    if not exist ${FRONTEND_BUILD_DIR} (
                        echo " ERROR: Frontend build folder not found!"
                        exit /b 1
                    ) else (
                        echo " Frontend build folder found!"
                    )
                    """
                    bat """
                    echo "Copying frontend build to backend..."
                    mkdir ${BACKEND_BUILD_DIR}\\frontend_build || echo "INFO: Directory already exists."
                    robocopy ${FRONTEND_BUILD_DIR} ${BACKEND_BUILD_DIR}\\frontend_build /E
                    """
                    bat """
                    if exist ${BACKEND_BUILD_DIR}\\frontend_build\\index.html (
                        echo " Frontend build successfully copied to backend."
                    ) else (
                        echo " ERROR: Frontend build was not copied correctly!"
                        exit /b 1
                    )
                    """
                    bat "exit /b 0" // 🔥 `ERRORLEVEL`을 0으로 초기화하여 Jenkins가 실패로 인식하지 않도록 함
                }
            }
        }



        stage('Setup Python Virtual Environment') {  //  venv 설정 단계 추가
            steps {
                script {
                    echo "Setting up Python Virtual Environment..."
                }
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') { 
                    bat """
                    chcp 65001 > nul
                    cd ${BACKEND_BUILD_DIR}

                    :: 현재 PATH에서 conda와 python 확인
                    echo "Checking Python & Conda paths..."
                    where python
                    where conda

                    :: Conda 환경 활성화 테스트
                    echo "Activating Conda environment..."
                    call activate stock-recommendation || (echo " ERROR: Failed to activate Conda environment" & exit /b 1)
                    python --version || (echo " ERROR: Python is not installed or not in PATH" & exit /b 1)

                    :: venv가 없으면 새로 생성
                    if not exist venv (
                        echo "Creating Python Virtual Environment..."
                        python -m venv venv || (echo " ERROR: Failed to create venv" & exit /b 1)
                    )

                    :: venv 활성화 후 패키지 설치
                    call venv\\Scripts\\activate || (echo " ERROR: Failed to activate venv" & exit /b 1)
                    echo " Virtual Environment activated successfully."

                    :: pip 업그레이드 및 패키지 설치
                    python -m pip install --upgrade pip || (echo " ERROR: Failed to upgrade pip" & exit /b 1)
                    python -m pip install -r requirements.txt || (echo " ERROR: Failed to install dependencies" & exit /b 1)

                    echo " Virtual Environment setup completed successfully."
                    """
                }
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
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {  
                    bat """
                    cd ${BACKEND_BUILD_DIR}
                    call venv\\Scripts\\activate || (echo "❌ ERROR: Failed to activate venv" & exit /b 1)
                    echo "✅ Virtual Environment activated."

                    :: 빌드 디렉토리 초기화
                    if exist dist rmdir /s /q dist
                    mkdir dist

                    :: Nuitka 빌드 실행 (로그 출력 추가)
                    nuitka --onefile --no-dependency --lto=no --disable-console --assume-yes-for-downloads --standalone --mingw64 --nofollow-import-to=venv --output-dir=dist app/main.py --show-progress --show-scons

                    :: 빌드 성공 여부 확인
                    if exist dist\\stock-trading.exe (
                        echo "✅ EXE build completed successfully."
                    ) else (
                        echo "❌ ERROR: EXE build failed!"
                        exit /b 1
                    )
                    """
                }
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
