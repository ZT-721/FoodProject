#!/usr/bin/env python3
"""
食譜資料庫建立腳本
建立 PostgreSQL 資料庫表格並插入範例食譜資料
"""

import os
import json
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 資料庫連線設定
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/fridge_saver_db')

def create_connection():
    """建立資料庫連線"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"資料庫連線失敗: {e}")
        return None

def create_tables(conn):
    """建立資料庫表格"""
    cursor = conn.cursor()
    
    # 建立食譜表格
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            ingredients JSONB NOT NULL,
            steps JSONB NOT NULL,
            cooking_time INTEGER NOT NULL,
            difficulty VARCHAR(50) NOT NULL,
            cuisine VARCHAR(50),
            image_url VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 建立回饋表格
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_feedback (
            id SERIAL PRIMARY KEY,
            recipe_id INTEGER REFERENCES recipes(id),
            rating INTEGER CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 建立索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_difficulty ON recipes(difficulty)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_cooking_time ON recipes(cooking_time)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_recipe_id ON recipe_feedback(recipe_id)")
    
    conn.commit()
    print("資料庫表格建立完成")

def insert_sample_recipes(conn):
    """插入範例食譜資料"""
    cursor = conn.cursor()
    
    sample_recipes = [
        {
            "name": "番茄炒蛋",
            "description": "經典家常菜，簡單易做，營養豐富",
            "ingredients": [
                {"name": "番茄", "amount": "2個", "category": "vegetables"},
                {"name": "雞蛋", "amount": "3個", "category": "others"},
                {"name": "蔥", "amount": "1根", "category": "vegetables"},
                {"name": "鹽", "amount": "適量", "category": "others"},
                {"name": "糖", "amount": "1茶匙", "category": "others"},
                {"name": "油", "amount": "2大匙", "category": "others"}
            ],
            "steps": [
                "將番茄洗淨，切成小塊備用",
                "將雞蛋打散，加入少許鹽調味",
                "熱鍋下油，倒入蛋液炒至半熟盛起",
                "原鍋下番茄塊，炒出汁水",
                "加入糖和鹽調味",
                "倒入炒蛋拌炒均勻即可"
            ],
            "cooking_time": 15,
            "difficulty": "簡單",
            "cuisine": "中式"
        },
        {
            "name": "青椒肉絲",
            "description": "下飯好菜，營養豐富，口感清脆",
            "ingredients": [
                {"name": "青椒", "amount": "2個", "category": "vegetables"},
                {"name": "豬肉絲", "amount": "200g", "category": "meat"},
                {"name": "大蒜", "amount": "2瓣", "category": "vegetables"},
                {"name": "醬油", "amount": "2大匙", "category": "others"},
                {"name": "米酒", "amount": "1大匙", "category": "others"},
                {"name": "太白粉", "amount": "1茶匙", "category": "others"},
                {"name": "油", "amount": "3大匙", "category": "others"}
            ],
            "steps": [
                "青椒洗淨切絲，大蒜切片",
                "豬肉絲用醬油、米酒、太白粉醃製15分鐘",
                "熱鍋下油，爆香大蒜",
                "下肉絲炒至變色",
                "加入青椒絲炒熟",
                "調味後即可起鍋"
            ],
            "cooking_time": 20,
            "difficulty": "中等",
            "cuisine": "中式"
        },
        {
            "name": "蛋炒飯",
            "description": "經典炒飯，簡單快速，適合清冰箱",
            "ingredients": [
                {"name": "白飯", "amount": "2碗", "category": "grains"},
                {"name": "雞蛋", "amount": "2個", "category": "others"},
                {"name": "蔥", "amount": "2根", "category": "vegetables"},
                {"name": "鹽", "amount": "適量", "category": "others"},
                {"name": "醬油", "amount": "1大匙", "category": "others"},
                {"name": "油", "amount": "2大匙", "category": "others"}
            ],
            "steps": [
                "將雞蛋打散，蔥切花",
                "熱鍋下油，倒入蛋液炒至半熟",
                "加入白飯炒散",
                "加入醬油和鹽調味",
                "最後撒上蔥花即可"
            ],
            "cooking_time": 10,
            "difficulty": "簡單",
            "cuisine": "中式"
        },
        {
            "name": "義大利麵",
            "description": "西式經典，簡單美味",
            "ingredients": [
                {"name": "義大利麵", "amount": "200g", "category": "grains"},
                {"name": "番茄", "amount": "3個", "category": "vegetables"},
                {"name": "洋蔥", "amount": "1個", "category": "vegetables"},
                {"name": "大蒜", "amount": "3瓣", "category": "vegetables"},
                {"name": "橄欖油", "amount": "3大匙", "category": "others"},
                {"name": "鹽", "amount": "適量", "category": "others"},
                {"name": "黑胡椒", "amount": "適量", "category": "others"},
                {"name": "起司", "amount": "50g", "category": "dairy"}
            ],
            "steps": [
                "煮一鍋水，加鹽，下義大利麵煮8-10分鐘",
                "番茄切丁，洋蔥切絲，大蒜切片",
                "熱鍋下橄欖油，爆香大蒜和洋蔥",
                "加入番茄丁炒出汁水",
                "加入煮好的義大利麵拌炒",
                "調味後撒上起司即可"
            ],
            "cooking_time": 25,
            "difficulty": "中等",
            "cuisine": "西式"
        },
        {
            "name": "蔬菜湯",
            "description": "清爽健康，適合減肥",
            "ingredients": [
                {"name": "高麗菜", "amount": "1/4顆", "category": "vegetables"},
                {"name": "胡蘿蔔", "amount": "1根", "category": "vegetables"},
                {"name": "馬鈴薯", "amount": "1個", "category": "vegetables"},
                {"name": "洋蔥", "amount": "1個", "category": "vegetables"},
                {"name": "番茄", "amount": "2個", "category": "vegetables"},
                {"name": "鹽", "amount": "適量", "category": "others"},
                {"name": "胡椒", "amount": "適量", "category": "others"},
                {"name": "水", "amount": "1000ml", "category": "others"}
            ],
            "steps": [
                "所有蔬菜洗淨切塊",
                "熱鍋下少許油，炒香洋蔥",
                "加入其他蔬菜炒一下",
                "加水煮滾後轉小火煮20分鐘",
                "調味後即可"
            ],
            "cooking_time": 30,
            "difficulty": "簡單",
            "cuisine": "西式"
        }
    ]
    
    for recipe in sample_recipes:
        cursor.execute("""
            INSERT INTO recipes (name, description, ingredients, steps, cooking_time, difficulty, cuisine)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            recipe["name"],
            recipe["description"],
            json.dumps(recipe["ingredients"], ensure_ascii=False),
            json.dumps(recipe["steps"], ensure_ascii=False),
            recipe["cooking_time"],
            recipe["difficulty"],
            recipe["cuisine"]
        ))
    
    conn.commit()
    print(f"已插入 {len(sample_recipes)} 筆範例食譜")

def main():
    """主程式"""
    print("開始建立食譜資料庫...")
    
    # 建立資料庫連線
    conn = create_connection()
    if not conn:
        print("無法連接到資料庫，請檢查設定")
        return
    
    try:
        # 建立表格
        create_tables(conn)
        
        # 插入範例資料
        insert_sample_recipes(conn)
        
        print("資料庫建立完成！")
        
    except Exception as e:
        print(f"建立資料庫時發生錯誤: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
