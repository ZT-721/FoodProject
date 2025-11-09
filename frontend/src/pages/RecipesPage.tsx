import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Clock, Star, ChefHat, Filter, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import { searchRecipes, SearchResponse } from '../services/api';

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
}

const RecipesPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [filters, setFilters] = useState({
    cooking_time: '',
    difficulty: '',
    cuisine: ''
  });

  useEffect(() => {
    // 從上傳頁面獲取食材清單
    if (location.state?.ingredients) {
      setIngredients(location.state.ingredients);
      searchForRecipes(location.state.ingredients);
    } else {
      // 如果沒有食材，顯示熱門食譜
      loadPopularRecipes();
    }
  }, [location.state]);

  const searchForRecipes = async (ingredientList: string[]) => {
    setIsLoading(true);
    try {
      const response: SearchResponse = await searchRecipes({
        ingredients: ingredientList,
        preferences: filters
      });
      setRecipes(response.recipes);
    } catch (error) {
      toast.error('搜尋食譜失敗');
    } finally {
      setIsLoading(false);
    }
  };

  const loadPopularRecipes = async () => {
    setIsLoading(true);
    try {
      // 載入熱門食譜
      const mockRecipes: Recipe[] = [
        {
          id: '1',
          name: '番茄炒蛋',
          description: '經典家常菜，簡單易做',
          ingredients: [
            { name: '番茄', amount: '2個', available: true },
            { name: '雞蛋', amount: '3個', available: true },
            { name: '蔥', amount: '1根', available: false, substitute: '洋蔥' }
          ],
          steps: ['將番茄切塊', '打散雞蛋', '熱鍋下蛋液', '加入番茄炒熟'],
          cooking_time: '15分鐘',
          difficulty: '簡單',
          match_percentage: 85
        },
        {
          id: '2',
          name: '青椒肉絲',
          description: '下飯好菜，營養豐富',
          ingredients: [
            { name: '青椒', amount: '2個', available: true },
            { name: '豬肉絲', amount: '200g', available: true },
            { name: '大蒜', amount: '2瓣', available: true }
          ],
          steps: ['青椒切絲', '肉絲醃製', '熱鍋爆香', '炒熟即可'],
          cooking_time: '20分鐘',
          difficulty: '中等',
          match_percentage: 90
        }
      ];
      setRecipes(mockRecipes);
    } catch (error) {
      toast.error('載入食譜失敗');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    
    if (ingredients.length > 0) {
      searchForRecipes(ingredients);
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

  const getMatchColor = (percentage: number) => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          推薦食譜
        </h1>
        
        {ingredients.length > 0 && (
          <div className="mb-4">
            <p className="text-lg text-gray-600 mb-2">基於以下食材推薦：</p>
            <div className="flex flex-wrap gap-2">
              {ingredients.map((ingredient, index) => (
                <span key={index} className="ingredient-tag">
                  {ingredient}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="card mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <Filter className="w-5 h-5 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900">篩選條件</h3>
        </div>
        
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              烹飪時間
            </label>
            <select
              value={filters.cooking_time}
              onChange={(e) => handleFilterChange('cooking_time', e.target.value)}
              className="input-field"
            >
              <option value="">不限</option>
              <option value="15">15分鐘以內</option>
              <option value="30">30分鐘以內</option>
              <option value="60">1小時以內</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              難度等級
            </label>
            <select
              value={filters.difficulty}
              onChange={(e) => handleFilterChange('difficulty', e.target.value)}
              className="input-field"
            >
              <option value="">不限</option>
              <option value="簡單">簡單</option>
              <option value="中等">中等</option>
              <option value="困難">困難</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              菜系
            </label>
            <select
              value={filters.cuisine}
              onChange={(e) => handleFilterChange('cuisine', e.target.value)}
              className="input-field"
            >
              <option value="">不限</option>
              <option value="中式">中式</option>
              <option value="西式">西式</option>
              <option value="日式">日式</option>
              <option value="韓式">韓式</option>
            </select>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="text-center py-12">
          <div className="loading-spinner mx-auto mb-4" />
          <p className="text-gray-600">正在搜尋推薦食譜...</p>
        </div>
      )}

      {/* Recipes Grid */}
      {!isLoading && recipes.length > 0 && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recipes.map((recipe) => (
            <div
              key={recipe.id}
              onClick={() => navigate(`/recipe/${recipe.id}`)}
              className="recipe-card group"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-xl font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                    {recipe.name}
                  </h3>
                  <div className={`text-sm font-medium ${getMatchColor(recipe.match_percentage)}`}>
                    {recipe.match_percentage}% 吻合
                  </div>
                </div>
                
                <p className="text-gray-600 mb-4 line-clamp-2">
                  {recipe.description}
                </p>
                
                <div className="flex items-center space-x-4 mb-4">
                  <div className="flex items-center space-x-1 text-gray-600">
                    <Clock className="w-4 h-4" />
                    <span className="text-sm">{recipe.cooking_time}</span>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(recipe.difficulty)}`}>
                    {recipe.difficulty}
                  </span>
                </div>
                
                <div className="mb-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">主要食材：</p>
                  <div className="flex flex-wrap gap-1">
                    {recipe.ingredients.slice(0, 3).map((ingredient, index) => (
                      <span
                        key={index}
                        className={`text-xs px-2 py-1 rounded ${
                          ingredient.available
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        {ingredient.name}
                      </span>
                    ))}
                    {recipe.ingredients.length > 3 && (
                      <span className="text-xs text-gray-500">
                        +{recipe.ingredients.length - 3} 更多
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="text-sm text-gray-600">4.5</span>
                  </div>
                  <ChefHat className="w-4 h-4 text-gray-400" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!isLoading && recipes.length === 0 && (
        <div className="text-center py-12">
          <ChefHat className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            沒有找到適合的食譜
          </h3>
          <p className="text-gray-600 mb-6">
            試試調整篩選條件或添加更多食材
          </p>
          <button
            onClick={() => navigate('/upload')}
            className="btn-primary"
          >
            重新上傳食材
          </button>
        </div>
      )}
    </div>
  );
};

export default RecipesPage;
