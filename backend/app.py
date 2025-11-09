import json
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from routes.vision import vision_bp
from routes.recipes import recipes_bp
from routes.vision import get_ingredients_from_llm_openai  # 匯入真函數
import uuid
import os

# --- Flask Configuration ---
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.register_blueprint(vision_bp, url_prefix='/api')
app.register_blueprint(recipes_bp, url_prefix='/api')

# 允許所有來源進行 CORS 訪問 (在實際生產環境中應限制)
# 手動加入 CORS 標頭，因為我們沒有安裝 flask-cors
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# 模擬 AI 分析結果 (與前端 UploadPage.tsx 中的 mock 一致)
# 為了避免安裝 PyTorch 等大型套件導致建構失敗，我們暫時使用這個模擬數據。
MOCK_AI_RESPONSE = {
    "ingredients": [
        {"id": "1", "name": "雞蛋", "quantity": "5顆"},
        {"id": "2", "name": "番茄", "quantity": "2個"},
        {"id": "3", "name": "青椒", "quantity": ""},
        {"id": "4", "name": "蘑菇", "quantity": "一小盒"},
    ],
    "success": True,
    "total_images": 1
}

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image", "success": False}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file", "success": False}), 400

    # 儲存到臨時路徑
    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    file_path = os.path.join("/tmp", filename)  # Docker 內可用
    file.save(file_path)

    try:
        # 呼叫真 AI 分析
        raw_ingredients = get_ingredients_from_llm_openai(file_path)

        # 轉換格式 + 加上 id
        ingredients = [
            {
                "id": str(i+1),
                "name": ing["name"],
                "quantity": ing.get("quantity", "")
            }
            for i, ing in enumerate(raw_ingredients)
        ]

        return jsonify({
            "ingredients": ingredients,
            "success": True,
            "total_images": 1
        })

    finally:
        # 清理臨時檔案
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/api/status', methods=['GET'])
def status_check():
    """服務健康檢查"""
    return jsonify({"status": "Backend running in MOCK mode 有在運行中喔", "mock_mode": False})

if __name__ == '__main__':
    # 在 gunicorn/docker 環境中，此處代碼不會運行
    app.run(debug=True, host='0.0.0.0', port=5000)
