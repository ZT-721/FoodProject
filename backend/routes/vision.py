# backend/routes/vision.py

import os
import json
import base64
from typing import List, Dict, TypedDict
from flask import Blueprint, request, jsonify, current_app
from openai import OpenAI

vision_bp = Blueprint('vision', __name__, url_prefix='/vision')

# -------------------------------------------------------------
# 型別定義（取代舊的 ChatCompletionMessageParam）
# -------------------------------------------------------------
class ContentPart(TypedDict, total=False):
    type: str
    text: str
    image_url: Dict[str, Dict[str, str]]

class Message(TypedDict):
    role: str
    content: List[ContentPart]

# 也可以用 TypeAlias 更簡潔
Messages = List[Message]

# -------------------------------------------------------------
# 初始化 OpenAI 客戶端
# -------------------------------------------------------------
try:
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception as e:
    current_app.logger.error(f"Failed to initialize OpenAI Client: {e}")
    openai_client = None

# -------------------------------------------------------------
# LLM 多模態識別函式 (使用 GPT-4o Vision)
# -------------------------------------------------------------
def get_ingredients_from_llm_openai(file_path):
    """
    使用 OpenAI GPT-4o Vision 進行圖像識別。
    """
    if not openai_client:
        return []

    try:
        # 1. 將圖片檔案轉換為 Base64 編碼
        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        # 2. 定義 Prompt 內容
        prompt_text = (
            "你是一位專業的廚師助理。請嚴格忽略圖片中的任何人、臉部或人物，"
            "只專注於辨識食材。請根據圖片中的食物，識別出所有主要的食材。 "
            "請嚴格以 JSON 格式回應，不要包含任何額外文字。JSON 格式必須是: "
            "{\"ingredients\": [{\"name\": \"食材名\", \"category\": \"類別\"}]}"
        )

        # 3. 構造多模態內容 (圖片 + 文字)
        messages: Messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        # 4. 呼叫 GPT-4o Vision
        response = openai_client.chat.completions.create(
            # model="gpt-4o", # 因OpenAI 的安全機制觸發了「人臉識別」限制，通常不提供辨識圖片
            model="gpt-4o-mini", # 支援多模態的最新模型
            messages=messages,
            response_format={"type": "json_object"}, # 確保 JSON 輸出
            max_tokens=2000
        )
        current_app.logger.debug(f"OpenAI GPT-4o API Response: {response}")

        # 5. 解析結果
        content = response.choices[0].message.content
        current_app.logger.debug(f"OpenAI GPT-4o API content: {content}")
        if content:
            llm_result = json.loads(content)
            final_ingredients = [
                {
                    'name': item['name'],
                    'confidence': 1.0,
                    'category': item.get('category', 'unknown')
                }
                for item in llm_result.get('ingredients', [])
            ]
            return final_ingredients
        return []

    except Exception as e:
        current_app.logger.error(f"OpenAI GPT-4o API Error: {e}")
        return []

# -------------------------------------------------------------
# 修改您的批次上傳 (batch-upload) 路由，使用 LLM 作為主要識別器
# -------------------------------------------------------------
@vision_bp.route('/batch-upload', methods=['POST'])
def batch_upload():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part', 'success': False}), 400

    all_ingredients = []
    
    for file in request.files.getlist('files'):
        if file.filename == '':
            continue
        
        # ⚠️ 這裡需要您的檔案儲存邏輯 ⚠️
        # 為了簡化，假設您已經有將檔案存到 temporary 並且獲取 file_path 的邏輯
        try:
            # 假設檔案被存儲在一個臨時路徑
            filename = file.filename # 您應該使用更安全的儲存方式
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename) 
            file.save(file_path)
        except Exception as e:
            current_app.logger.error(f"File saving error: {e}")
            continue

        # 執行 LLM 多模態識別
        ingredients_from_llm = get_ingredients_from_llm_openai(file_path)
        all_ingredients.extend(ingredients_from_llm)
        
        # 檔案清理 (請確保您的程式碼有清理機制)
        if os.path.exists(file_path):
             os.remove(file_path)

    # ... (去重/整理邏輯，如果需要) ...

    return jsonify({
        'success': True,
        'ingredients': all_ingredients,
        'total_images': len(request.files.getlist('files'))
    })