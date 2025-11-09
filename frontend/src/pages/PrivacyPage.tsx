// frontend/src/pages/PrivacyPage.tsx
import React from 'react';
import { Lock } from 'lucide-react';

const PrivacyPage = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 flex items-center">
          <Lock className="w-8 h-8 mr-3 text-indigo-600" />
          隱私權政策
        </h1>
        <div className="prose prose-lg text-gray-700">
          <p className="mb-4">
            最後更新：{new Date().toLocaleDateString('zh-TW')}
          </p>
          <p className="mb-4">
            FridgeSaver 非常重視您的隱私。我們僅收集上傳的食材照片用於 AI 分析，並在處理後立即刪除。
          </p>
          <h3 className="text-xl font-semibold mt-6 mb-3">我們收集的資料</h3>
          <ul className="list-disc pl-6 mb-4">
            <li>上傳的冰箱或食材照片（僅暫存）</li>
            <li>AI 辨識出的食材清單</li>
            <li>瀏覽器基本資訊（用於改善體驗）</li>
          </ul>
          <p className="text-sm text-gray-500 mt-8">
            如有疑問，請聯絡：support@fridgesaver.com
          </p>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPage;