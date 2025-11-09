# 冰箱救星 AI 食譜推薦系統 - 部署指南

## 🌐 線上部署方案

本專案提供多種部署方案，讓您可以快速將系統部署到線上供使用者使用。

## 🚀 推薦部署方案

### 方案一：Vercel + Render + Supabase (推薦)

**優點**：
- 免費額度充足
- 設定簡單
- 效能優異
- 自動部署

**架構**：
- **前端**：Vercel (React 應用)
- **後端**：Render (Flask API)
- **資料庫**：Supabase (PostgreSQL)

## 📋 部署步驟

### 1. 準備工作

#### 取得必要的 API Keys

1. **Google Cloud Vision API**
   - 前往 [Google Cloud Console](https://console.cloud.google.com/)
   - 啟用 Vision API
   - 建立服務帳戶並下載 JSON 金鑰

2. **OpenAI API**
   - 前往 [OpenAI Platform](https://platform.openai.com/)
   - 建立 API Key

3. **Supabase**
   - 前往 [Supabase](https://supabase.com/)
   - 建立新專案
   - 取得專案 URL 和 API Keys

### 2. 部署資料庫 (Supabase)

#### 步驟 1：建立 Supabase 專案
1. 登入 [Supabase](https://supabase.com/)
2. 點擊 "New Project"
3. 選擇組織和專案名稱
4. 設定資料庫密碼
5. 選擇區域 (建議選擇離使用者最近的區域)

#### 步驟 2：初始化資料庫
```bash
# 設定環境變數
export DATABASE_URL="postgresql://postgres:[password]@db.[project-id].supabase.co:5432/postgres"

# 執行初始化腳本
cd supabase
python init_database.py
```

#### 步驟 3：取得連線資訊
在 Supabase 儀表板中：
- 前往 Settings > Database
- 複製 Connection string
- 前往 Settings > API
- 複製 Project URL 和 anon key

### 3. 部署後端 (Render)

#### 步驟 1：準備程式碼
1. 將程式碼推送到 GitHub
2. 確保 `render.yaml` 檔案在根目錄

#### 步驟 2：建立 Render 服務
1. 登入 [Render](https://render.com/)
2. 點擊 "New +" > "Web Service"
3. 連接 GitHub 倉庫
4. 設定服務參數：
   - **Name**: fridge-saver-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python data/create_recipe_database.py && python data/create_vector_index.py`
   - **Start Command**: `python app.py`

#### 步驟 3：設定環境變數
在 Render 儀表板中設定以下環境變數：
```
DATABASE_URL=postgresql://postgres:[password]@db.[project-id].supabase.co:5432/postgres
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_ANON_KEY=[your-anon-key]
GOOGLE_APPLICATION_CREDENTIALS_JSON=[your-google-service-account-json]
OPENAI_API_KEY=[your-openai-api-key]
FLASK_ENV=production
SECRET_KEY=[your-secret-key]
CHROMA_PERSIST_DIRECTORY=./chroma_db
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=16777216
```

#### 步驟 4：部署
1. 點擊 "Create Web Service"
2. 等待建置完成
3. 記錄服務 URL (例如：https://fridge-saver-backend.onrender.com)

### 4. 部署前端 (Vercel)

#### 步驟 1：準備程式碼
1. 確保 `vercel.json` 檔案在 `frontend` 目錄
2. 更新 API URL：
```bash
cd frontend
echo "REACT_APP_API_URL=https://fridge-saver-backend.onrender.com/api" > .env.production
```

#### 步驟 2：建立 Vercel 專案
1. 登入 [Vercel](https://vercel.com/)
2. 點擊 "New Project"
3. 連接 GitHub 倉庫
4. 選擇 `frontend` 資料夾作為根目錄

#### 步驟 3：設定環境變數
在 Vercel 儀表板中設定：
```
REACT_APP_API_URL=https://fridge-saver-backend.onrender.com/api
REACT_APP_ENVIRONMENT=production
```

#### 步驟 4：部署
1. 點擊 "Deploy"
2. 等待建置完成
3. 獲得前端 URL (例如：https://fridge-saver-frontend.vercel.app)

### 5. 設定 CORS

在後端 `app.py` 中更新 CORS 設定：
```python
CORS(app, origins=[
    "https://fridge-saver-frontend.vercel.app",
    "http://localhost:3000"  # 開發環境
])
```

## 🐳 Docker 部署方案

### 本地 Docker 部署

```bash
# 1. 建立環境變數檔案
cp backend/env.example .env
# 編輯 .env 檔案，填入實際的 API Keys

# 2. 啟動服務
docker-compose up -d

# 3. 初始化資料庫
docker-compose exec backend python data/create_recipe_database.py
docker-compose exec backend python data/create_vector_index.py

# 4. 訪問應用程式
# 前端: http://localhost:3000
# 後端: http://localhost:5000
```

### 雲端 Docker 部署

#### 使用 Railway
1. 連接 GitHub 倉庫
2. 選擇 `docker-compose.yml`
3. 設定環境變數
4. 部署

#### 使用 DigitalOcean App Platform
1. 建立 App
2. 選擇 Docker
3. 上傳 `docker-compose.yml`
4. 設定環境變數
5. 部署

## 🔧 環境變數設定

### 後端環境變數
```env
# 資料庫
DATABASE_URL=postgresql://postgres:[password]@db.[project-id].supabase.co:5432/postgres

# Supabase
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_ANON_KEY=[your-anon-key]

# Google Vision API
GOOGLE_APPLICATION_CREDENTIALS_JSON=[your-google-service-account-json]

# OpenAI API
OPENAI_API_KEY=[your-openai-api-key]

# Flask 設定
FLASK_ENV=production
SECRET_KEY=[your-secret-key]

# 檔案設定
CHROMA_PERSIST_DIRECTORY=./chroma_db
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=16777216
```

### 前端環境變數
```env
REACT_APP_API_URL=https://your-backend-url.onrender.com/api
REACT_APP_ENVIRONMENT=production
```

## 📊 監控和維護

### 1. 健康檢查
- 後端：`https://your-backend-url.onrender.com/api/health`
- 前端：檢查 Vercel 部署狀態

### 2. 日誌監控
- **Render**：在儀表板查看應用程式日誌
- **Vercel**：在 Functions 標籤查看日誌
- **Supabase**：在 Logs 標籤查看資料庫日誌

### 3. 效能監控
- 使用 Vercel Analytics 監控前端效能
- 使用 Render Metrics 監控後端效能
- 使用 Supabase Dashboard 監控資料庫效能

## 🚨 故障排除

### 常見問題

#### 1. CORS 錯誤
**問題**：前端無法連接到後端 API
**解決方案**：
```python
# 在 backend/app.py 中更新 CORS 設定
CORS(app, origins=[
    "https://your-frontend-url.vercel.app",
    "http://localhost:3000"
])
```

#### 2. 資料庫連線失敗
**問題**：後端無法連接到 Supabase
**解決方案**：
- 檢查 `DATABASE_URL` 是否正確
- 確認 Supabase 專案狀態
- 檢查網路連線

#### 3. API 金鑰錯誤
**問題**：Google Vision API 或 OpenAI API 呼叫失敗
**解決方案**：
- 檢查 API 金鑰是否正確
- 確認 API 配額是否充足
- 檢查服務帳戶權限

#### 4. 檔案上傳失敗
**問題**：圖片上傳失敗
**解決方案**：
- 檢查檔案大小限制
- 確認上傳目錄權限
- 檢查網路連線

### 除錯技巧

1. **檢查日誌**：查看各平台的日誌輸出
2. **測試 API**：使用 Postman 或 curl 測試 API 端點
3. **檢查環境變數**：確認所有環境變數都正確設定
4. **網路檢查**：確認服務之間的網路連線

## 📈 效能優化

### 1. 快取策略
- 使用 Redis 快取 API 回應
- 設定適當的 Cache-Control 標頭
- 使用 CDN 加速靜態資源

### 2. 資料庫優化
- 建立適當的索引
- 使用連線池
- 定期清理舊資料

### 3. 前端優化
- 使用程式碼分割
- 壓縮圖片和資源
- 實作懶載入

## 🔒 安全性考量

### 1. API 安全性
- 使用 HTTPS
- 實作 API 限流
- 驗證輸入資料
- 使用環境變數儲存敏感資訊

### 2. 資料保護
- 啟用 RLS (Row Level Security)
- 加密敏感資料
- 定期備份資料

### 3. 存取控制
- 限制 API 存取
- 使用適當的 CORS 設定
- 監控異常存取

## 📞 支援

### 部署支援
- 查看各平台的文件
- 使用社群論壇
- 建立 Issue 回報問題

### 監控工具
- **Uptime Robot**：監控服務可用性
- **Sentry**：錯誤追蹤
- **Google Analytics**：使用者分析

---

**現在您可以開始部署您的冰箱救星 AI 食譜推薦系統了！** 🚀✨