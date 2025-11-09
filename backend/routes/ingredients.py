from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

# 建立藍圖
bp = Blueprint('ingredients', __name__)

# 常見食材資料庫
COMMON_INGREDIENTS = {
    'vegetables': [
        '番茄', '洋蔥', '大蒜', '胡蘿蔔', '馬鈴薯', '高麗菜', '菠菜', 
        '花椰菜', '蘑菇', '青椒', '紅椒', '黃椒', '小黃瓜', '芹菜',
        '韭菜', '蔥', '薑', '蒜苗', '白蘿蔔', '紅蘿蔔', '玉米', '豌豆'
    ],
    'fruits': [
        '蘋果', '香蕉', '橘子', '檸檬', '萊姆', '葡萄', '草莓', '藍莓',
        '奇異果', '鳳梨', '芒果', '西瓜', '哈密瓜', '梨子', '桃子', '櫻桃'
    ],
    'meat': [
        '雞肉', '牛肉', '豬肉', '羊肉', '火雞肉', '雞胸肉', '雞腿肉',
        '牛絞肉', '豬絞肉', '培根', '火腿', '香腸', '臘肉'
    ],
    'seafood': [
        '魚', '鮭魚', '鮪魚', '蝦子', '螃蟹', '龍蝦', '蛤蜊', '牡蠣',
        '花枝', '章魚', '干貝', '魚丸', '蝦仁'
    ],
    'dairy': [
        '牛奶', '起司', '優格', '奶油', '鮮奶油', '酸奶', '乳酪',
        '馬茲瑞拉起司', '切達起司', '帕瑪森起司'
    ],
    'grains': [
        '米飯', '麵包', '麵條', '義大利麵', '麥片', '燕麥', '藜麥',
        '糙米', '白米', '糯米', '冬粉', '米粉', '烏龍麵'
    ],
    'others': [
        '雞蛋', '油', '鹽', '糖', '醬油', '醋', '胡椒', '香料',
        '香草', '蜂蜜', '果醬', '花生醬', '芝麻', '堅果'
    ]
}

@bp.route('/categories', methods=['GET'])
def get_ingredient_categories():
    """取得食材分類"""
    try:
        return jsonify({
            'success': True,
            'categories': COMMON_INGREDIENTS
        })
    except Exception as e:
        logger.error(f"取得食材分類錯誤: {e}")
        return jsonify({'error': '取得食材分類失敗'}), 500

@bp.route('/search', methods=['GET'])
def search_ingredients():
    """搜尋食材"""
    try:
        query = request.args.get('q', '').lower()
        category = request.args.get('category', '')
        
        if not query:
            return jsonify({'error': '請提供搜尋關鍵字'}), 400
        
        results = []
        
        # 如果指定了分類，只搜尋該分類
        if category and category in COMMON_INGREDIENTS:
            ingredients = COMMON_INGREDIENTS[category]
        else:
            # 搜尋所有分類
            ingredients = []
            for cat_ingredients in COMMON_INGREDIENTS.values():
                ingredients.extend(cat_ingredients)
        
        # 搜尋匹配的食材
        for ingredient in ingredients:
            if query in ingredient.lower():
                results.append({
                    'name': ingredient,
                    'category': get_ingredient_category(ingredient)
                })
        
        return jsonify({
            'success': True,
            'ingredients': results[:20]  # 限制結果數量
        })
        
    except Exception as e:
        logger.error(f"搜尋食材錯誤: {e}")
        return jsonify({'error': '搜尋食材失敗'}), 500

def get_ingredient_category(ingredient):
    """取得食材所屬分類"""
    for category, ingredients in COMMON_INGREDIENTS.items():
        if ingredient in ingredients:
            return category
    return 'others'

@bp.route('/validate', methods=['POST'])
def validate_ingredients():
    """驗證食材清單"""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({'error': '請提供食材清單'}), 400
        
        validated_ingredients = []
        
        for ingredient in ingredients:
            # 檢查食材是否存在於資料庫中
            category = get_ingredient_category(ingredient)
            
            validated_ingredients.append({
                'name': ingredient,
                'category': category,
                'valid': category != 'others' or ingredient in COMMON_INGREDIENTS['others']
            })
        
        return jsonify({
            'success': True,
            'ingredients': validated_ingredients
        })
        
    except Exception as e:
        logger.error(f"驗證食材錯誤: {e}")
        return jsonify({'error': '驗證食材失敗'}), 500

@bp.route('/suggest', methods=['POST'])
def suggest_ingredients():
    """根據現有食材建議額外食材"""
    try:
        data = request.get_json()
        current_ingredients = data.get('ingredients', [])
        
        if not current_ingredients:
            return jsonify({'error': '請提供現有食材清單'}), 400
        
        # 分析現有食材的分類
        current_categories = set()
        for ingredient in current_ingredients:
            category = get_ingredient_category(ingredient)
            current_categories.add(category)
        
        # 建議互補的食材
        suggestions = []
        
        # 如果沒有蔬菜，建議蔬菜
        if 'vegetables' not in current_categories:
            suggestions.extend(COMMON_INGREDIENTS['vegetables'][:3])
        
        # 如果沒有蛋白質，建議蛋白質
        if not any(cat in current_categories for cat in ['meat', 'seafood', 'dairy']):
            suggestions.extend(COMMON_INGREDIENTS['meat'][:2])
            suggestions.extend(COMMON_INGREDIENTS['dairy'][:1])
        
        # 如果沒有調味料，建議基本調味料
        if 'others' not in current_categories:
            suggestions.extend(['鹽', '胡椒', '油'])
        
        return jsonify({
            'success': True,
            'suggestions': suggestions[:10]  # 限制建議數量
        })
        
    except Exception as e:
        logger.error(f"建議食材錯誤: {e}")
        return jsonify({'error': '建議食材失敗'}), 500

@bp.route('/nutrition/<ingredient>', methods=['GET'])
def get_ingredient_nutrition(ingredient):
    """取得食材營養資訊"""
    try:
        # 這裡可以整合營養資料庫 API
        # 目前回傳基本資訊
        nutrition_info = {
            'name': ingredient,
            'calories_per_100g': 50,  # 範例數據
            'protein': 2.0,
            'carbs': 10.0,
            'fat': 0.5,
            'fiber': 2.0,
            'vitamins': ['維生素C', '維生素A'],
            'minerals': ['鉀', '鈣']
        }
        
        return jsonify({
            'success': True,
            'nutrition': nutrition_info
        })
        
    except Exception as e:
        logger.error(f"取得營養資訊錯誤: {e}")
        return jsonify({'error': '取得營養資訊失敗'}), 500
