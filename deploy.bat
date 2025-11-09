@echo off

REM 冰箱救星 AI 食譜推薦系統 - Windows 一鍵部署腳本

echo 🚀 冰箱救星 AI 食譜推薦系統 - 一鍵部署
echo ========================================

REM 檢查必要工具
:check_requirements
echo [INFO] 檢查部署需求...

REM 檢查 Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git 未安裝，請先安裝 Git
    pause
    exit /b 1
)

REM 檢查 Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js 未安裝，請先安裝 Node.js
    pause
    exit /b 1
)

REM 檢查 npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm 未安裝，請先安裝 npm
    pause
    exit /b 1
)

REM 檢查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 未安裝，請先安裝 Python
    pause
    exit /b 1
)

REM 檢查 Docker (可選)
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Docker 未安裝，將跳過 Docker 部署選項
)

echo [SUCCESS] 所有必要工具已安裝

REM 設定環境變數
:setup_environment
echo [INFO] 設定環境變數...

if not exist ".env" (
    echo # 資料庫設定 > .env
    echo DATABASE_URL=postgresql://username:password@localhost:5432/fridge_saver_db >> .env
    echo. >> .env
    echo # Supabase 設定 (部署時需要) >> .env
    echo SUPABASE_URL=https://your-project-id.supabase.co >> .env
    echo SUPABASE_ANON_KEY=your-anon-key >> .env
    echo. >> .env
    echo # Google Vision API >> .env
    echo GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project"} >> .env
    echo. >> .env
    echo # OpenAI API >> .env
    echo OPENAI_API_KEY=sk-your-openai-api-key >> .env
    echo. >> .env
    echo # Flask 設定 >> .env
    echo FLASK_ENV=production >> .env
    echo SECRET_KEY=your-production-secret-key >> .env
    echo. >> .env
    echo # 檔案設定 >> .env
    echo CHROMA_PERSIST_DIRECTORY=./chroma_db >> .env
    echo UPLOAD_FOLDER=./uploads >> .env
    echo MAX_CONTENT_LENGTH=16777216 >> .env
    
    echo [WARNING] 已建立 .env 檔案，請編輯並填入實際的 API Keys
) else (
    echo [INFO] .env 檔案已存在
)

REM 部署選單
:show_menu
echo.
echo 請選擇部署方案：
echo 1. 本地開發環境
echo 2. Docker 容器部署
echo 3. Vercel + Render + Supabase (推薦)
echo 4. 只部署前端 (Vercel)
echo 5. 只部署後端 (Render)
echo 6. 設定 Supabase 資料庫
echo 7. 退出
echo.
set /p choice="請輸入選項 (1-7): "

if "%choice%"=="1" goto deploy_local
if "%choice%"=="2" goto deploy_docker
if "%choice%"=="3" goto deploy_full
if "%choice%"=="4" goto deploy_vercel
if "%choice%"=="5" goto deploy_render
if "%choice%"=="6" goto setup_supabase
if "%choice%"=="7" goto exit_script
echo [ERROR] 無效選項，請重新選擇
goto show_menu

REM 本地開發環境部署
:deploy_local
echo [INFO] 設定本地開發環境...

REM 安裝後端依賴
cd backend
pip install -r requirements.txt
cd ..

REM 安裝前端依賴
cd frontend
npm install
cd ..

REM 建立必要目錄
if not exist "backend\uploads" mkdir backend\uploads
if not exist "backend\chroma_db" mkdir backend\chroma_db

echo [SUCCESS] 本地開發環境設定完成
echo [INFO] 執行以下命令啟動服務：
echo   命令提示字元 1: cd backend ^&^& python app.py
echo   命令提示字元 2: cd frontend ^&^& npm start
goto end_menu

REM Docker 部署
:deploy_docker
echo [INFO] 使用 Docker 部署...

docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker 未安裝，請先安裝 Docker
    goto end_menu
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose 未安裝，請先安裝 Docker Compose
    goto end_menu
)

REM 建立環境變數檔案
if not exist ".env.docker" (
    echo POSTGRES_DB=fridge_saver_db > .env.docker
    echo POSTGRES_USER=postgres >> .env.docker
    echo POSTGRES_PASSWORD=password123 >> .env.docker
    echo DATABASE_URL=postgresql://postgres:password123@db:5432/fridge_saver_db >> .env.docker
    echo SECRET_KEY=your-production-secret-key >> .env.docker
    echo GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project"} >> .env.docker
    echo OPENAI_API_KEY=sk-your-openai-api-key >> .env.docker
    
    echo [WARNING] 已建立 .env.docker 檔案，請編輯並填入實際的 API Keys
)

REM 啟動 Docker 服務
docker-compose --env-file .env.docker up -d

echo [SUCCESS] Docker 服務已啟動
echo [INFO] 訪問 http://localhost 使用應用程式
goto end_menu

REM Vercel 部署
:deploy_vercel
echo [INFO] 部署前端到 Vercel...

vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] 安裝 Vercel CLI...
    npm install -g vercel
)

cd frontend

REM 設定環境變數
set /p backend_url="請輸入後端 API URL (例如: https://your-backend.onrender.com): "

echo REACT_APP_API_URL=%backend_url%/api > .env.production
echo REACT_APP_ENVIRONMENT=production >> .env.production

REM 部署到 Vercel
vercel --prod

echo [SUCCESS] 前端已部署到 Vercel
cd ..
goto end_menu

REM Render 部署
:deploy_render
echo [INFO] 部署後端到 Render...
echo [INFO] 請按照以下步驟手動部署到 Render：
echo 1. 前往 https://render.com/
echo 2. 點擊 'New +' ^> 'Web Service'
echo 3. 連接您的 GitHub 倉庫
echo 4. 設定以下參數：
echo    - Name: fridge-saver-backend
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: python app.py
echo 5. 設定環境變數（參考 docs/deployment-guide.md）
echo 6. 點擊 'Create Web Service'

pause
goto end_menu

REM Supabase 設定
:setup_supabase
echo [INFO] 設定 Supabase 資料庫...
echo [INFO] 請按照以下步驟設定 Supabase：
echo 1. 前往 https://supabase.com/
echo 2. 建立新專案
echo 3. 在 Settings ^> Database 中取得連線字串
echo 4. 在 Settings ^> API 中取得 Project URL 和 anon key
echo 5. 執行以下命令初始化資料庫：
echo    cd supabase
echo    python init_database.py

pause
goto end_menu

REM 完整部署
:deploy_full
echo [INFO] 執行完整部署 (Vercel + Render + Supabase)...

echo.
echo [INFO] 步驟 1: 設定 Supabase 資料庫
call :setup_supabase

echo.
echo [INFO] 步驟 2: 部署後端到 Render
call :deploy_render

echo.
echo [INFO] 步驟 3: 部署前端到 Vercel
call :deploy_vercel

echo [SUCCESS] 完整部署流程完成！
echo [INFO] 請檢查各服務的部署狀態並測試功能
goto end_menu

REM 結束選單
:end_menu
echo.
pause
goto show_menu

REM 退出腳本
:exit_script
echo [INFO] 退出部署腳本
exit /b 0




