// frontend/src/components/Footer.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, FileText, Lock, Copyright } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-16">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* 品牌區 */}
          <div>
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <Copyright className="w-5 h-5 mr-2" />
              FridgeSaver
            </h3>
            <p className="text-sm">
              用 AI 幫你把冰箱食材變成美味料理，減少食物浪費，愛地球從你開始。
            </p>
          </div>

          {/* 快速連結 */}
          <div>
            <h4 className="text-white font-semibold mb-3">快速連結</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/" className="hover:text-white transition">首頁</Link></li>
              <li><Link to="/upload" className="hover:text-white transition">上傳食材</Link></li>
              <li><Link to="/recipes" className="hover:text-white transition">食譜推薦</Link></li>
            </ul>
          </div>

          {/* 法律與政策 */}
          <div>
            <h4 className="text-white font-semibold mb-3 flex items-center">
              <FileText className="w-4 h-4 mr-2" />
              政策與條款
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/privacy" className="hover:text-white transition flex items-center">
                  <Lock className="w-3 h-3 mr-1" />
                  隱私權政策
                </Link>
              </li>
              <li>
                <Link to="/terms" className="hover:text-white transition">
                  使用條款
                </Link>
              </li>
              <li>
                <Link to="/safety" className="hover:text-white transition flex items-center">
                  <Shield className="w-3 h-3 mr-1" />
                  食品安全聲明
                </Link>
              </li>
            </ul>
          </div>

          {/* 聯絡資訊 */}
          <div>
            <h4 className="text-white font-semibold mb-3">聯絡我們</h4>
            <p className="text-sm">
              <a href="mailto:womenmax@gmail.com" className="hover:text-white transition">
                womenmax@gmail.com
              </a>
            </p>
            <p className="text-xs mt-2 text-gray-500">
              © {new Date().getFullYear()} FridgeSaver. All rights reserved.
            </p>
          </div>
        </div>

        {/* 底部著作權 */}
        <div className="border-t border-gray-800 pt-6 text-center text-xs text-gray-500">
          <p>
            © {new Date().getFullYear()} FridgeSaver. 版權所有。
            <span className="mx-2">|</span>
            由 AI 驅動，致力於減少食物浪費。
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;