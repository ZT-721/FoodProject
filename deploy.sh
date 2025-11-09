#!/bin/bash

# 冰箱救星 AI 食譜推薦系統 - 一鍵部署腳本

echo "🚀 冰箱救星 AI 食譜推薦系統 - 一鍵部署"
echo "========================================"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函數：顯示訊息
show_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

show_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

show_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

show_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查必要工具
check_requirements() {
    show_message "檢查部署需求..."
    
    local missing_tools=()
    
    # 檢查 Git
    if ! command -v git &> /dev/null; then
        missing_tools+=("git")
    fi
    
    # 檢查 Node.js
    if ! command -v node &> /dev/null; then
        missing_tools+=("node")
    fi
    
    # 檢查 npm
    if ! command -v npm &> /dev/null; then
        missing_tools+=("npm")
    fi
    
    # 檢查 Python
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    # 檢查 Docker (可選)
    if ! command -v docker &> /dev/null; then
        show_warning "Docker 未安裝，將跳過 Docker 部署選項"
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        show_error "缺少必要工具: ${missing_tools[*]}"
        show_message "請先安裝缺少的工具後再執行部署腳本"
        exit 1
    fi
    
    show_success "所有必要工具已安裝"
}

# 設定環境變數
setup_environment() {
    show_message "設定環境變數..."
    
    # 建立 .env 檔案
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# 資料庫設定
DATABASE_URL=postgresql://username:password@localhost:5432/fridge_saver_db

# Supabase 設定 (部署時需要)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Google Vision API
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project"}

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key

# Flask 設定
FLASK_ENV=production
SECRET_KEY=your-production-secret-key

# 檔案設定
CHROMA_PERSIST_DIRECTORY=./chroma_db
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=16777216
EOF
        show_warning "已建立 .env 檔案，請編輯並填入實際的 API Keys"
    else
        show_message ".env 檔案已存在"
    fi
}

# 部署選單
show_deployment_menu() {
    echo ""
    echo "請選擇部署方案："
    echo "1. 本地開發環境"
    echo "2. Docker 容器部署"
    echo "3. Vercel + Render + Supabase (推薦)"
    echo "4. 只部署前端 (Vercel)"
    echo "5. 只部署後端 (Render)"
    echo "6. 設定 Supabase 資料庫"
    echo "7. 退出"
    echo ""
    read -p "請輸入選項 (1-7): " choice
}

# 本地開發環境部署
deploy_local() {
    show_message "設定本地開發環境..."
    
    # 安裝後端依賴
    cd backend
    pip install -r requirements.txt
    cd ..
    
    # 安裝前端依賴
    cd frontend
    npm install
    cd ..
    
    # 建立必要目錄
    mkdir -p backend/uploads backend/chroma_db
    
    show_success "本地開發環境設定完成"
    show_message "執行以下命令啟動服務："
    echo "  終端 1: cd backend && python app.py"
    echo "  終端 2: cd frontend && npm start"
}

# Docker 部署
deploy_docker() {
    show_message "使用 Docker 部署..."
    
    if ! command -v docker &> /dev/null; then
        show_error "Docker 未安裝，請先安裝 Docker"
        return 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        show_error "Docker Compose 未安裝，請先安裝 Docker Compose"
        return 1
    fi
    
    # 建立環境變數檔案
    if [ ! -f ".env.docker" ]; then
        cat > .env.docker << EOF
POSTGRES_DB=fridge_saver_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
DATABASE_URL=postgresql://postgres:password123@db:5432/fridge_saver_db
SECRET_KEY=your-production-secret-key
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project"}
OPENAI_API_KEY=sk-your-openai-api-key
EOF
        show_warning "已建立 .env.docker 檔案，請編輯並填入實際的 API Keys"
    fi
    
    # 啟動 Docker 服務
    docker-compose --env-file .env.docker up -d
    
    show_success "Docker 服務已啟動"
    show_message "訪問 http://localhost 使用應用程式"
}

# Vercel 部署
deploy_vercel() {
    show_message "部署前端到 Vercel..."
    
    if ! command -v vercel &> /dev/null; then
        show_message "安裝 Vercel CLI..."
        npm install -g vercel
    fi
    
    cd frontend
    
    # 設定環境變數
    read -p "請輸入後端 API URL (例如: https://your-backend.onrender.com): " backend_url
    
    echo "REACT_APP_API_URL=${backend_url}/api" > .env.production
    echo "REACT_APP_ENVIRONMENT=production" >> .env.production
    
    # 部署到 Vercel
    vercel --prod
    
    show_success "前端已部署到 Vercel"
    cd ..
}

# Render 部署
deploy_render() {
    show_message "部署後端到 Render..."
    
    show_message "請按照以下步驟手動部署到 Render："
    echo "1. 前往 https://render.com/"
    echo "2. 點擊 'New +' > 'Web Service'"
    echo "3. 連接您的 GitHub 倉庫"
    echo "4. 設定以下參數："
    echo "   - Name: fridge-saver-backend"
    echo "   - Environment: Python 3"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: python app.py"
    echo "5. 設定環境變數（參考 docs/deployment-guide.md）"
    echo "6. 點擊 'Create Web Service'"
    
    read -p "按 Enter 繼續..."
}

# Supabase 設定
setup_supabase() {
    show_message "設定 Supabase 資料庫..."
    
    show_message "請按照以下步驟設定 Supabase："
    echo "1. 前往 https://supabase.com/"
    echo "2. 建立新專案"
    echo "3. 在 Settings > Database 中取得連線字串"
    echo "4. 在 Settings > API 中取得 Project URL 和 anon key"
    echo "5. 執行以下命令初始化資料庫："
    echo "   cd supabase"
    echo "   python init_database.py"
    
    read -p "按 Enter 繼續..."
}

# 完整部署 (Vercel + Render + Supabase)
deploy_full() {
    show_message "執行完整部署 (Vercel + Render + Supabase)..."
    
    echo ""
    show_message "步驟 1: 設定 Supabase 資料庫"
    setup_supabase
    
    echo ""
    show_message "步驟 2: 部署後端到 Render"
    deploy_render
    
    echo ""
    show_message "步驟 3: 部署前端到 Vercel"
    deploy_vercel
    
    show_success "完整部署流程完成！"
    show_message "請檢查各服務的部署狀態並測試功能"
}

# 主函數
main() {
    show_message "開始部署流程..."
    
    # 檢查需求
    check_requirements
    
    # 設定環境
    setup_environment
    
    # 顯示選單並處理選擇
    while true; do
        show_deployment_menu
        
        case $choice in
            1)
                deploy_local
                ;;
            2)
                deploy_docker
                ;;
            3)
                deploy_full
                ;;
            4)
                deploy_vercel
                ;;
            5)
                deploy_render
                ;;
            6)
                setup_supabase
                ;;
            7)
                show_message "退出部署腳本"
                exit 0
                ;;
            *)
                show_error "無效選項，請重新選擇"
                ;;
        esac
        
        echo ""
        read -p "按 Enter 繼續..."
    done
}

# 執行主函數
main
