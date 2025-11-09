# backend/routes/recipes.py

import os
import json
from flask import Blueprint, request, jsonify, current_app
from openai import OpenAI
from typing import List, Dict, Any

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

# -------------------------------------------------------------
# 型別定義（取代舊的 ChatCompletionMessageParam）
# -------------------------------------------------------------
Message = Dict[str, str]  # {"role": "user", "content": "..."}
Messages = List[Message]

# -------------------------------------------------------------
# 初始化 OpenAI 客戶端
# -------------------------------------------------------------
try:
    # 讀取 .env 中的 OPENAI_API_KEY
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception as e:
    current_app.logger.error(f"Failed to initialize OpenAI Client for recipes: {e}")
    openai_client = None

# -------------------------------------------------------------
# 食譜搜尋 (search) 路由：完全由 LLM 生成 (使用 GPT-4o)
# -------------------------------------------------------------
@recipes_bp.route('/search', methods=['POST'])
def search_recipes():
    # === 讀取 JSON body ===
    data = request.get_json(silent=True)
    if not data or 'ingredients' not in data:
        return jsonify({'error': 'Missing ingredients', 'success': False}), 400

    ingredients_list = data['ingredients']
    if not isinstance(ingredients_list, list):
        return jsonify({'error': 'Ingredients must be a list', 'success': False}), 400

    cleaned_ingredients = [i.strip() for i in ingredients_list if i.strip()]
    if not cleaned_ingredients:
        return jsonify({'recipes': [], 'success': True})

    if not openai_client:
        return jsonify({'error': 'OpenAI service unavailable', 'success': False}), 500

    try:
        ingredients_str = "、".join(cleaned_ingredients)
        prompt = (
            f"根據以下食材: {ingredients_str}，推薦 3 道最適合的食譜。 "
            "每個食譜包含：名稱、描述、時間(分鐘)、難度(簡單/中等/困難)、主要食材。 "
            "嚴格回傳 JSON: "
            "{\"recipes\": [{\"name\": \"\", \"description\": \"\", \"time\": 30, \"difficulty\": \"中等\", \"main_ingredients\": []}]}"
        )

        messages: Messages = [{"role": "user", "content": prompt}]

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=1000
        )

        content = response.choices[0].message.content
        if not content:
            return jsonify({'recipes': [], 'success': True})

        result = json.loads(content)
        recipes = result.get('recipes', [])

        # 補上 id（前端需要）
        for i, recipe in enumerate(recipes):
            recipe['id'] = str(i + 1)

        return jsonify({
            'recipes': recipes,
            'success': True
        })

    except Exception as e:
        current_app.logger.error(f"Recipe generation error: {e}")
        return jsonify({'error': 'Generation failed', 'success': False}), 500