# 冰箱救星 AI 食譜推薦系統 - 開發指南

## 🛠️ 開發環境設定

### 前置需求
- Node.js 18+
- Python 3.9+
- PostgreSQL 12+
- Git

### 開發工具推薦
- **IDE**: VS Code, PyCharm
- **資料庫工具**: pgAdmin, DBeaver
- **API 測試**: Postman, Insomnia
- **版本控制**: Git

## 📁 專案架構說明

### 前端架構 (React + TypeScript)
```
frontend/src/
├── components/          # 可重用組件
│   ├── Header.tsx     # 導航列
│   ├── Loading.tsx    # 載入組件
│   └── ...
├── pages/             # 頁面組件
│   ├── HomePage.tsx   # 首頁
│   ├── UploadPage.tsx # 上傳頁面
│   ├── RecipesPage.tsx # 食譜列表
│   └── RecipeDetailPage.tsx # 食譜詳情
├── services/          # API 服務
│   └── api.ts        # API 客戶端
├── types/            # TypeScript 類型定義
├── utils/            # 工具函數
└── hooks/            # 自定義 Hooks
```

### 後端架構 (Flask + Python)
```
backend/
├── routes/           # API 路由
│   ├── vision.py    # 視覺識別 API
│   ├── recipes.py   # 食譜 API
│   └── ingredients.py # 食材 API
├── models/          # 資料模型
├── services/        # 業務邏輯
├── utils/           # 工具函數
├── config/          # 配置檔案
└── app.py          # 主應用程式
```

## 🔧 開發工作流程

### 1. 功能開發
1. 建立功能分支
2. 實作功能
3. 撰寫測試
4. 提交變更
5. 建立 Pull Request

### 2. 程式碼規範
- 使用 ESLint 和 Prettier
- 遵循 TypeScript 最佳實踐
- 撰寫清晰的註解
- 使用有意義的變數名稱

### 3. 測試策略
- 單元測試 (Jest)
- 整合測試
- E2E 測試 (Cypress)

## 📊 API 設計原則

### RESTful API 設計
- 使用適當的 HTTP 方法
- 清晰的 URL 結構
- 統一的回應格式
- 適當的狀態碼

### 回應格式
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 錯誤處理
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "輸入資料無效",
    "details": {...}
  }
}
```

## 🧠 AI 服務整合

### Google Vision API
```python
from google.cloud import vision

def analyze_image(image_content):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    return process_labels(labels)
```

### OpenAI GPT API
```python
import openai

def generate_recipe(ingredients, retrieved_recipes):
    prompt = create_recipe_prompt(ingredients, retrieved_recipes)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是專業廚師"},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content
```

### RAG 實作
```python
import chromadb
from sentence_transformers import SentenceTransformer

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient()
        self.collection = self.client.get_collection("recipes")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def retrieve(self, query, n_results=5):
        query_embedding = self.embedding_model.encode([query])
        
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )
        
        return results
    
    def generate(self, query, retrieved_docs):
        # 使用 LLM 生成最終回應
        pass
```

## 🗄️ 資料庫設計

### 食譜表格
```sql
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    ingredients JSONB NOT NULL,
    steps JSONB NOT NULL,
    cooking_time INTEGER NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    cuisine VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 回饋表格
```sql
CREATE TABLE recipe_feedback (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 前端開發最佳實踐

### 組件設計
```typescript
interface RecipeCardProps {
  recipe: Recipe;
  onSelect: (recipe: Recipe) => void;
  className?: string;
}

const RecipeCard: React.FC<RecipeCardProps> = ({
  recipe,
  onSelect,
  className
}) => {
  return (
    <div className={clsx('recipe-card', className)}>
      {/* 組件內容 */}
    </div>
  );
};
```

### 狀態管理
```typescript
// 使用 React Query 管理伺服器狀態
const { data: recipes, isLoading, error } = useQuery(
  'recipes',
  () => searchRecipes(ingredients),
  {
    enabled: ingredients.length > 0,
    staleTime: 5 * 60 * 1000, // 5分鐘
  }
);
```

### 錯誤處理
```typescript
const handleError = (error: Error) => {
  console.error('API Error:', error);
  toast.error('操作失敗，請重試');
};
```

## 🧪 測試撰寫

### 前端測試
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import RecipeCard from './RecipeCard';

describe('RecipeCard', () => {
  it('renders recipe information correctly', () => {
    const mockRecipe = {
      id: '1',
      name: '番茄炒蛋',
      description: '經典家常菜',
      // ... 其他屬性
    };
    
    render(<RecipeCard recipe={mockRecipe} onSelect={jest.fn()} />);
    
    expect(screen.getByText('番茄炒蛋')).toBeInTheDocument();
    expect(screen.getByText('經典家常菜')).toBeInTheDocument();
  });
});
```

### 後端測試
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'
```

## 🚀 效能優化

### 前端優化
- 使用 React.memo 避免不必要的重渲染
- 實作虛擬滾動處理大量資料
- 使用圖片懶載入
- 實作程式碼分割

### 後端優化
- 使用資料庫連線池
- 實作快取機制
- 優化資料庫查詢
- 使用非同步處理

## 🔍 除錯技巧

### 前端除錯
- 使用 React Developer Tools
- 檢查 Network 標籤
- 使用 console.log 追蹤狀態
- 檢查瀏覽器控制台錯誤

### 後端除錯
- 使用 logging 模組
- 檢查資料庫查詢
- 使用除錯器
- 監控 API 回應時間

## 📚 學習資源

### React 開發
- [React 官方文件](https://reactjs.org/docs)
- [TypeScript 手冊](https://www.typescriptlang.org/docs)
- [Tailwind CSS 文件](https://tailwindcss.com/docs)

### Python 開發
- [Flask 文件](https://flask.palletsprojects.com/)
- [SQLAlchemy 文件](https://docs.sqlalchemy.org/)
- [Python 最佳實踐](https://docs.python-guide.org/)

### AI 開發
- [LangChain 文件](https://python.langchain.com/)
- [ChromaDB 文件](https://docs.trychroma.com/)
- [OpenAI API 文件](https://platform.openai.com/docs)

## 🤝 貢獻指南

1. Fork 專案
2. 建立功能分支
3. 實作功能並撰寫測試
4. 提交變更
5. 建立 Pull Request

### 提交訊息規範
```
feat: 新增食材識別功能
fix: 修復食譜搜尋錯誤
docs: 更新 API 文件
style: 調整程式碼格式
refactor: 重構 RAG 服務
test: 新增單元測試
```

## 📞 技術支援

- 建立 [Issue](../../issues) 回報問題
- 查看 [Wiki](../../wiki) 獲取更多資訊
- 參與 [Discussions](../../discussions) 討論

