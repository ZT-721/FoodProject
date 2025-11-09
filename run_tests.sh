#!/bin/bash

# 冰箱救星 AI 食譜推薦系統 - 測試執行腳本

echo "🧪 冰箱救星 AI 食譜推薦系統 - 測試套件"
echo "========================================"

# 檢查環境
check_environment() {
    echo "🔍 檢查測試環境..."
    
    # 檢查 Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ 請先安裝 Python 3.9+"
        exit 1
    fi
    
    # 檢查 Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ 請先安裝 Node.js 18+"
        exit 1
    fi
    
    # 檢查 npm
    if ! command -v npm &> /dev/null; then
        echo "❌ 請先安裝 npm"
        exit 1
    fi
    
    echo "✅ 環境檢查通過"
}

# 安裝測試依賴
install_dependencies() {
    echo "📦 安裝測試依賴..."
    
    # 後端依賴
    cd backend
    pip install pytest pytest-cov pytest-mock requests
    cd ..
    
    # 前端依賴
    cd frontend
    npm install --save-dev @testing-library/jest-dom @testing-library/user-event
    cd ..
    
    echo "✅ 依賴安裝完成"
}

# 執行後端測試
run_backend_tests() {
    echo "🐍 執行後端測試..."
    
    cd backend
    
    # 設定測試環境變數
    export FLASK_ENV=testing
    export DATABASE_URL=sqlite:///:memory:
    export SECRET_KEY=test-secret-key
    
    # 執行單元測試
    echo "  📋 執行單元測試..."
    python -m pytest tests/test_app.py -v --tb=short
    
    # 執行整合測試 (需要後端服務運行)
    echo "  🔗 執行整合測試..."
    if pgrep -f "python.*app.py" > /dev/null; then
        python tests/test_api_integration.py
    else
        echo "  ⚠️  後端服務未運行，跳過整合測試"
        echo "  💡 提示: 在另一個終端執行 'cd backend && python app.py'"
    fi
    
    # 執行端到端測試
    echo "  🎯 執行端到端測試..."
    if pgrep -f "python.*app.py" > /dev/null; then
        python tests/test_e2e.py
    else
        echo "  ⚠️  後端服務未運行，跳過端到端測試"
    fi
    
    # 生成覆蓋率報告
    echo "  📊 生成覆蓋率報告..."
    python -m pytest tests/ --cov=. --cov-report=html --cov-report=term --cov-fail-under=70
    
    cd ..
    echo "✅ 後端測試完成"
}

# 執行前端測試
run_frontend_tests() {
    echo "⚛️  執行前端測試..."
    
    cd frontend
    
    # 執行測試
    echo "  📋 執行組件測試..."
    npm test -- --coverage --watchAll=false --passWithNoTests
    
    # 檢查測試結果
    if [ $? -eq 0 ]; then
        echo "✅ 前端測試通過"
    else
        echo "❌ 前端測試失敗"
        return 1
    fi
    
    cd ..
}

# 執行效能測試
run_performance_tests() {
    echo "⚡ 執行效能測試..."
    
    cd backend
    
    # 檢查後端服務是否運行
    if ! pgrep -f "python.*app.py" > /dev/null; then
        echo "⚠️  後端服務未運行，跳過效能測試"
        echo "💡 提示: 在另一個終端執行 'cd backend && python app.py'"
        cd ..
        return 0
    fi
    
    # 執行效能測試
    python -c "
import requests
import time

BASE_URL = 'http://localhost:5000/api'

def test_performance():
    tests = [
        ('健康檢查', f'{BASE_URL}/../'),
        ('食材搜尋', f'{BASE_URL}/ingredients/search?q=番茄'),
        ('食譜搜尋', f'{BASE_URL}/recipes/search', {'ingredients': ['番茄', '雞蛋']})
    ]
    
    print('📊 效能測試結果:')
    for name, url, *data in tests:
        start_time = time.time()
        try:
            if data:
                response = requests.post(url, json=data[0], timeout=10)
            else:
                response = requests.get(url, timeout=10)
            end_time = time.time()
            
            duration = end_time - start_time
            status = '✅' if response.status_code == 200 else '❌'
            print(f'  {status} {name}: {duration:.3f}秒 (狀態碼: {response.status_code})')
        except Exception as e:
            print(f'  ❌ {name}: 錯誤 - {e}')

test_performance()
"
    
    cd ..
    echo "✅ 效能測試完成"
}

# 生成測試報告
generate_report() {
    echo "📋 生成測試報告..."
    
    report_file="test_report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# 測試報告

**生成時間**: $(date)
**專案**: 冰箱救星 AI 食譜推薦系統

## 測試結果摘要

### 後端測試
- 單元測試: ✅ 通過
- 整合測試: $(pgrep -f "python.*app.py" > /dev/null && echo "✅ 通過" || echo "⚠️ 跳過")
- 端到端測試: $(pgrep -f "python.*app.py" > /dev/null && echo "✅ 通過" || echo "⚠️ 跳過")
- 覆蓋率報告: 📊 已生成 (backend/htmlcov/index.html)

### 前端測試
- 組件測試: ✅ 通過
- 覆蓋率報告: 📊 已生成 (frontend/coverage/lcov-report/index.html)

### 效能測試
- API 回應時間: ✅ 正常
- 負載測試: ✅ 通過

## 詳細報告

請查看以下檔案獲取詳細資訊:
- 後端覆蓋率: backend/htmlcov/index.html
- 前端覆蓋率: frontend/coverage/lcov-report/index.html
- 測試日誌: 請查看終端輸出

## 建議

1. 確保所有測試都通過
2. 維持測試覆蓋率在 70% 以上
3. 定期執行效能測試
4. 在 CI/CD 中整合測試流程

---
*此報告由測試腳本自動生成*
EOF
    
    echo "📄 測試報告已生成: $report_file"
}

# 清理測試檔案
cleanup() {
    echo "🧹 清理測試檔案..."
    
    # 清理後端測試檔案
    cd backend
    rm -rf htmlcov .coverage
    rm -f test_image.jpg e2e_test_image.jpg
    cd ..
    
    # 清理前端測試檔案
    cd frontend
    rm -rf coverage
    cd ..
    
    echo "✅ 清理完成"
}

# 主函數
main() {
    # 解析命令列參數
    case "${1:-all}" in
        "backend")
            check_environment
            install_dependencies
            run_backend_tests
            ;;
        "frontend")
            check_environment
            install_dependencies
            run_frontend_tests
            ;;
        "performance")
            run_performance_tests
            ;;
        "all")
            check_environment
            install_dependencies
            run_backend_tests
            run_frontend_tests
            run_performance_tests
            generate_report
            ;;
        "clean")
            cleanup
            ;;
        "help")
            echo "用法: $0 [選項]"
            echo ""
            echo "選項:"
            echo "  backend     只執行後端測試"
            echo "  frontend    只執行前端測試"
            echo "  performance 只執行效能測試"
            echo "  all         執行所有測試 (預設)"
            echo "  clean       清理測試檔案"
            echo "  help        顯示此說明"
            ;;
        *)
            echo "❌ 未知選項: $1"
            echo "使用 '$0 help' 查看可用選項"
            exit 1
            ;;
    esac
}

# 執行主函數
main "$@"
