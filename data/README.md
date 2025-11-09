# 冰箱救星 AI 食譜推薦系統 - 資料庫腳本

## 食譜資料庫建立腳本

這個腳本用於建立和填充食譜資料庫，支援 RAG 系統的向量檢索功能。

### 使用方式

```bash
# 安裝依賴
pip install -r requirements.txt

# 執行資料庫建立腳本
python create_recipe_database.py

# 執行向量索引建立腳本
python create_vector_index.py
```

### 資料庫結構

#### recipes 表格
- id: 主鍵
- name: 食譜名稱
- description: 食譜描述
- ingredients: 食材清單 (JSON)
- steps: 製作步驟 (JSON)
- cooking_time: 烹飪時間 (分鐘)
- difficulty: 難度等級
- cuisine: 菜系
- created_at: 建立時間
- updated_at: 更新時間

#### recipe_feedback 表格
- id: 主鍵
- recipe_id: 食譜 ID
- rating: 評分 (1-5)
- comment: 評論
- created_at: 建立時間

### 向量索引

使用 ChromaDB 建立向量索引，支援：
- 食材名稱檢索
- 食譜描述檢索
- 製作步驟檢索
- 多語言支援

### 資料來源

- 公開食譜資料庫
- 使用者貢獻內容
- AI 生成的食譜建議
