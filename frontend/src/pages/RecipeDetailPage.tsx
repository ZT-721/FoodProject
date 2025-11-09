import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock, Star, ChefHat, CheckCircle, AlertCircle, ThumbsUp, ThumbsDown } from 'lucide-react';
import toast from 'react-hot-toast';

interface Recipe {
  id: string;
  name: string;
  description: string;
  ingredients: Array<{
    name: string;
    amount: string;
    available: boolean;
    substitute?: string;
  }>;
  steps: string[];
  cooking_time: string;
  difficulty: string;
  match_percentage: number;
  rating?: number;
}

const RecipeDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const [feedback, setFeedback] = useState({
    rating: 0,
    comment: ''
  });

  useEffect(() => {
    loadRecipe();
  }, [id]);

  const loadRecipe = async () => {
    setIsLoading(true);
    try {
      // 模擬載入食譜資料
      const mockRecipe: Recipe = {
        id: id || '1',
        name: '番茄炒蛋',
        description: '經典家常菜，簡單易做，營養豐富',
        ingredients: [
          { name: '番茄', amount: '2個', available: true },
          { name: '雞蛋', amount: '3個', available: true },
          { name: '蔥', amount: '1根', available: false, substitute: '洋蔥' },
          { name: '鹽', amount: '適量', available: true },
          { name: '糖', amount: '1茶匙', available: true },
          { name: '油', amount: '2大匙', available: true }
        ],
        steps: [
          '將番茄洗淨，切成小塊備用',
          '將雞蛋打散，加入少許鹽調味',
          '熱鍋下油，倒入蛋液炒至半熟盛起',
          '原鍋下番茄塊，炒出汁水',
          '加入糖和鹽調味',
          '倒入炒蛋拌炒均勻即可'
        ],
        cooking_time: '15分鐘',
        difficulty: '簡單',
        match_percentage: 85,
        rating: 4.5
      };
      
      setRecipe(mockRecipe);
    } catch (error) {
      toast.error('載入食譜失敗');
    } finally {
      setIsLoading(false);
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case '簡單': return 'bg-green-100 text-green-800';
      case '中等': return 'bg-yellow-100 text-yellow-800';
      case '困難': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const submitFeedback = async () => {
    if (feedback.rating === 0) {
      toast.error('請選擇評分');
      return;
    }

    try {
      // 提交回饋到後端
      toast.success('感謝您的回饋！');
      setFeedback({ rating: 0, comment: '' });
    } catch (error) {
      toast.error('提交回饋失敗');
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <div className="loading-spinner mx-auto mb-4" />
          <p className="text-gray-600">載入食譜中...</p>
        </div>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            食譜不存在
          </h3>
          <button
            onClick={() => navigate('/recipes')}
            className="btn-primary mt-4"
          >
            返回食譜列表
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/recipes')}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>返回食譜列表</span>
        </button>
        
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {recipe.name}
            </h1>
            <p className="text-lg text-gray-600 mb-4">
              {recipe.description}
            </p>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-1 text-gray-600">
                <Clock className="w-4 h-4" />
                <span>{recipe.cooking_time}</span>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(recipe.difficulty)}`}>
                {recipe.difficulty}
              </span>
              <div className="flex items-center space-x-1">
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <span className="text-gray-600">{recipe.rating}</span>
              </div>
              <div className="text-sm font-medium text-green-600">
                {recipe.match_percentage}% 食材吻合
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Ingredients */}
        <div className="lg:col-span-1">
          <div className="card sticky top-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              食材清單
            </h3>
            
            <div className="space-y-3">
              {recipe.ingredients.map((ingredient, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="font-medium text-gray-900">
                        {ingredient.name}
                      </span>
                      {ingredient.available ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <AlertCircle className="w-4 h-4 text-orange-500" />
                      )}
                    </div>
                    <div className="text-sm text-gray-600">
                      {ingredient.amount}
                    </div>
                    {!ingredient.available && ingredient.substitute && (
                      <div className="text-xs text-blue-600 mt-1">
                        替代：{ingredient.substitute}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Steps */}
        <div className="lg:col-span-2">
          <div className="card">
            <h3 className="text-xl font-semibold text-gray-900 mb-6">
              製作步驟
            </h3>
            
            <div className="space-y-6">
              {recipe.steps.map((step, index) => (
                <div key={index} className="flex items-start space-x-4">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    index <= currentStep 
                      ? 'bg-primary-500 text-white' 
                      : 'bg-gray-200 text-gray-600'
                  }`}>
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <p className="text-gray-900 leading-relaxed">
                      {step}
                    </p>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-8 flex items-center justify-between">
              <button
                onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                disabled={currentStep === 0}
                className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                上一步
              </button>
              
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">
                  步驟 {currentStep + 1} / {recipe.steps.length}
                </span>
              </div>
              
              <button
                onClick={() => setCurrentStep(Math.min(recipe.steps.length - 1, currentStep + 1))}
                disabled={currentStep === recipe.steps.length - 1}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                下一步
              </button>
            </div>
          </div>

          {/* Feedback Section */}
          <div className="card mt-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              評價這個食譜
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  評分
                </label>
                <div className="flex items-center space-x-2">
                  {[1, 2, 3, 4, 5].map((rating) => (
                    <button
                      key={rating}
                      onClick={() => setFeedback(prev => ({ ...prev, rating }))}
                      className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        rating <= feedback.rating
                          ? 'bg-yellow-400 text-white'
                          : 'bg-gray-200 text-gray-600'
                      }`}
                    >
                      <Star className="w-4 h-4" />
                    </button>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  意見回饋
                </label>
                <textarea
                  value={feedback.comment}
                  onChange={(e) => setFeedback(prev => ({ ...prev, comment: e.target.value }))}
                  placeholder="分享您的烹飪心得..."
                  className="input-field h-24 resize-none"
                />
              </div>
              
              <button
                onClick={submitFeedback}
                className="btn-primary"
              >
                提交回饋
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetailPage;
