#!/usr/bin/env python3
"""
向量索引建立腳本
使用 ChromaDB 建立食譜的向量索引，支援 RAG 檢索
"""

import os
import json
import psycopg2
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 資料庫連線設定
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/fridge_saver_db')
CHROMA_PERSIST_DIRECTORY = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')

def create_connection():
    """建立 PostgreSQL 連線"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"PostgreSQL 連線失敗: {e}")
        return None

def get_recipes_from_db(conn):
    """從資料庫取得所有食譜"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, ingredients, steps, cooking_time, difficulty, cuisine FROM recipes")
    
    recipes = []
    for row in cursor.fetchall():
        recipe = {
            'id': str(row[0]),
            'name': row[1],
            'description': row[2],
            'ingredients': json.loads(row[3]) if row[3] else [],
            'steps': json.loads(row[4]) if row[4] else [],
            'cooking_time': row[5],
            'difficulty': row[6],
            'cuisine': row[7]
        }
        recipes.append(recipe)
    
    return recipes

def create_recipe_text(recipe):
    """將食譜轉換為搜尋文本"""
    # 組合食譜的各個部分
    text_parts = []
    
    # 食譜名稱
    text_parts.append(f"食譜名稱: {recipe['name']}")
    
    # 描述
    if recipe['description']:
        text_parts.append(f"描述: {recipe['description']}")
    
    # 食材
    if recipe['ingredients']:
        ingredients_text = "食材: " + ", ".join([ing['name'] for ing in recipe['ingredients']])
        text_parts.append(ingredients_text)
    
    # 製作步驟
    if recipe['steps']:
        steps_text = "製作步驟: " + " ".join(recipe['steps'])
        text_parts.append(steps_text)
    
    # 烹飪資訊
    cooking_info = f"烹飪時間: {recipe['cooking_time']}分鐘, 難度: {recipe['difficulty']}, 菜系: {recipe['cuisine']}"
    text_parts.append(cooking_info)
    
    return " ".join(text_parts)

def create_vector_index():
    """建立向量索引"""
    print("初始化 ChromaDB...")
    
    # 初始化 ChromaDB 客戶端
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)
    
    # 取得或建立集合
    try:
        collection = client.get_collection("recipes")
        print("找到現有的食譜集合")
    except:
        collection = client.create_collection(
            name="recipes",
            metadata={"description": "食譜向量索引"}
        )
        print("建立新的食譜集合")
    
    # 初始化嵌入模型
    print("載入嵌入模型...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 從資料庫取得食譜
    print("從資料庫載入食譜...")
    conn = create_connection()
    if not conn:
        print("無法連接到資料庫")
        return
    
    recipes = get_recipes_from_db(conn)
    conn.close()
    
    if not recipes:
        print("沒有找到食譜資料")
        return
    
    print(f"找到 {len(recipes)} 筆食譜")
    
    # 準備資料
    documents = []
    metadatas = []
    ids = []
    
    for recipe in recipes:
        # 建立搜尋文本
        text = create_recipe_text(recipe)
        documents.append(text)
        
        # 建立元資料
        metadata = {
            'name': recipe['name'],
            'description': recipe['description'],
            'ingredients': json.dumps(recipe['ingredients'], ensure_ascii=False),
            'steps': json.dumps(recipe['steps'], ensure_ascii=False),
            'cooking_time': recipe['cooking_time'],
            'difficulty': recipe['difficulty'],
            'cuisine': recipe['cuisine']
        }
        metadatas.append(metadata)
        ids.append(recipe['id'])
    
    # 批次添加到 ChromaDB
    print("建立向量嵌入...")
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i+batch_size]
        batch_metadatas = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        
        collection.add(
            documents=batch_docs,
            metadatas=batch_metadatas,
            ids=batch_ids
        )
        
        print(f"已處理 {min(i+batch_size, len(documents))}/{len(documents)} 筆食譜")
    
    print("向量索引建立完成！")
    
    # 測試檢索
    print("\n測試檢索功能...")
    test_query = "番茄 雞蛋 簡單料理"
    results = collection.query(
        query_texts=[test_query],
        n_results=3
    )
    
    print(f"查詢: {test_query}")
    print("檢索結果:")
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        print(f"{i+1}. {metadata['name']} (相似度: {1-results['distances'][0][i]:.3f})")

def main():
    """主程式"""
    print("開始建立向量索引...")
    
    try:
        create_vector_index()
        print("向量索引建立完成！")
    except Exception as e:
        print(f"建立向量索引時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
