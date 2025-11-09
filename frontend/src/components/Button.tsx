import React from 'react';

// 定義 Button 組件的屬性 (Props)
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  // 可選的載入狀態
  isLoading?: boolean;
  // 覆蓋預設的 className
  className?: string;
  // 按鈕的子元素 (文字或圖標)
  children: React.ReactNode;
}

/**
 * 通用的按鈕組件，支援載入狀態和 Tailwind CSS 樣式。
 */
const Button: React.FC<ButtonProps> = ({ 
  children, 
  isLoading = false, 
  className = 'px-4 py-2 bg-indigo-600 text-white font-medium rounded-lg shadow-md hover:bg-indigo-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed', 
  disabled, 
  ...rest 
}) => {
  return (
    <button
      className={`flex items-center justify-center space-x-2 ${className}`}
      disabled={disabled || isLoading}
      {...rest}
    >
      {/* 載入指示器 */}
      {isLoading && (
        <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      )}
      {/* 按鈕內容 */}
      <span>{children}</span>
    </button>
  );
};

export default Button;
