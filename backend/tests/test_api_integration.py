#!/usr/bin/env python3
"""
API 整合測試腳本
測試完整的 API 流程
"""

import requests
import json
import time
import os
from pathlib import Path

# API 基礎 URL
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """測試健康檢查"""
    print("🔍 測試健康檢查...")
    
    try:
        response = requests.get(f"{BASE_URL}/../")
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'healthy'
        print("✅ 健康檢查通過")
        return True
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}")
        return False

def test_ingredients_api():
    """測試食材 API"""
    print("\n🔍 測試食材 API...")
    
    try:
        # 測試取得分類
        response = requests.get(f"{BASE_URL}/ingredients/categories")
        assert response.status_code == 200
        data = response.json()
        assert 'categories' in data
        print("✅ 取得食材分類成功")
        
        # 測試搜尋食材
        response = requests.get(f"{BASE_URL}/ingredients/search?q=番茄")
        assert response.status_code == 200
        data = response.json()
        assert 'ingredients' in data
        print("✅ 搜尋食材成功")
        
        # 測試驗證食材
        response = requests.post(f"{BASE_URL}/ingredients/validate",
                               json={'ingredients': ['番茄', '雞蛋']})
        assert response.status_code == 200
        data = response.json()
        assert len(data['ingredients']) == 2
        print("✅ 驗證食材成功")
        
        # 測試建議食材
        response = requests.post(f"{BASE_URL}/ingredients/suggest",
                               json={'ingredients': ['番茄']})
        assert response.status_code == 200
        data = response.json()
        assert 'suggestions' in data
        print("✅ 建議食材成功")
        
        return True
    except Exception as e:
        print(f"❌ 食材 API 測試失敗: {e}")
        return False

def test_recipes_api():
    """測試食譜 API"""
    print("\n🔍 測試食譜 API...")
    
    try:
        # 測試搜尋食譜
        response = requests.post(f"{BASE_URL}/recipes/search",
                               json={
                                   'ingredients': ['番茄', '雞蛋'],
                                   'preferences': {
                                       'cooking_time': '30',
                                       'difficulty': '簡單'
                                   }
                               })
        assert response.status_code == 200
        data = response.json()
        assert 'recipes' in data
        print("✅ 搜尋食譜成功")
        
        # 測試取得熱門食譜
        response = requests.get(f"{BASE_URL}/recipes/popular")
        assert response.status_code == 200
        data = response.json()
        assert 'recipes' in data
        print("✅ 取得熱門食譜成功")
        
        # 測試提交回饋
        response = requests.post(f"{BASE_URL}/recipes/feedback",
                               json={
                                   'recipe_id': '1',
                                   'rating': 5,
                                   'comment': '測試回饋'
                               })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        print("✅ 提交回饋成功")
        
        return True
    except Exception as e:
        print(f"❌ 食譜 API 測試失敗: {e}")
        return False

