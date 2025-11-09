# 冰箱救星 AI 食譜推薦系統 - 測試指南

## 🧪 測試概述

本專案包含完整的測試套件，涵蓋單元測試、整合測試和端到端測試，確保系統的穩定性和可靠性。

## 📁 測試結構

```
tests/
├── backend/
│   ├── test_app.py              # 後端單元測試
│   ├── test_api_integration.py   # API 整合測試
│   └── test_e2e.py             # 端到端測試
├── frontend/
│   └── src/__tests__/
│       ├── App.test.tsx         # 前端組件測試
│       └── UploadPage.test.tsx  # 上傳頁面測試
└── docs/
    └── testing-guide.md         # 測試指南
```

## 🚀 快速開始

### 前置需求

1. **後端測試**：
   - Python 3.9+
   - pytest
   - PostgreSQL (測試用)

2. **前端測試**：
   - Node.js 18+
   - Jest
   - React Testing Library

### 安裝測試依賴

```bash
# 後端測試依賴
cd backend
pip install pytest pytest-cov pytest-mock

# 前端測試依賴
cd frontend
npm install --save-dev @testing-library/jest-dom @testing-library/user-event
```

## 🔧 執行測試

### 後端測試

#### 1. 單元測試
```bash
cd backend
python -m pytest tests/test_app.py -v
```

#### 2. 整合測試
```bash
# 確保後端服務運行
python app.py &

# 執行整合測試
python tests/test_api_integration.py
```

#### 3. 端到端測試
```bash
# 確保後端服務運行
python app.py &

# 執行 E2E 測試
python tests/test_e2e.py
```

#### 4. 所有測試
```bash
# 執行所有測試並生成覆蓋率報告
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### 前端測試

#### 1. 執行所有測試
```bash
cd frontend
npm test
```

#### 2. 生成覆蓋率報告
```bash
npm run test:coverage
```

#### 3. CI 環境測試
```bash
npm run test:ci
```

## 📊 測試類型

### 1. 單元測試 (Unit Tests)

**目的**：測試個別函數和組件的功能

**範圍**：
- API 端點功能
- 工具函數
- React 組件渲染
- 狀態管理

**範例**：
```python
def test_health_check(client):
    """測試健康檢查端點"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
```

### 2. 整合測試 (Integration Tests)

**目的**：測試多個組件協同工作

**範圍**：
- API 端點之間的互動
- 資料庫操作
- 外部 API 整合
- 前後端通訊

**範例**：
```python
def test_complete_workflow():
    """測試完整工作流程"""
    # 1. 上傳圖片
    # 2. 識別食材
    # 3. 搜尋食譜
    # 4. 提交回饋
```

### 3. 端到端測試 (E2E Tests)

**目的**：測試完整的用戶旅程

**範圍**：
- 用戶從上傳圖片到獲得食譜的完整流程
- 跨瀏覽器相容性
- 效能基準測試
- 錯誤處理

## 🎯 測試覆蓋率

### 目標覆蓋率
- **程式碼覆蓋率**：≥ 70%
- **分支覆蓋率**：≥ 70%
- **函數覆蓋率**：≥ 70%

### 查看覆蓋率報告
```bash
# 後端覆蓋率
cd backend
python -m pytest --cov=. --cov-report=html
open htmlcov/index.html

# 前端覆蓋率
cd frontend
npm run test:coverage
open coverage/lcov-report/index.html
```

## 🔍 測試最佳實踐

### 1. 測試命名
- 使用描述性的測試名稱
- 遵循 `test_功能_條件_預期結果` 格式

### 2. 測試結構
- **Arrange**：準備測試資料
- **Act**：執行被測試的功能
- **Assert**：驗證結果

### 3. Mock 使用
- Mock 外部 API 呼叫
- Mock 檔案系統操作
- Mock 時間相關函數

### 4. 測試資料
- 使用固定的測試資料
- 避免依賴外部服務
- 清理測試產生的資料

## 🚨 常見問題

### 1. 測試失敗

**問題**：API 測試失敗
```bash
❌ 無法連接到後端服務
```

**解決方案**：
```bash
# 確保後端服務運行
cd backend
python app.py
```

### 2. 資料庫連線問題

**問題**：測試資料庫連線失敗

**解決方案**：
```bash
# 檢查環境變數
echo $DATABASE_URL

# 使用記憶體資料庫進行測試
export DATABASE_URL="sqlite:///:memory:"
```

### 3. 前端測試環境問題

**問題**：React 測試環境設定錯誤

**解決方案**：
```bash
# 重新安裝依賴
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📈 持續整合

### GitHub Actions 範例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          python -m pytest tests/ --cov=. --cov-report=xml

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: 18
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm run test:ci
```

## 🔧 測試工具

### 後端測試工具
- **pytest**：測試框架
- **pytest-cov**：覆蓋率報告
- **pytest-mock**：Mock 功能
- **requests**：HTTP 測試

### 前端測試工具
- **Jest**：測試框架
- **React Testing Library**：React 組件測試
- **@testing-library/user-event**：用戶互動測試
- **@testing-library/jest-dom**：DOM 斷言

## 📚 進階測試

### 1. 效能測試
```python
def test_api_performance():
    """測試 API 效能"""
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/health")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 1.0  # 1秒內回應
```

### 2. 負載測試
```python
def test_concurrent_requests():
    """測試並發請求"""
    import concurrent.futures
    
    def make_request():
        return requests.get(f"{BASE_URL}/health")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in futures]
    
    assert all(r.status_code == 200 for r in results)
```

### 3. 安全測試
```python
def test_sql_injection():
    """測試 SQL 注入防護"""
    malicious_input = "'; DROP TABLE recipes; --"
    response = requests.post(f"{BASE_URL}/recipes/search",
                           json={'ingredients': [malicious_input]})
    
    # 應該正常處理，不應該導致錯誤
    assert response.status_code in [200, 400]
```

## 📞 測試支援

### 除錯技巧
1. **增加日誌輸出**：在測試中添加 `print` 語句
2. **使用斷點**：在 IDE 中設定斷點
3. **檢查測試資料**：確認測試資料正確性
4. **隔離測試**：一次只執行一個測試

### 獲取幫助
- 查看測試日誌
- 檢查測試覆蓋率報告
- 參考測試範例
- 建立 Issue 回報問題

---

**記住**：好的測試是軟體品質的基石！ 🧪✨
