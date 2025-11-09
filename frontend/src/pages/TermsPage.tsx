// frontend/src/pages/TermsPage.tsx
import React from 'react';
import { FileText } from 'lucide-react';

const TermsPage = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 flex items-center">
          <FileText className="w-8 h-8 mr-3 text-green-600" />
          使用條款
        </h1>
        <div className="prose prose-lg text-gray-700">
          <p className="mb-4">
            歡迎使用 FridgeSaver！使用本服務即表示您同意以下條款：
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>請上傳真實的食材照片</li>
            <li>食譜建議僅供參考，請依個人健康狀況調整</li>
            <li>我們不保證所有食材都能被正確辨識</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TermsPage;