def test_vision_api():
    """測試視覺識別 API"""
    print("\n🔍 測試視覺識別 API...")
    
    try:
        # 建立測試圖片檔案
        test_image_path = create_test_image()
        
        # 測試單張圖片上傳
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test.jpg', f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/vision/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert 'ingredients' in data
        print("✅ 單張圖片上傳成功")
        
        # 測試批次上傳
        with open(test_image_path, 'rb') as f1, open(test_image_path, 'rb') as f2:
            files = [
                ('files', ('test1.jpg', f1, 'image/jpeg')),
                ('files', ('test2.jpg', f2, 'image/jpeg'))
            ]
            response = requests.post(f"{BASE_URL}/vision/batch-upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data['total_images'] == 2
        print("✅ 批次圖片上傳成功")
        
        # 清理測試檔案
        os.remove(test_image_path)
        
        return True
    except Exception as e:
        print(f"❌ 視覺識別 API 測試失敗: {e}")
        return False

def create_test_image():
    """建立測試圖片檔案"""
    # 建立一個簡單的測試圖片 (1x1 像素的 JPEG)
    test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    test_image_path = 'test_image.jpg'
    with open(test_image_path, 'wb') as f:
        f.write(test_image_data)
    
    return test_image_path

def test_complete_workflow():
    """測試完整工作流程"""
    print("\n🔍 測試完整工作流程...")
    
    try:
        # 1. 上傳圖片並識別食材
        test_image_path = create_test_image()
        
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test.jpg', f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/vision/upload", files=files)
        
        assert response.status_code == 200
        vision_data = response.json()
        ingredients = [ing['name'] for ing in vision_data['ingredients']]
        print(f"✅ 識別到食材: {ingredients}")
        
        # 2. 根據食材搜尋食譜
        if ingredients:
            response = requests.post(f"{BASE_URL}/recipes/search",
                                   json={'ingredients': ingredients[:3]})
            
            assert response.status_code == 200
            recipes_data = response.json()
            recipes = recipes_data['recipes']
            print(f"✅ 找到 {len(recipes)} 個推薦食譜")
            
            # 3. 對第一個食譜提交回饋
            if recipes:
                recipe_id = recipes[0].get('id', '1')
                response = requests.post(f"{BASE_URL}/recipes/feedback",
                                       json={
                                           'recipe_id': recipe_id,
                                           'rating': 4,
                                           'comment': '自動測試回饋'
                                       })
                
                assert response.status_code == 200
                print("✅ 提交回饋成功")
        
        # 清理測試檔案
        os.remove(test_image_path)
        
        return True
    except Exception as e:
        print(f"❌ 完整工作流程測試失敗: {e}")
        return False

def test_error_handling():
    """測試錯誤處理"""
    print("\n🔍 測試錯誤處理...")
    
    try:
        # 測試無效的 JSON
        response = requests.post(f"{BASE_URL}/recipes/search",
                               data='invalid json',
                               headers={'Content-Type': 'application/json'})
        assert response.status_code == 400
        print("✅ 無效 JSON 處理正確")
        
        # 測試缺少必要參數
        response = requests.post(f"{BASE_URL}/recipes/search",
                               json={})
        assert response.status_code == 400
        print("✅ 缺少參數處理正確")
        
        # 測試無效的搜尋查詢
        response = requests.get(f"{BASE_URL}/ingredients/search")
        assert response.status_code == 400
        print("✅ 無效查詢處理正確")
        
        return True
    except Exception as e:
        print(f"❌ 錯誤處理測試失敗: {e}")
        return False

def test_performance():
    """測試效能"""
    print("\n🔍 測試 API 效能...")
    
    try:
        # 測試健康檢查回應時間
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/../")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 1.0  # 應該在 1 秒內回應
        print(f"✅ 健康檢查回應時間: {response_time:.3f}秒")
        
        # 測試食材搜尋效能
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/ingredients/search?q=番茄")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 2.0  # 應該在 2 秒內回應
        print(f"✅ 食材搜尋回應時間: {response_time:.3f}秒")
        
        return True
    except Exception as e:
        print(f"❌ 效能測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🍔 冰箱救星 AI 食譜推薦系統 - API 整合測試")
    print("=" * 50)
    
    # 檢查服務是否運行
    try:
        response = requests.get(f"{BASE_URL}/../", timeout=5)
        if response.status_code != 200:
            print("❌ 後端服務未運行，請先啟動後端服務")
            print("執行: cd backend && python app.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到後端服務")
        print("請確保後端服務正在運行: cd backend && python app.py")
        return
    
    # 執行測試
    tests = [
        ("健康檢查", test_health_check),
        ("食材 API", test_ingredients_api),
        ("食譜 API", test_recipes_api),
        ("視覺識別 API", test_vision_api),
        ("完整工作流程", test_complete_workflow),
        ("錯誤處理", test_error_handling),
        ("效能測試", test_performance),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {e}")
    
    print("\n" + "=" * 50)
    print(f"測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！系統運行正常")
    else:
        print("⚠️  部分測試失敗，請檢查相關功能")
    
    return passed == total

if __name__ == "__main__":
    main()
