import React from 'react';
import { Ingredient } from '../types/Ingredient'; // 從 types/Ingredient.ts 導入類型
import { toast } from 'react-toastify';

// 定義 IngredientList 組件的屬性 (Props) 介面
interface IngredientListProps {
  ingredients: Ingredient[];
  setIngredients: React.Dispatch<React.SetStateAction<Ingredient[]>>;
}

/**
 * 顯示和管理 AI 識別出的食材清單。
 * 允許使用者編輯名稱、數量或刪除食材。
 */
const IngredientList: React.FC<IngredientListProps> = ({ ingredients, setIngredients }) => {
  
  // 當食材清單為空時的顯示內容
  if (ingredients.length === 0) {
    return (
      <div className="text-center p-8 border border-dashed rounded-lg text-gray-500 bg-gray-50">
        目前沒有識別到的食材。請上傳圖片並點擊「開始分析食材」。
      </div>
    );
  }

  // 處理食材名稱變更的函式
  const handleNameChange = (id: string, newName: string) => {
    setIngredients(prevIngredients =>
      prevIngredients.map(ing =>
        ing.id === id ? { ...ing, name: newName } : ing
      )
    );
  };

  // 處理食材數量/狀態變更的函式
  const handleQuantityChange = (id: string, newQuantity: string) => {
    setIngredients(prevIngredients =>
      prevIngredients.map(ing =>
        ing.id === id ? { ...ing, quantity: newQuantity } : ing
      )
    );
  };

  // 處理刪除食材的函式
  const handleDelete = (id: string) => {
    setIngredients(prevIngredients => {
      const newIngredients = prevIngredients.filter(ing => ing.id !== id);
      // 顯示通知
      toast.info(`已移除食材: ${prevIngredients.find(ing => ing.id === id)?.name}`);
      return newIngredients;
    });
  };

  return (
    <div className="bg-white shadow-lg rounded-xl p-4">
      {/* 遍歷並渲染每個食材項目 */}
      {ingredients.map((ingredient) => (
        <div 
          key={ingredient.id} 
          className="flex flex-col sm:flex-row items-start sm:items-center p-3 border-b last:border-b-0 space-y-2 sm:space-y-0 sm:space-x-4 transition duration-150 ease-in-out hover:bg-indigo-50"
        >
          {/* 食材名稱輸入欄位 */}
          <div className="flex-1 w-full">
            <label htmlFor={`name-${ingredient.id}`} className="sr-only">食材名稱</label>
            <input
              id={`name-${ingredient.id}`}
              type="text"
              value={ingredient.name}
              onChange={(e) => handleNameChange(ingredient.id, e.target.value)}
              className="w-full border border-gray-300 rounded-lg p-2 text-gray-800 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="輸入食材名稱"
            />
          </div>

          {/* 數量/狀態輸入欄位 (可選) */}
          <div className="flex-1 w-full sm:w-auto">
            <label htmlFor={`qty-${ingredient.id}`} className="sr-only">數量/狀態</label>
            <input
              id={`qty-${ingredient.id}`}
              type="text"
              value={ingredient.quantity || ''}
              onChange={(e) => handleQuantityChange(ingredient.id, e.target.value)}
              className="w-full border border-gray-300 rounded-lg p-2 text-gray-600 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="數量或狀態 (可選)"
            />
          </div>

          {/* 刪除按鈕 */}
          <button
            onClick={() => handleDelete(ingredient.id)}
            className="flex-shrink-0 bg-red-500 text-white rounded-lg p-2 hover:bg-red-600 transition-colors shadow-sm"
            aria-label={`移除 ${ingredient.name}`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      ))}
    </div>
  );
};

export default IngredientList;
