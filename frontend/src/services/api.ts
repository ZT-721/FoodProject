import axios from 'axios';
import { AnalyzeResponse, SearchResponse } from '../types/api';

// API 基礎設定
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    // 可以在這裡添加認證 token
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 回應攔截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    throw error;
  }
);

// Vision API 相關
export const uploadImage = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return api.post('/vision/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const analyzeIngredients = async (formData: FormData): Promise<AnalyzeResponse> => {
  return api.post('/vision/batch-upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

// Recipes API 相關
export const searchRecipes = async (data: {
  ingredients: string[];
  preferences?: { cooking_time?: string; difficulty?: string; cuisine?: string };
}): Promise<SearchResponse> => {
  return api.post<SearchResponse>('/recipes/search', data);
};

export const getPopularRecipes = async () => {
  return api.get('/recipes/popular');
};

export const submitFeedback = async (data: {
  recipe_id: string;
  rating: number;
  comment: string;
}) => {
  return api.post('/recipes/feedback', data);
};

// Ingredients API 相關
export const getIngredientCategories = async () => {
  return api.get('/ingredients/categories');
};

export const searchIngredients = async (query: string, category?: string) => {
  const params = new URLSearchParams({ q: query });
  if (category) params.append('category', category);
  
  return api.get(`/ingredients/search?${params}`);
};

export const validateIngredients = async (ingredients: string[]) => {
  return api.post('/ingredients/validate', { ingredients });
};

export const suggestIngredients = async (ingredients: string[]) => {
  return api.post('/ingredients/suggest', { ingredients });
};

export const getIngredientNutrition = async (ingredient: string) => {
  return api.get(`/ingredients/nutrition/${encodeURIComponent(ingredient)}`);
};

// 健康檢查
export const healthCheck = async () => {
  return api.get('/health');
};

export default api;
