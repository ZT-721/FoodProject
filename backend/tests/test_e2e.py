#!/usr/bin/env python3
"""
端到端測試腳本
測試完整的用戶工作流程
"""

import requests
import json
import time
import os
import tempfile
from pathlib import Path

# API 基礎 URL
BASE_URL = "http://localhost:5000/api"

class E2ETestSuite:
    """端到端測試套件"""
    
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.test_image_path = None
    
    def create_test_image(self):
        """建立測試圖片"""
        # 建立一個簡單的測試圖片 (1x1 像素的 JPEG)
        test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        
        self.test_image_path = 'e2e_test_image.jpg'
        with open(self.test_image_path, 'wb') as f:
            f.write(test_image_data)
        
        return self.test_image_path
    
    def cleanup(self):
        """清理測試檔案"""
        if self.test_image_path and os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
    
    def run_test(self, test_name, test_func):
        """執行單個測試"""
        print(f"\n🔍 執行測試: {test_name}")
        start_time = time.time()
        
        try:
            result = test_func()
            end_time = time.time()
            duration = end_time - start_time
            
            if result:
                print(f"✅ {test_name} 通過 ({duration:.2f}秒)")
                self.test_results.append((test_name, True, duration))
            else:
                print(f"❌ {test_name} 失敗 ({duration:.2f}秒)")
                self.test_results.append((test_name, False, duration))
                
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"❌ {test_name} 異常: {e} ({duration:.2f}秒)")
            self.test_results.append((test_name, False, duration))
    
    def test_service_availability(self):
        """測試服務可用性"""
        try:
            response = self.session.get(f"{BASE_URL}/../", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def test_health_endpoints(self):
        """測試健康檢查端點"""
        # 測試主健康檢查
        response = self.session.get(f"{BASE_URL}/../")
        if response.status_code != 200:
            return False
        
        # 測試 API 健康檢查
        response = self.session.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            return False
        
        data = response.json()
        return data.get('status') == 'ok'
    
    def test_ingredients_workflow(self):
        """測試食材相關工作流程"""
        # 1. 取得食材分類
        response = self.session.get(f"{BASE_URL}/ingredients/categories")
        if response.status_code != 200:
            return False
        
        data = response.json()
        if not data.get('success') or 'categories' not in data:
            return False
        
        # 2. 搜尋食材
        response = self.session.get(f"{BASE_URL}/ingredients/search?q=番茄")
        if response.status_code != 200:
            return False
        
        data = response.json()
        if not data.get('success') or 'ingredients' not in data:
            return False
        
        # 3. 驗證食材
        response = self.session.post(f"{BASE_URL}/ingredients/validate",
                                   json={'ingredients': ['番茄', '雞蛋']})
        if response.status_code != 200:
            return False
        
        data = response.json()
        if not data.get('success') or len(data.get('ingredients', [])) != 2:
            return False
        
        # 4. 建議食材
        response = self.session.post(f"{BASE_URL}/ingredients/suggest",
                                   json={'ingredients': ['番茄']})
        if response.status_code != 200:
            return False
        
        data = response.json()
        return data.get('success') and 'suggestions' in data
    
    def test_vision_api_workflow(self):
        """測試視覺識別 API 工作流程"""
        # 建立測試圖片
        image_path = self.create_test_image()
        
        try:
            # 1. 單張圖片上傳
            with open(image_path, 'rb') as f:
                files = {'file': ('test.jpg', f, 'image/jpeg')}
                response = self.session.post(f"{BASE_URL}/vision/upload", files=files)
            
            if response.status_code != 200:
                return False
            
            data = response.json()
            if not data.get('success') or 'ingredients' not in data:
                return False
            
            # 2. 批次上傳
            with open(image_path, 'rb') as f1, open(image_path, 'rb') as f2:
                files = [
                    ('files', ('test1.jpg', f1, 'image/jpeg')),
                    ('files', ('test2.jpg', f2, 'image/jpeg'))
                ]
                response = self.session.post(f"{BASE_URL}/vision/batch-upload", files=files)
            
            if response.status_code != 200:
                return False
            
            data = response.json()
            return data.get('success') and data.get('total_images') == 2
            
        finally:
            # 清理測試檔案
            if os.path.exists(image_path):
                os.remove(image_path)
    
    def test_recipes_workflow(self):
        """測試食譜相關工作流程"""
        # 1. 搜尋食譜
        response = self.session.post(f"{BASE_URL}/recipes/search",
                                   json={
                                       'ingredients': ['番茄', '雞蛋'],
                                       'preferences': {
                                           'cooking_time': '30',
                                           'difficulty': '簡單'
                                       }
                                   })
        
        if response.status_code != 200:
            return False
        
        data = response.json()
        if not data.get('success') or 'recipes' not in data:
            return False
        
        recipes = data.get('recipes', [])
        if not recipes:
            return False
        
        # 2. 取得熱門食譜
        response = self.session.get(f"{BASE_URL}/recipes/popular")
        if response.status_code != 200:
            return False
        
        data = response.json()
        if not data.get('success') or 'recipes' not in data:
            return False
        
        # 3. 提交回饋
        recipe_id = recipes[0].get('id', '1')
        response = self.session.post(f"{BASE_URL}/recipes/feedback",
                                   json={
                                       'recipe_id': recipe_id,
                                       'rating': 5,
                                       'comment': 'E2E 測試回饋'
                                   })
        
        if response.status_code != 200:
            return False
        
        data = response.json()
        return data.get('success')
    
    def test_complete_user_journey(self):
        """測試完整用戶旅程"""
        try:
            # 1. 上傳圖片並識別食材
            image_path = self.create_test_image()
            
            with open(image_path, 'rb') as f:
                files = {'file': ('test.jpg', f, 'image/jpeg')}
                response = self.session.post(f"{BASE_URL}/vision/upload", files=files)
            
            if response.status_code != 200:
                return False
            
            vision_data = response.json()
            if not vision_data.get('success'):
                return False
            
            ingredients = [ing['name'] for ing in vision_data.get('ingredients', [])]
            if not ingredients:
                # 如果沒有識別到食材，使用預設食材
                ingredients = ['番茄', '雞蛋']
            
            # 2. 根據食材搜尋食譜
            response = self.session.post(f"{BASE_URL}/recipes/search",
                                       json={'ingredients': ingredients[:3]})
            
            if response.status_code != 200:
                return False
            
            recipes_data = response.json()
            if not recipes_data.get('success'):
                return False
            
            recipes = recipes_data.get('recipes', [])
            if not recipes:
                return False
            
            # 3. 對第一個食譜提交回饋
            recipe_id = recipes[0].get('id', '1')
            response = self.session.post(f"{BASE_URL}/recipes/feedback",
                                       json={
                                           'recipe_id': recipe_id,
                                           'rating': 4,
                                           'comment': '完整流程測試回饋'
                                       })
            
            if response.status_code != 200:
                return False
            
            feedback_data = response.json()
            return feedback_data.get('success')
            
        finally:
            # 清理測試檔案
            if os.path.exists(image_path):
                os.remove(image_path)
    
    def test_error_handling(self):
        """測試錯誤處理"""
        # 1. 測試無效的 JSON
        response = self.session.post(f"{BASE_URL}/recipes/search",
                                   data='invalid json',
                                   headers={'Content-Type': 'application/json'})
        if response.status_code != 400:
            return False
        
        # 2. 測試缺少必要參數
        response = self.session.post(f"{BASE_URL}/recipes/search",
                                   json={})
        if response.status_code != 400:
            return False
        
        # 3. 測試無效的搜尋查詢
        response = self.session.get(f"{BASE_URL}/ingredients/search")
        if response.status_code != 400:
            return False
        
        return True
    
    def test_performance_benchmarks(self):
        """測試效能基準"""
        benchmarks = []
        
        # 健康檢查效能
        start_time = time.time()
        response = self.session.get(f"{BASE_URL}/../")
        end_time = time.time()
        
        if response.status_code == 200:
            benchmarks.append(('健康檢查', end_time - start_time))
        
        # 食材搜尋效能
        start_time = time.time()
        response = self.session.get(f"{BASE_URL}/ingredients/search?q=番茄")
        end_time = time.time()
        
        if response.status_code == 200:
            benchmarks.append(('食材搜尋', end_time - start_time))
        
        # 食譜搜尋效能
        start_time = time.time()
        response = self.session.post(f"{BASE_URL}/recipes/search",
                                   json={'ingredients': ['番茄', '雞蛋']})
        end_time = time.time()
        
        if response.status_code == 200:
            benchmarks.append(('食譜搜尋', end_time - start_time))
        
        # 檢查效能基準
        for test_name, duration in benchmarks:
            if duration > 5.0:  # 超過 5 秒視為效能問題
                print(f"⚠️  {test_name} 回應時間過長: {duration:.2f}秒")
                return False
        
        return True
    
    def run_all_tests(self):
        """執行所有測試"""
        print("🍔 冰箱救星 AI 食譜推薦系統 - 端到端測試")
        print("=" * 60)
        
        # 檢查服務可用性
        if not self.test_service_availability():
            print("❌ 服務不可用，請先啟動後端服務")
            print("執行: cd backend && python app.py")
            return False
        
        # 定義測試套件
        tests = [
            ("服務可用性", self.test_service_availability),
            ("健康檢查端點", self.test_health_endpoints),
            ("食材工作流程", self.test_ingredients_workflow),
            ("視覺識別工作流程", self.test_vision_api_workflow),
            ("食譜工作流程", self.test_recipes_workflow),
            ("完整用戶旅程", self.test_complete_user_journey),
            ("錯誤處理", self.test_error_handling),
            ("效能基準", self.test_performance_benchmarks),
        ]
        
        # 執行測試
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # 生成測試報告
        self.generate_report()
        
        # 清理
        self.cleanup()
        
        return self.get_success_rate() >= 0.8  # 80% 通過率
    
    def generate_report(self):
        """生成測試報告"""
        print("\n" + "=" * 60)
        print("📊 測試報告")
        print("=" * 60)
        
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        success_rate = passed / total if total > 0 else 0
        
        print(f"總測試數: {total}")
        print(f"通過數: {passed}")
        print(f"失敗數: {total - passed}")
        print(f"通過率: {success_rate:.1%}")
        
        print("\n詳細結果:")
        for test_name, success, duration in self.test_results:
            status = "✅ 通過" if success else "❌ 失敗"
            print(f"  {test_name}: {status} ({duration:.2f}秒)")
        
        if success_rate >= 0.8:
            print("\n🎉 測試通過！系統運行正常")
        else:
            print("\n⚠️  測試未完全通過，請檢查相關功能")
    
    def get_success_rate(self):
        """取得成功率"""
        if not self.test_results:
            return 0
        passed = sum(1 for _, success, _ in self.test_results if success)
        return passed / len(self.test_results)

def main():
    """主函數"""
    test_suite = E2ETestSuite()
    
    try:
        success = test_suite.run_all_tests()
        exit_code = 0 if success else 1
        return exit_code
    except KeyboardInterrupt:
        print("\n\n⚠️  測試被中斷")
        test_suite.cleanup()
        return 1
    except Exception as e:
        print(f"\n\n❌ 測試執行異常: {e}")
        test_suite.cleanup()
        return 1

if __name__ == "__main__":
    exit(main())
