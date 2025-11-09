// frontend/src/pages/SafetyPage.tsx
import React from 'react';
import { Shield } from 'lucide-react';

const SafetyPage = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 flex items-center">
          <Shield className="w-8 h-8 mr-3 text-red-600" />
          食品安全聲明
        </h1>
        <div className="prose prose-lg text-gray-700">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <p className="font-semibold text-yellow-800">重要提醒</p>
          </div>
          <ul className="list-disc pl-6 space-y-2">
            <li>請確認食材新鮮度，避免使用變質食物</li>
            <li>過敏原提醒：系統無法偵測堅果、乳製品等過敏原</li>
            <li>烹調時請確保食材充分加熱</li>
            <li>孕婦、幼童、老人請諮詢醫師</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default SafetyPage;