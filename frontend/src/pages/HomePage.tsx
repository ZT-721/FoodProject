import React from 'react';
import { Link } from 'react-router-dom';
import { Camera, ChefHat, Sparkles, ArrowRight } from 'lucide-react';

const HomePage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <section className="text-center py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            讓 AI 幫你
            <span className="text-gradient block">把剩食變美食</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 leading-relaxed">
            上傳冰箱食材照片，AI 智能識別並推薦專屬食譜
            <br />
            減少食物浪費，創造美味料理
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/upload"
              className="btn-primary text-lg px-8 py-3 inline-flex items-center justify-center space-x-2"
            >
              <Camera className="w-5 h-5" />
              <span>開始使用</span>
            </Link>
            <Link
              to="/recipes"
              className="btn-secondary text-lg px-8 py-3 inline-flex items-center justify-center space-x-2"
            >
              <ChefHat className="w-5 h-5" />
              <span>瀏覽食譜</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            為什麼選擇冰箱救星？
          </h2>
          <p className="text-lg text-gray-600">
            結合最新 AI 技術，讓烹飪變得簡單有趣
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="card text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Camera className="w-8 h-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              AI 智能識別
            </h3>
            <p className="text-gray-600">
              上傳食材照片，AI 自動識別食材種類和數量，準確率高達 90% 以上
            </p>
          </div>

          {/* Feature 2 */}
          <div className="card text-center">
            <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-8 h-8 text-secondary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              RAG 智能推薦
            </h3>
            <p className="text-gray-600">
              基於檢索增強生成技術，根據現有食材推薦最適合的食譜和替代方案
            </p>
          </div>

          {/* Feature 3 */}
          <div className="card text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <ChefHat className="w-8 h-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              詳細製作步驟
            </h3>
            <p className="text-gray-600">
              提供完整的食材清單、製作步驟和烹飪技巧，讓新手也能輕鬆上手
            </p>
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="py-16 bg-white rounded-2xl shadow-soft">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            使用流程
          </h2>
          <p className="text-lg text-gray-600">
            簡單三步驟，輕鬆開始你的烹飪之旅
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Step 1 */}
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
              1
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              上傳食材照片
            </h3>
            <p className="text-gray-600">
              拍攝或上傳冰箱中剩餘食材的照片
            </p>
          </div>

          {/* Step 2 */}
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
              2
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              AI 識別與確認
            </h3>
            <p className="text-gray-600">
              系統自動識別食材，你可手動調整清單
            </p>
          </div>

          {/* Step 3 */}
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
              3
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              獲得推薦食譜
            </h3>
            <p className="text-gray-600">
              查看客製化食譜，開始製作美味料理
            </p>
          </div>
        </div>

        <div className="text-center mt-8">
          <Link
            to="/upload"
            className="btn-primary text-lg px-8 py-3 inline-flex items-center space-x-2"
          >
            <span>立即開始</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16">
        <div className="grid md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-3xl font-bold text-primary-600 mb-2">1000+</div>
            <div className="text-gray-600">食譜資料庫</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary-600 mb-2">90%</div>
            <div className="text-gray-600">識別準確率</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary-600 mb-2">5秒</div>
            <div className="text-gray-600">平均處理時間</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary-600 mb-2">24/7</div>
            <div className="text-gray-600">全天候服務</div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
