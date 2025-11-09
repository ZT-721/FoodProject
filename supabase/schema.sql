-- Supabase 資料庫設定腳本
-- 建立冰箱救星 AI 食譜推薦系統的資料庫結構

-- 啟用必要的擴展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 建立食譜表格
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 建立回饋表格
CREATE TABLE IF NOT EXISTS recipe_feedback (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    user_ip INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 建立使用者表格 (未來擴展用)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 建立使用記錄表格
CREATE TABLE IF NOT EXISTS usage_logs (
    id SERIAL PRIMARY KEY,
    user_ip INET,
    action VARCHAR(100) NOT NULL,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 建立索引
CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine);
CREATE INDEX IF NOT EXISTS idx_recipes_difficulty ON recipes(difficulty);
CREATE INDEX IF NOT EXISTS idx_recipes_cooking_time ON recipes(cooking_time);
CREATE INDEX IF NOT EXISTS idx_recipes_ingredients ON recipes USING GIN(ingredients);
CREATE INDEX IF NOT EXISTS idx_feedback_recipe_id ON recipe_feedback(recipe_id);
CREATE INDEX IF NOT EXISTS idx_feedback_rating ON recipe_feedback(rating);
CREATE INDEX IF NOT EXISTS idx_usage_logs_action ON usage_logs(action);
CREATE INDEX IF NOT EXISTS idx_usage_logs_created_at ON usage_logs(created_at);

-- 建立全文搜尋索引
CREATE INDEX IF NOT EXISTS idx_recipes_search ON recipes USING GIN(
    to_tsvector('english', name || ' ' || COALESCE(description, ''))
);

-- 建立觸發器函數來更新 updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 建立觸發器
CREATE TRIGGER update_recipes_updated_at 
    BEFORE UPDATE ON recipes 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入範例食譜資料
INSERT INTO recipes (name, description, ingredients, steps, cooking_time, difficulty, cuisine) VALUES
('番茄炒蛋', '經典家常菜，簡單易做，營養豐富', 
 '[{"name": "番茄", "amount": "2個", "category": "vegetables"}, {"name": "雞蛋", "amount": "3個", "category": "others"}, {"name": "蔥", "amount": "1根", "category": "vegetables"}, {"name": "鹽", "amount": "適量", "category": "others"}, {"name": "糖", "amount": "1茶匙", "category": "others"}, {"name": "油", "amount": "2大匙", "category": "others"}]',
 '["將番茄洗淨，切成小塊備用", "將雞蛋打散，加入少許鹽調味", "熱鍋下油，倒入蛋液炒至半熟盛起", "原鍋下番茄塊，炒出汁水", "加入糖和鹽調味", "倒入炒蛋拌炒均勻即可"]',
 15, '簡單', '中式'),

('青椒肉絲', '下飯好菜，營養豐富，口感清脆',
 '[{"name": "青椒", "amount": "2個", "category": "vegetables"}, {"name": "豬肉絲", "amount": "200g", "category": "meat"}, {"name": "大蒜", "amount": "2瓣", "category": "vegetables"}, {"name": "醬油", "amount": "2大匙", "category": "others"}, {"name": "米酒", "amount": "1大匙", "category": "others"}, {"name": "太白粉", "amount": "1茶匙", "category": "others"}, {"name": "油", "amount": "3大匙", "category": "others"}]',
 '["青椒洗淨切絲，大蒜切片", "豬肉絲用醬油、米酒、太白粉醃製15分鐘", "熱鍋下油，爆香大蒜", "下肉絲炒至變色", "加入青椒絲炒熟", "調味後即可起鍋"]',
 20, '中等', '中式'),

('蛋炒飯', '經典炒飯，簡單快速，適合清冰箱',
 '[{"name": "白飯", "amount": "2碗", "category": "grains"}, {"name": "雞蛋", "amount": "2個", "category": "others"}, {"name": "蔥", "amount": "2根", "category": "vegetables"}, {"name": "鹽", "amount": "適量", "category": "others"}, {"name": "醬油", "amount": "1大匙", "category": "others"}, {"name": "油", "amount": "2大匙", "category": "others"}]',
 '["將雞蛋打散，蔥切花", "熱鍋下油，倒入蛋液炒至半熟", "加入白飯炒散", "加入醬油和鹽調味", "最後撒上蔥花即可"]',
 10, '簡單', '中式'),

('義大利麵', '西式經典，簡單美味',
 '[{"name": "義大利麵", "amount": "200g", "category": "grains"}, {"name": "番茄", "amount": "3個", "category": "vegetables"}, {"name": "洋蔥", "amount": "1個", "category": "vegetables"}, {"name": "大蒜", "amount": "3瓣", "category": "vegetables"}, {"name": "橄欖油", "amount": "3大匙", "category": "others"}, {"name": "鹽", "amount": "適量", "category": "others"}, {"name": "黑胡椒", "amount": "適量", "category": "others"}, {"name": "起司", "amount": "50g", "category": "dairy"}]',
 '["煮一鍋水，加鹽，下義大利麵煮8-10分鐘", "番茄切丁，洋蔥切絲，大蒜切片", "熱鍋下橄欖油，爆香大蒜和洋蔥", "加入番茄丁炒出汁水", "加入煮好的義大利麵拌炒", "調味後撒上起司即可"]',
 25, '中等', '西式'),

('蔬菜湯', '清爽健康，適合減肥',
 '[{"name": "高麗菜", "amount": "1/4顆", "category": "vegetables"}, {"name": "胡蘿蔔", "amount": "1根", "category": "vegetables"}, {"name": "馬鈴薯", "amount": "1個", "category": "vegetables"}, {"name": "洋蔥", "amount": "1個", "category": "vegetables"}, {"name": "番茄", "amount": "2個", "category": "vegetables"}, {"name": "鹽", "amount": "適量", "category": "others"}, {"name": "胡椒", "amount": "適量", "category": "others"}, {"name": "水", "amount": "1000ml", "category": "others"}]',
 '["所有蔬菜洗淨切塊", "熱鍋下少許油，炒香洋蔥", "加入其他蔬菜炒一下", "加水煮滾後轉小火煮20分鐘", "調味後即可"]',
 30, '簡單', '西式')
ON CONFLICT DO NOTHING;

-- 建立 RLS (Row Level Security) 政策
ALTER TABLE recipes ENABLE ROW LEVEL SECURITY;
ALTER TABLE recipe_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_logs ENABLE ROW LEVEL SECURITY;

-- 允許公開讀取食譜
CREATE POLICY "Allow public read access to recipes" ON recipes
    FOR SELECT USING (true);

-- 允許公開插入回饋
CREATE POLICY "Allow public insert to feedback" ON recipe_feedback
    FOR INSERT WITH CHECK (true);

-- 允許公開讀取回饋
CREATE POLICY "Allow public read access to feedback" ON recipe_feedback
    FOR SELECT USING (true);

-- 允許公開插入使用記錄
CREATE POLICY "Allow public insert to usage_logs" ON usage_logs
    FOR INSERT WITH CHECK (true);

-- 建立搜尋函數
CREATE OR REPLACE FUNCTION search_recipes(
    search_query TEXT DEFAULT '',
    cuisine_filter TEXT DEFAULT '',
    difficulty_filter TEXT DEFAULT '',
    max_cooking_time INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR(255),
    description TEXT,
    ingredients JSONB,
    steps JSONB,
    cooking_time INTEGER,
    difficulty VARCHAR(50),
    cuisine VARCHAR(50),
    image_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id,
        r.name,
        r.description,
        r.ingredients,
        r.steps,
        r.cooking_time,
        r.difficulty,
        r.cuisine,
        r.image_url,
        r.created_at,
        r.updated_at,
        CASE 
            WHEN search_query = '' THEN 1.0
            ELSE ts_rank(to_tsvector('english', r.name || ' ' || COALESCE(r.description, '')), plainto_tsquery('english', search_query))
        END as rank
    FROM recipes r
    WHERE 
        (search_query = '' OR to_tsvector('english', r.name || ' ' || COALESCE(r.description, '')) @@ plainto_tsquery('english', search_query))
        AND (cuisine_filter = '' OR r.cuisine = cuisine_filter)
        AND (difficulty_filter = '' OR r.difficulty = difficulty_filter)
        AND (max_cooking_time IS NULL OR r.cooking_time <= max_cooking_time)
    ORDER BY rank DESC, r.created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- 建立統計函數
CREATE OR REPLACE FUNCTION get_recipe_stats()
RETURNS TABLE (
    total_recipes INTEGER,
    avg_rating NUMERIC,
    total_feedback INTEGER,
    popular_cuisine VARCHAR(50),
    avg_cooking_time NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(r.id)::INTEGER as total_recipes,
        ROUND(AVG(rf.rating), 2) as avg_rating,
        COUNT(rf.id)::INTEGER as total_feedback,
        (SELECT cuisine FROM recipes GROUP BY cuisine ORDER BY COUNT(*) DESC LIMIT 1) as popular_cuisine,
        ROUND(AVG(r.cooking_time), 1) as avg_cooking_time
    FROM recipes r
    LEFT JOIN recipe_feedback rf ON r.id = rf.recipe_id;
END;
$$ LANGUAGE plpgsql;

-- 建立使用統計函數
CREATE OR REPLACE FUNCTION get_usage_stats(days INTEGER DEFAULT 7)
RETURNS TABLE (
    total_requests INTEGER,
    unique_users INTEGER,
    popular_actions TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::INTEGER as total_requests,
        COUNT(DISTINCT user_ip)::INTEGER as unique_users,
        ARRAY_AGG(action ORDER BY COUNT(*) DESC) as popular_actions
    FROM usage_logs
    WHERE created_at >= NOW() - INTERVAL '1 day' * days;
END;
$$ LANGUAGE plpgsql;
