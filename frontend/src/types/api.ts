// frontend/src/types/api.ts
export interface Ingredient {
  name: string;
  confidence: number;
  category: string;
}

export interface Recipe {
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

export interface AnalyzeResponse {
  ingredients: Ingredient[];
  success: boolean;
  total_images: number;
}

export interface SearchResponse {
  recipes: Recipe[];
  success: boolean;
}