# 冰箱救星 AI 食譜推薦系統 - API 文件

## 📚 API 概述

本系統提供 RESTful API 服務，支援食材識別、食譜推薦和使用者互動功能。

**基礎 URL**: `https://your-backend-url.onrender.com/api`

**認證**: 目前無需認證，未來版本將支援 API Key 認證

## 🔍 端點列表

### 健康檢查
- `GET /` - 系統健康檢查
- `GET /api/health` - API 健康檢查

### 視覺識別 API
- `POST /api/vision/upload` - 上傳單張圖片
- `POST /api/vision/batch-upload` - 批次上傳圖片

### 食譜 API
- `POST /api/recipes/search` - 搜尋食譜
- `GET /api/recipes/popular` - 取得熱門食譜
- `POST /api/recipes/feedback` - 提交回饋

### 食材 API
- `GET /api/ingredients/categories` - 取得食材分類
- `GET /api/ingredients/search` - 搜尋食材
- `POST /api/ingredients/validate` - 驗證食材
- `POST /api/ingredients/suggest` - 建議食材
- `GET /api/ingredients/nutrition/{ingredient}` - 取得營養資訊

## 📋 詳細 API 文件

### 健康檢查

#### GET /
系統健康檢查

**回應**:
```json
{
  "status": "healthy",
  "message": "冰箱救星 AI 食譜推薦系統運行中",
  "version": "1.0.0"
}
```

#### GET /api/health
API 健康檢查

**回應**:
```json
{
  "status": "ok",
  "services": {
    "database": "connected",
    "vision_api": "ready",
    "rag_service": "ready"
  }
}
```

### 視覺識別 API

#### POST /api/vision/upload
上傳單張圖片進行食材識別

**請求**:
- **Content-Type**: `multipart/form-data`
- **Body**: 
  - `file`: 圖片檔案 (JPG, PNG, GIF)

**回應**:
```json
{
  "success": true,
  "ingredients": [
    {
      "name": "番茄",
      "confidence": 0.95,
      "category": "vegetables"
    },
    {
      "name": "雞蛋",
      "confidence": 0.88,
      "category": "others"
    }
  ],
  "filename": "uploaded_image.jpg"
}
```

**錯誤回應**:
```json
{
  "error": "沒有上傳檔案"
}
```

#### POST /api/vision/batch-upload
批次上傳多張圖片

**請求**:
- **Content-Type**: `multipart/form-data`
- **Body**: 
  - `files`: 多個圖片檔案

**回應**:
```json
{
  "success": true,
  "ingredients": [
    {
      "name": "番茄",
      "confidence": 0.95,
      "category": "vegetables"
    }
  ],
  "total_images": 2
}
```

### 食譜 API

#### POST /api/recipes/search
根據食材搜尋食譜

**請求**:
```json
{
  "ingredients": ["番茄", "雞蛋"],
  "preferences": {
    "cooking_time": "30",
    "difficulty": "簡單",
    "cuisine": "中式"
  }
}
```

**參數說明**:
- `ingredients` (必填): 食材清單
- `preferences` (選填): 偏好設定
  - `cooking_time`: 烹飪時間限制 (分鐘)
  - `difficulty`: 難度等級 (簡單/中等/困難)
  - `cuisine`: 菜系 (中式/西式/日式/韓式)

**回應**:
```json
{
  "success": true,
  "recipes": [
    {
      "id": "1",
      "name": "番茄炒蛋",
      "description": "經典家常菜，簡單易做",
      "ingredients": [
        {
          "name": "番茄",
          "amount": "2個",
          "available": true
        },
        {
          "name": "雞蛋",
          "amount": "3個",
          "available": true
        },
        {
          "name": "蔥",
          "amount": "1根",
          "available": false,
          "substitute": "洋蔥"
        }
      ],
      "steps": [
        "將番茄洗淨，切成小塊備用",
        "將雞蛋打散，加入少許鹽調味"
      ],
      "cooking_time": "15分鐘",
      "difficulty": "簡單",
      "match_percentage": 85
    }
  ],
  "ingredients_used": ["番茄", "雞蛋"]
}
```

#### GET /api/recipes/popular
取得熱門食譜

**回應**:
```json
{
  "success": true,
  "recipes": [
    {
      "id": "1",
      "name": "番茄炒蛋",
      "description": "經典家常菜，簡單易做",
      "cooking_time": 15,
      "difficulty": "easy",
      "image_url": "/images/tomato-egg.jpg"
    }
  ]
}
```

#### POST /api/recipes/feedback
提交食譜回饋

**請求**:
```json
{
  "recipe_id": "1",
  "rating": 5,
  "comment": "很好吃！"
}
```

**參數說明**:
- `recipe_id` (必填): 食譜 ID
- `rating` (必填): 評分 (1-5)
- `comment` (選填): 評論

**回應**:
```json
{
  "success": true,
  "message": "回饋已提交，感謝您的意見！"
}
```

### 食材 API

#### GET /api/ingredients/categories
取得食材分類

