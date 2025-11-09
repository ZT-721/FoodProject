// 來源: frontend/src/types/Ingredient.ts
// 定義 Ingredient 的資料結構，確保型別安全

export interface Ingredient {
  id: string; // 用於列表渲染的唯一 ID
  name: string; // 食材名稱，例如 'Tomato', 'Eggplant'
  quantity?: string; // 食材的數量或狀態（可選）
}
