import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Camera, Image as ImageIcon, CheckCircle, XCircle, Search, Trash2, ChefHat } from 'lucide-react'; // <-- 這裡加入了 ChefHat
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';

// 導入本地組件
import IngredientList from '../components/IngredientList';
import Button from '../components/Button';
import { Ingredient } from '../types/Ingredient'; // <--- 這裡已經修正！

// 假設您的上傳圖片限制為 10MB
const MAX_FILE_SIZE = 10 * 1024 * 1024;


/**
 * 食材上傳與分析頁面
 */
const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  // --- Dropzone 邏輯 ---
  const onDrop = useCallback((acceptedFiles: File[], fileRejections: any[]) => {
    if (fileRejections.length > 0) {
      toast.error('檔案太大或格式不正確，請選擇小於 10MB 的圖片 (jpg/png)。');
      setFile(null);
      return;
    }

    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setIngredients([]); // 清空舊的分析結果
      toast.success(`圖片已載入: ${acceptedFiles[0].name}`);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpeg', '.jpg'],
      'image/png': ['.png'],
    },
    maxSize: MAX_FILE_SIZE,
    maxFiles: 1,
  });

  const handleAnalyze = async () => {
  if (!file) {
    toast.warn('請先上傳一張食材圖片。');
    return;
  }

  setIsLoading(true);
  setIngredients([]);

  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error('分析失敗');

    const data = await response.json();

    // 轉換後端格式 → 前端 Ingredient[]
    const formattedIngredients: Ingredient[] = data.ingredients.map((ing: any, index: number) => ({
      id: ing.id || `mock-${index}`,
      name: ing.name,
      quantity: ing.quantity || '',
    }));

    setIngredients(formattedIngredients);
    toast.success('食材分析完成！請確認結果。');
  } catch (error) {
    console.error('API Error:', error);
    toast.error('分析失敗，請稍後再試。');
  } finally {
    setIsLoading(false);
  }
};
  
  // --- 清空所有狀態 ---
  const handleClearAll = () => {
      setFile(null);
      setIngredients([]);
      setIsLoading(false);
      toast.info('所有狀態已清除。');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <ToastContainer position="top-center" autoClose={3000} hideProgressBar newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />

      <h1 className="text-3xl font-extrabold text-gray-900 mb-6 flex items-center">
        <Camera className="w-8 h-8 mr-3 text-indigo-600" />
        上傳食材並進行 AI 分析
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 左側: 圖片上傳區域 */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold mb-4 border-b pb-2 text-gray-700">1. 上傳圖片</h2>
          
          <div 
            {...getRootProps()} 
            className={`
              flex flex-col items-center justify-center p-10 border-2 border-dashed rounded-lg cursor-pointer transition-colors duration-200 
              ${isDragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-gray-400'}
            `}
            style={{ minHeight: '200px' }}
          >
            <input {...getInputProps()} />
            {file ? (
              <div className="text-center">
                <CheckCircle className="w-8 h-8 mx-auto text-green-500 mb-2" />
                <p className="text-sm font-medium text-gray-700">圖片已載入: {file.name}</p>
                <p className="text-xs text-gray-500 mt-1">點擊或拖曳其他圖片來替換</p>
              </div>
            ) : (
              <div className="text-center">
                <ImageIcon className="w-8 h-8 mx-auto text-gray-400 mb-2" />
                <p className="text-lg font-medium text-gray-700">拖曳圖片到此處，或點擊上傳</p>
                <p className="text-sm text-gray-500 mt-1">僅限 JPG 或 PNG 格式 (最大 10MB)</p>
              </div>
            )}
          </div>
          
          {file && (
            <div className="mt-4 flex justify-between items-center">
                <p className="text-sm text-gray-600">已選圖片: {file.name}</p>
                <Button 
                    onClick={handleClearAll} 
                    className="bg-gray-200 text-gray-700 hover:bg-gray-300 px-3 py-1 text-sm"
                >
                    <Trash2 className="w-4 h-4 mr-1" /> 清除
                </Button>
            </div>
          )}

          <Button
            onClick={handleAnalyze}
            isLoading={isLoading}
            disabled={!file}
            className="w-full mt-6 flex items-center justify-center space-x-2 px-4 py-3 text-lg bg-indigo-600 hover:bg-indigo-700 rounded-xl"
          >
            <Search className="w-5 h-5" />
            <span>{isLoading ? '分析中...' : '2. 開始分析食材'}</span>
          </Button>
        </div>

        {/* 右側: 食材清單結果 */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold mb-4 border-b pb-2 text-gray-700">3. 確認與編輯食材清單</h2>
          
          <IngredientList ingredients={ingredients} setIngredients={setIngredients} />

          <Button
            onClick={() => {
              if (ingredients.length === 0) {
                toast.warn('請先分析食材！');
                return;
              }
              // 這裡應該是導航到食譜推薦頁面，並傳遞食材數據
              console.log('Final Ingredients to use:', ingredients);
              toast.success('食材已確認，準備導航到食譜推薦頁...');
              navigate('/recipes', { state: { ingredients } });
            }}
            disabled={ingredients.length === 0}
            className="w-full mt-6 flex items-center justify-center space-x-2 px-4 py-3 text-lg bg-green-600 hover:bg-green-700 rounded-xl"
          >
            <ChefHat className="w-5 h-5" />
            <span>4. 查找食譜</span>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