**回應**:
```json
{
  "success": true,
  "categories": {
    "vegetables": ["番茄", "洋蔥", "大蒜"],
    "fruits": ["蘋果", "香蕉", "橘子"],
    "meat": ["雞肉", "牛肉", "豬肉"],
    "seafood": ["魚", "蝦子", "螃蟹"],
    "dairy": ["牛奶", "起司", "優格"],
    "grains": ["米飯", "麵包", "麵條"],
    "others": ["雞蛋", "油", "鹽"]
  }
}
```

#### GET /api/ingredients/search
搜尋食材

**請求**:
- **Query Parameters**:
  - `q` (必填): 搜尋關鍵字
  - `category` (選填): 食材分類

**範例**: `/api/ingredients/search?q=番茄&category=vegetables`

**回應**:
```json
{
  "success": true,
  "ingredients": [
    {
      "name": "番茄",
      "category": "vegetables"
    }
  ]
}
```

#### POST /api/ingredients/validate
驗證食材清單

**請求**:
```json
{
  "ingredients": ["番茄", "雞蛋", "未知食材"]
}
```

**回應**:
```json
{
  "success": true,
  "ingredients": [
    {
      "name": "番茄",
      "category": "vegetables",
      "valid": true
    },
    {
      "name": "雞蛋",
      "category": "others",
      "valid": true
    },
    {
      "name": "未知食材",
      "category": "others",
      "valid": false
    }
  ]
}
```

#### POST /api/ingredients/suggest
根據現有食材建議額外食材

**請求**:
```json
{
  "ingredients": ["番茄"]
}
```

**回應**:
```json
{
  "success": true,
  "suggestions": ["雞蛋", "洋蔥", "大蒜", "鹽", "胡椒"]
}
```

#### GET /api/ingredients/nutrition/{ingredient}
取得食材營養資訊

**範例**: `/api/ingredients/nutrition/番茄`

**回應**:
```json
{
  "success": true,
  "nutrition": {
    "name": "番茄",
    "calories_per_100g": 18,
    "protein": 0.9,
    "carbs": 3.9,
    "fat": 0.2,
    "fiber": 1.2,
    "vitamins": ["維生素C", "維生素A"],
    "minerals": ["鉀", "鈣"]
  }
}
```

## 🔧 錯誤處理

### HTTP 狀態碼

- `200 OK`: 請求成功
- `400 Bad Request`: 請求參數錯誤
- `404 Not Found`: 資源不存在
- `413 Payload Too Large`: 檔案過大
- `500 Internal Server Error`: 伺服器內部錯誤

### 錯誤回應格式

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "輸入資料無效",
    "details": {
      "field": "ingredients",
      "reason": "不能為空"
    }
  }
}
```

### 常見錯誤碼

- `VALIDATION_ERROR`: 輸入驗證失敗
- `FILE_TOO_LARGE`: 檔案過大
- `UNSUPPORTED_FORMAT`: 不支援的檔案格式
- `API_QUOTA_EXCEEDED`: API 配額超限
- `DATABASE_ERROR`: 資料庫錯誤
- `VISION_API_ERROR`: 視覺識別 API 錯誤

## 📊 使用限制

### 檔案上傳限制
- **檔案大小**: 最大 16MB
- **支援格式**: JPG, PNG, GIF
- **批次上傳**: 最多 10 張圖片

### API 呼叫限制
- **每分鐘請求數**: 100 次
- **每小時請求數**: 1000 次
- **每日請求數**: 10000 次

### 資料限制
- **食材清單**: 最多 50 個食材
- **搜尋結果**: 最多 20 個食譜
- **回饋評論**: 最多 500 字元

## 🔐 安全性

### HTTPS
所有 API 呼叫都必須使用 HTTPS

### CORS
支援的來源：
- `https://your-frontend-url.vercel.app`
- `http://localhost:3000` (開發環境)

### 資料保護
- 圖片檔案不會永久儲存
- 使用者資料加密傳輸
- 符合 GDPR 規範

## 📈 效能指標

### 回應時間目標
- **健康檢查**: < 100ms
- **食材搜尋**: < 500ms
- **圖片識別**: < 5s
- **食譜推薦**: < 10s

### 可用性
- **目標可用性**: 99.9%
- **維護時間**: 每月最多 4 小時

## 🧪 測試

### 測試環境
- **URL**: `https://test-backend-url.onrender.com/api`
- **資料**: 測試專用資料

### 測試工具
- **Postman**: 匯入 API Collection
- **curl**: 命令列測試
- **Swagger UI**: 互動式 API 文件

## 📞 支援

### 技術支援
- **Email**: support@fridge-saver.com
- **GitHub Issues**: 回報問題
- **文件**: 查看完整文件

### 更新通知
- **版本更新**: 透過 API 版本標頭通知
- **維護通知**: 提前 24 小時通知
- **狀態頁面**: 即時服務狀態

---

**API 版本**: v1.0.0  
**最後更新**: 2024年1月  
**文件維護者**: AI Assistant
