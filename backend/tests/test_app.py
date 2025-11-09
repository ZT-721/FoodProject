#!/usr/bin/env python3
"""
後端測試檔案
使用 pytest 進行單元測試和整合測試
"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
from app import app, db
from routes.vision import analyze_image_for_ingredients
from routes.recipes import retrieve_recipes, generate_customized_recipes
from routes.ingredients import get_ingredient_category

@pytest.fixture
def client():
    """建立測試客戶端"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def sample_image():
    """建立範例圖片檔案"""
    # 建立一個簡單的測試圖片
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        f.write(b'fake image data')
        return f.name

class TestHealthCheck:
    """健康檢查測試"""
    
    def test_health_check(self, client):
        """測試健康檢查端點"""
        response = client.get('/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert '冰箱救星' in data['message']
    
    def test_api_health(self, client):
        """測試 API 健康檢查端點"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert 'services' in data

class TestVisionAPI:
    """視覺識別 API 測試"""
    
    @patch('routes.vision.get_vision_client')
    def test_upload_and_analyze_success(self, mock_vision_client, client, sample_image):
        """測試成功上傳和分析圖片"""
        # 模擬 Vision API 回應
        mock_client = MagicMock()
        mock_label = MagicMock()
        mock_label.description = 'tomato'
        mock_label.score = 0.9
        
        mock_response = MagicMock()
        mock_response.label_annotations = [mock_label]
        mock_client.label_detection.return_value = mock_response
        mock_vision_client.return_value = mock_client
        
        with open(sample_image, 'rb') as f:
            response = client.post('/api/vision/upload', 
                                 data={'file': (f, 'test.jpg', 'image/jpeg')})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'ingredients' in data
    
    def test_upload_no_file(self, client):
        """測試沒有上傳檔案的情況"""
        response = client.post('/api/vision/upload')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_upload_invalid_file_type(self, client):
        """測試無效檔案類型"""
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            f.write(b'not an image')
            f.seek(0)
            response = client.post('/api/vision/upload',
                                 data={'file': (f, 'test.txt', 'text/plain')})
        
        assert response.status_code == 400
    
    def test_batch_upload(self, client, sample_image):
        """測試批次上傳"""
        with patch('routes.vision.get_vision_client') as mock_vision_client:
            mock_client = MagicMock()
            mock_label = MagicMock()
            mock_label.description = 'apple'
            mock_label.score = 0.8
            
            mock_response = MagicMock()
            mock_response.label_annotations = [mock_label]
            mock_client.label_detection.return_value = mock_response
            mock_vision_client.return_value = mock_client
            
            with open(sample_image, 'rb') as f:
                response = client.post('/api/vision/batch-upload',
                                     data={'files': [(f, 'test1.jpg'), (f, 'test2.jpg')]})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] == True
            assert data['total_images'] == 2

class TestRecipesAPI:
    """食譜 API 測試"""
    
    def test_search_recipes_no_ingredients(self, client):
        """測試沒有提供食材的搜尋"""
        response = client.post('/api/recipes/search', 
                              json={'ingredients': []})
        assert response.status_code == 400
    
    @patch('routes.recipes.retrieve_recipes')
    @patch('routes.recipes.generate_customized_recipes')
    def test_search_recipes_success(self, mock_generate, mock_retrieve, client):
        """測試成功搜尋食譜"""
        # 模擬檢索結果
        mock_retrieve.return_value = [
            {
                'id': '1',
                'name': '番茄炒蛋',
                'ingredients': ['番茄', '雞蛋'],
                'steps': ['步驟1', '步驟2'],
                'cooking_time': 15,
                'difficulty': '簡單',
                'cuisine': '中式',
                'similarity_score': 0.9
            }
        ]
        
        # 模擬生成結果
        mock_generate.return_value = [
            {
                'name': '番茄炒蛋',
                'description': '經典家常菜',
                'ingredients': [
                    {'name': '番茄', 'amount': '2個', 'available': True},
                    {'name': '雞蛋', 'amount': '3個', 'available': True}
                ],
                'steps': ['步驟1', '步驟2'],
                'cooking_time': '15分鐘',
                'difficulty': '簡單',
                'match_percentage': 90
            }
        ]
        
        response = client.post('/api/recipes/search',
                              json={'ingredients': ['番茄', '雞蛋']})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert len(data['recipes']) == 1
        assert data['recipes'][0]['name'] == '番茄炒蛋'
    
    def test_submit_feedback(self, client):
        """測試提交回饋"""
        response = client.post('/api/recipes/feedback',
                              json={
                                  'recipe_id': '1',
                                  'rating': 5,
                                  'comment': '很好吃！'
                              })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
    
    def test_submit_feedback_missing_rating(self, client):
        """測試缺少評分的回饋提交"""
        response = client.post('/api/recipes/feedback',
                              json={
                                  'recipe_id': '1',
                                  'comment': '很好吃！'
                              })
        
        assert response.status_code == 400
    
    def test_get_popular_recipes(self, client):
        """測試取得熱門食譜"""
        response = client.get('/api/recipes/popular')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'recipes' in data

class TestIngredientsAPI:
    """食材 API 測試"""
    
    def test_get_categories(self, client):
        """測試取得食材分類"""
        response = client.get('/api/ingredients/categories')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'categories' in data
        assert 'vegetables' in data['categories']
    
    def test_search_ingredients(self, client):
        """測試搜尋食材"""
        response = client.get('/api/ingredients/search?q=番茄')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'ingredients' in data
    
    def test_search_ingredients_no_query(self, client):
        """測試沒有搜尋關鍵字"""
        response = client.get('/api/ingredients/search')
        
        assert response.status_code == 400
    
    def test_validate_ingredients(self, client):
        """測試驗證食材"""
        response = client.post('/api/ingredients/validate',
                              json={'ingredients': ['番茄', '雞蛋']})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert len(data['ingredients']) == 2
    
    def test_suggest_ingredients(self, client):
        """測試建議食材"""
        response = client.post('/api/ingredients/suggest',
                              json={'ingredients': ['番茄']})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'suggestions' in data
    
    def test_get_nutrition(self, client):
        """測試取得營養資訊"""
        response = client.get('/api/ingredients/nutrition/番茄')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'nutrition' in data

class TestUtilityFunctions:
    """工具函數測試"""
    
    def test_analyze_image_for_ingredients(self):
        """測試圖片分析函數"""
        with patch('routes.vision.get_vision_client') as mock_vision_client:
            mock_client = MagicMock()
            mock_label = MagicMock()
            mock_label.description = 'tomato'
            mock_label.score = 0.9
            
            mock_response = MagicMock()
            mock_response.label_annotations = [mock_label]
            mock_client.label_detection.return_value = mock_response
            mock_vision_client.return_value = mock_client
            
            result = analyze_image_for_ingredients(b'fake image data')
            
            assert len(result) > 0
            assert result[0]['name'] == 'tomato'
            assert result[0]['confidence'] == 0.9
    
    def test_get_ingredient_category(self):
        """測試食材分類函數"""
        assert get_ingredient_category('番茄') == 'vegetables'
        assert get_ingredient_category('雞蛋') == 'others'
        assert get_ingredient_category('雞肉') == 'meat'
        assert get_ingredient_category('牛奶') == 'dairy'
    
    def test_categorize_ingredient(self):
        """測試食材分類邏輯"""
        from routes.vision import categorize_ingredient
        
        assert categorize_ingredient('tomato') == 'vegetables'
        assert categorize_ingredient('chicken') == 'meat'
        assert categorize_ingredient('milk') == 'dairy'
        assert categorize_ingredient('unknown') == 'others'

class TestErrorHandling:
    """錯誤處理測試"""
    
    def test_invalid_json(self, client):
        """測試無效的 JSON 請求"""
        response = client.post('/api/recipes/search',
                              data='invalid json',
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_missing_required_fields(self, client):
        """測試缺少必要欄位"""
        response = client.post('/api/recipes/search',
                              json={})
        
        assert response.status_code == 400
    
    def test_large_file_upload(self, client):
        """測試過大檔案上傳"""
        # 建立一個超過限制的檔案
        large_data = b'x' * (17 * 1024 * 1024)  # 17MB
        
        response = client.post('/api/vision/upload',
                              data={'file': (large_data, 'large.jpg', 'image/jpeg')})
        
        # 應該被 Flask 的 MAX_CONTENT_LENGTH 攔截
        assert response.status_code == 413

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
