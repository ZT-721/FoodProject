import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import RecipesPage from './pages/RecipesPage';
import RecipeDetailPage from './pages/RecipeDetailPage';
import PrivacyPage from './pages/PrivacyPage';
import TermsPage from './pages/TermsPage';
import SafetyPage from './pages/SafetyPage';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header 固定在上方 */}
      <Header />

      {/* 主要內容區，flex-grow 讓它撐開 */}
      <main className="flex-grow container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/recipes" element={<RecipesPage />} />
          <Route path="/recipe/:id" element={<RecipeDetailPage />} />
          
          {/* 新增三個政策頁面路由 */}
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="/terms" element={<TermsPage />} />
          <Route path="/safety" element={<SafetyPage />} />
        </Routes>
      </main>

      {/* Footer 固定在底部 */}
      <Footer />
    </div>
  );
}

export default App;
