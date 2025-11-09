# 冰箱救星 AI 食譜推薦系統

## 🎯 專案概述

這是一個基於 AI 的剩餘食材食譜推薦系統，旨在解決使用者冰箱中剩餘食材的應用問題。透過上傳食材照片，系統會自動識別食材並推薦適合的料理食譜。

## ✨ 核心功能

### 1. AI 食材識別
- 支援多張圖片批次上傳
- 使用 Google Vision API 進行智能識別
- 手動編輯和調整食材清單
- 食材分類和信心度顯示

### 2. RAG 食譜推薦
- 基於檢索增強生成技術
- 根據食材吻合度推薦食譜
- 提供替代方案建議
- 支援多種篩選條件

### 3. 使用者體驗
- 響應式設計，支援多種裝置
- 直觀的操作介面
- 詳細的食譜步驟展示
- 使用者回饋機制

## 🏗️ 技術架構

### 前端技術棧
- **React 18** + **TypeScript**: 現代化前端框架
- **Tailwind CSS**: 實用優先的 CSS 框架
- **React Query**: 資料管理和快取
- **React Router**: 路由管理
- **React Dropzone**: 檔案上傳
- **Lucide React**: 圖示庫

### 後端技術棧
- **Python Flask**: 輕量級 Web 框架
- **PostgreSQL**: 關聯式資料庫
- **ChromaDB**: 向量資料庫
- **SQLAlchemy**: ORM 框架

### AI 服務
- **Google Vision API**: 食材圖片識別
- **OpenAI GPT API**: 食譜生成
- **Sentence-BERT**: 文本嵌入模型
- **LangChain**: RAG 框架

## 🚀 快速開始

### 前置需求
- Node.js 18+
- Python 3.9+
- PostgreSQL 12+
- Google Cloud API Key
- OpenAI API Key

### 安裝步驟

1. **複製專案**
```bash
git clone <repository-url>
cd fridge-saver-ai
```

2. **設定後端**
```bash
cd backend
pip install -r requirements.txt
cp env.example .env
# 編輯 .env 檔案，填入 API Keys
```

3. **設定資料庫**
```bash
# 建立 PostgreSQL 資料庫
createdb fridge_saver_db

# 執行資料庫腳本
python data/create_recipe_database.py
python data/create_vector_index.py
```

4. **設定前端**
```bash
cd frontend
npm install
```

5. **啟動服務**
```bash
# 啟動後端 (終端 1)
cd backend
python app.py

# 啟動前端 (終端 2)
cd frontend
npm start
```

6. **訪問應用程式**
```
前端: http://localhost:3000
後端: http://localhost:5000
```

## 📁 專案結構

```
fridge-saver-ai/
├── frontend/                 # React 前端應用
│   ├── src/
│   │   ├── components/       # React 組件
│   │   ├── pages/           # 頁面組件
│   │   ├── services/        # API 服務
│   │   └── ...
│   ├── package.json
│   └── tailwind.config.js
├── backend/                  # Flask 後端 API
│   ├── routes/              # API 路由
│   ├── app.py              # 主應用程式
│   ├── requirements.txt
│   └── env.example
├── data/                    # 資料庫腳本
│   ├── create_recipe_database.py
│   └── create_vector_index.py
├── docs/                    # 文件
│   ├── README.md
│   ├── deployment-guide.md
│   └── development-guide.md
└── README.md
```

## 🔧 環境變數設定

建立 `backend/.env` 檔案：

```env
# Google Cloud Vision API
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# 資料庫設定
DATABASE_URL=postgresql://username:password@localhost:5432/fridge_saver_db

# Flask 設定
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key

# ChromaDB 設定
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 📊 API 端點

### Vision API
- `POST /api/vision/upload` - 上傳單張圖片
- `POST /api/vision/batch-upload` - 批次上傳圖片

### Recipes API
- `POST /api/recipes/search` - 搜尋食譜
- `GET /api/recipes/popular` - 取得熱門食譜
- `POST /api/recipes/feedback` - 提交回饋

### Ingredients API
- `GET /api/ingredients/categories` - 取得食材分類
- `GET /api/ingredients/search` - 搜尋食材
- `POST /api/ingredients/validate` - 驗證食材

## 🧪 測試

```bash
# 後端測試
cd backend
python -m pytest tests/

# 前端測試
cd frontend
npm test
```

## 🚀 部署

### 使用 Docker

```bash
# 建立 Docker 映像
docker build -t fridge-saver-ai .

# 執行容器
docker run -p 5000:5000 fridge-saver-ai
```

### 使用雲端平台

- **Vercel** (前端)
- **Render** (後端)
- **Supabase** (資料庫)

## 🤝 貢獻

1. Fork 專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 授權

本專案採用 MIT 授權 - 查看 [LICENSE](LICENSE) 檔案了解詳情。

## 🙏 致謝

- [Google Vision API](https://cloud.google.com/vision)
- [OpenAI](https://openai.com/)
- [ChromaDB](https://www.trychroma.com/)
- [LangChain](https://langchain.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)

## 📞 聯絡資訊

如有問題或建議，請透過以下方式聯絡：

- 建立 [Issue](../../issues)
- 發送 [Pull Request](../../pulls)
- 電子郵件: your-email@example.com

---

**讓 AI 幫你把剩食變美食！** 🍽️✨