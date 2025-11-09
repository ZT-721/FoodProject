#!/bin/bash

# 冰箱救星 AI 食譜推薦系統 - 快速啟動腳本

echo "🍔 冰箱救星 AI 食譜推薦系統"
echo "================================"

# 檢查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 請先安裝 Node.js 18+"
    exit 1
fi

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 請先安裝 Python 3.9+"
    exit 1
fi

# 檢查 PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ 請先安裝 PostgreSQL"
    exit 1
fi

echo "✅ 環境檢查通過"

# 設定環境變數
export FLASK_APP=app.py
export FLASK_ENV=development

# 建立必要的目錄
mkdir -p backend/uploads
mkdir -p backend/chroma_db

echo "📁 建立必要目錄"

# 檢查是否已安裝依賴
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 安裝前端依賴..."
    cd frontend
    npm install
    cd ..
fi

if [ ! -f "backend/.env" ]; then
    echo "⚙️  設定環境變數..."
    cp backend/env.example backend/.env
    echo "請編輯 backend/.env 檔案，填入您的 API Keys"
fi

# 檢查資料庫
echo "🗄️  檢查資料庫..."
if ! psql -lqt | cut -d \| -f 1 | grep -qw fridge_saver_db; then
    echo "建立資料庫..."
    createdb fridge_saver_db
fi

# 檢查是否已建立表格
if ! psql fridge_saver_db -c "\dt" | grep -q recipes; then
    echo "📊 建立資料庫表格和範例資料..."
    cd backend
    python3 data/create_recipe_database.py
    cd ..
fi

# 檢查是否已建立向量索引
if [ ! -d "backend/chroma_db" ] || [ -z "$(ls -A backend/chroma_db)" ]; then
    echo "🧠 建立向量索引..."
    cd backend
    python3 data/create_vector_index.py
    cd ..
fi

echo ""
echo "🚀 準備啟動服務..."
echo ""
echo "請在兩個不同的終端中執行以下命令："
echo ""
echo "終端 1 (後端):"
echo "  cd backend"
echo "  python3 app.py"
echo ""
echo "終端 2 (前端):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "然後訪問 http://localhost:3000 開始使用！"
echo ""
echo "📚 更多資訊請查看 docs/ 目錄"
echo "🔧 如有問題請查看 docs/development-guide.md"




