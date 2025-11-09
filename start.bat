@echo off

REM 冰箱救星 AI 食譜推薦系統 - Windows 快速啟動腳本

echo 🍔 冰箱救星 AI 食譜推薦系統
echo ================================

REM 檢查 Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 請先安裝 Node.js 18+
    pause
    exit /b 1
)

REM 檢查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 請先安裝 Python 3.9+
    pause
    exit /b 1
)

REM 檢查 PostgreSQL
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 請先安裝 PostgreSQL
    pause
    exit /b 1
)

echo ✅ 環境檢查通過

REM 設定環境變數
set FLASK_APP=app.py
set FLASK_ENV=development

REM 建立必要的目錄
if not exist "backend\uploads" mkdir backend\uploads
if not exist "backend\chroma_db" mkdir backend\chroma_db

echo 📁 建立必要目錄

REM 檢查是否已安裝前端依賴
if not exist "frontend\node_modules" (
    echo 📦 安裝前端依賴...
    cd frontend
    npm install
    cd ..
)

REM 檢查環境變數檔案
if not exist "backend\.env" (
    echo ⚙️  設定環境變數...
    copy backend\env.example backend\.env
    echo 請編輯 backend\.env 檔案，填入您的 API Keys
)

echo.
echo 🚀 準備啟動服務...
echo.
echo 請在兩個不同的命令提示字元中執行以下命令：
echo.
echo 命令提示字元 1 (後端):
echo   cd backend
echo   python app.py
echo.
echo 命令提示字元 2 (前端):
echo   cd frontend
echo   npm start
echo.
echo 然後訪問 http://localhost:3000 開始使用！
echo.
echo 📚 更多資訊請查看 docs\ 目錄
echo 🔧 如有問題請查看 docs\development-guide.md
echo.
pause




