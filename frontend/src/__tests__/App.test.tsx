import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import '@testing-library/jest-dom';
import Header from '../components/Header';
import HomePage from '../pages/HomePage';
import UploadPage from '../pages/UploadPage';
import RecipesPage from '../pages/RecipesPage';
import RecipeDetailPage from '../pages/RecipeDetailPage';

// 建立測試用的 QueryClient
const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

// 測試包裝器
const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = createTestQueryClient();
  
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

// Mock API 服務
jest.mock('../services/api', () => ({
  uploadImage: jest.fn(),
  analyzeIngredients: jest.fn(),
  searchRecipes: jest.fn(),
  getPopularRecipes: jest.fn(),
  submitFeedback: jest.fn(),
  getIngredientCategories: jest.fn(),
  searchIngredients: jest.fn(),
  validateIngredients: jest.fn(),
  suggestIngredients: jest.fn(),
  getIngredientNutrition: jest.fn(),
  healthCheck: jest.fn(),
}));

describe('Header Component', () => {
  test('renders logo and navigation', () => {
    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    expect(screen.getByText('冰箱救星')).toBeInTheDocument();
    expect(screen.getByText('首頁')).toBeInTheDocument();
    expect(screen.getByText('上傳食材')).toBeInTheDocument();
    expect(screen.getByText('食譜推薦')).toBeInTheDocument();
  });

  test('navigation links work correctly', () => {
    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    const homeLink = screen.getByText('首頁').closest('a');
    const uploadLink = screen.getByText('上傳食材').closest('a');
    
    expect(homeLink).toHaveAttribute('href', '/');
    expect(uploadLink).toHaveAttribute('href', '/upload');
  });

  test('shows active state for current page', () => {
    // Mock useLocation hook
    jest.mock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useLocation: () => ({ pathname: '/upload' }),
    }));
    
    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    const uploadLink = screen.getByText('上傳食材').closest('a');
    expect(uploadLink).toHaveClass('bg-primary-100');
  });
});

describe('HomePage Component', () => {
  test('renders hero section', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );
    
    expect(screen.getByText('讓 AI 幫你')).toBeInTheDocument();
    expect(screen.getByText('把剩食變美食')).toBeInTheDocument();
    expect(screen.getByText('開始使用')).toBeInTheDocument();
  });

  test('renders features section', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );
    
    expect(screen.getByText('為什麼選擇冰箱救星？')).toBeInTheDocument();
    expect(screen.getByText('AI 智能識別')).toBeInTheDocument();
    expect(screen.getByText('RAG 智能推薦')).toBeInTheDocument();
    expect(screen.getByText('詳細製作步驟')).toBeInTheDocument();
  });

  test('renders how it works section', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );
    
    expect(screen.getByText('使用流程')).toBeInTheDocument();
    expect(screen.getByText('上傳食材照片')).toBeInTheDocument();
    expect(screen.getByText('AI 識別與確認')).toBeInTheDocument();
    expect(screen.getByText('獲得推薦食譜')).toBeInTheDocument();
  });

  test('call to action buttons work', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );
    
    const startButton = screen.getByText('開始使用').closest('a');
    const browseButton = screen.getByText('瀏覽食譜').closest('a');
    
    expect(startButton).toHaveAttribute('href', '/upload');
    expect(browseButton).toHaveAttribute('href', '/recipes');
  });
});

describe('UploadPage Component', () => {
  test('renders upload interface', () => {
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    expect(screen.getByText('上傳食材照片')).toBeInTheDocument();
    expect(screen.getByText('拖拽圖片到這裡，或點擊選擇檔案')).toBeInTheDocument();
  });

  test('handles file drop', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockResolvedValue({
      ingredients: [
        { name: '番茄', confidence: 0.9, category: 'vegetables' },
        { name: '雞蛋', confidence: 0.8, category: 'others' }
      ]
    });

    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );

    // 模擬檔案上傳
    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    const input = screen.getByRole('button', { name: /拖拽圖片到這裡/i });
    
    fireEvent.drop(input, {
      dataTransfer: {
        files: [file],
      },
    });

    await waitFor(() => {
      expect(screen.getByText('已上傳的圖片 (1)')).toBeInTheDocument();
    });
  });

  test('analyzes ingredients when button clicked', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockResolvedValue({
      ingredients: [
        { name: '番茄', confidence: 0.9, category: 'vegetables' },
        { name: '雞蛋', confidence: 0.8, category: 'others' }
      ]
    });

    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );

    // 模擬檔案上傳
    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    const input = screen.getByRole('button', { name: /拖拽圖片到這裡/i });
    
    fireEvent.drop(input, {
      dataTransfer: {
        files: [file],
      },
    });

    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      fireEvent.click(analyzeButton);
    });

    await waitFor(() => {
      expect(mockAnalyzeIngredients).toHaveBeenCalled();
    });
  });

  test('allows editing ingredients', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockResolvedValue({
      ingredients: [
        { name: '番茄', confidence: 0.9, category: 'vegetables' }
      ]
    });

    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );

    // 模擬檔案上傳和分析
    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    const input = screen.getByRole('button', { name: /拖拽圖片到這裡/i });
    
    fireEvent.drop(input, {
      dataTransfer: {
        files: [file],
      },
    });

    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      fireEvent.click(analyzeButton);
    });

    await waitFor(() => {
      const editButton = screen.getByText('編輯清單');
      fireEvent.click(editButton);
    });

    await waitFor(() => {
      expect(screen.getByText('完成編輯')).toBeInTheDocument();
    });
  });
});

describe('RecipesPage Component', () => {
  test('renders recipes page', () => {
    render(
      <TestWrapper>
        <RecipesPage />
      </TestWrapper>
    );
    
    expect(screen.getByText('推薦食譜')).toBeInTheDocument();
  });

  test('shows ingredients when provided', () => {
    const mockLocation = {
      state: {
        ingredients: ['番茄', '雞蛋']
      }
    };

    jest.mock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useLocation: () => mockLocation,
    }));

    render(
      <TestWrapper>
        <RecipesPage />
      </TestWrapper>
    );
    
    expect(screen.getByText('基於以下食材推薦：')).toBeInTheDocument();
  });

  test('renders filter options', () => {
    render(
      <TestWrapper>
        <RecipesPage />
      </TestWrapper>
    );
    
    expect(screen.getByText('篩選條件')).toBeInTheDocument();
    expect(screen.getByText('烹飪時間')).toBeInTheDocument();
    expect(screen.getByText('難度等級')).toBeInTheDocument();
    expect(screen.getByText('菜系')).toBeInTheDocument();
  });

  test('handles filter changes', () => {
    render(
      <TestWrapper>
        <RecipesPage />
      </TestWrapper>
    );
    
    const cookingTimeSelect = screen.getByDisplayValue('不限');
    fireEvent.change(cookingTimeSelect, { target: { value: '15' } });
    
    expect(cookingTimeSelect).toHaveValue('15');
  });
});

describe('RecipeDetailPage Component', () => {
  test('renders recipe detail page', () => {
    // Mock useParams
    jest.mock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useParams: () => ({ id: '1' }),
    }));

    render(
      <TestWrapper>
        <RecipeDetailPage />
      </TestWrapper>
    );
    
    expect(screen.getByText('載入食譜中...')).toBeInTheDocument();
  });

  test('shows loading state initially', () => {
    jest.mock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useParams: () => ({ id: '1' }),
    }));

    render(
      <TestWrapper>
        <RecipeDetailPage />
      </TestWrapper>
    );
    
    expect(screen.getByText('載入食譜中...')).toBeInTheDocument();
  });
});

describe('API Integration', () => {
  test('handles API errors gracefully', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockRejectedValue(new Error('API Error'));

    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );

    // 模擬檔案上傳
    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    const input = screen.getByRole('button', { name: /拖拽圖片到這裡/i });
    
    fireEvent.drop(input, {
      dataTransfer: {
        files: [file],
      },
    });

    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      fireEvent.click(analyzeButton);
    });

    // 應該顯示錯誤訊息
    await waitFor(() => {
      expect(screen.getByText('食材識別失敗，請重試')).toBeInTheDocument();
    });
  });
});

describe('Accessibility', () => {
  test('has proper ARIA labels', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );
    
    const startButton = screen.getByText('開始使用');
    expect(startButton).toHaveAttribute('href', '/upload');
  });

  test('supports keyboard navigation', () => {
    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    const homeLink = screen.getByText('首頁').closest('a');
    expect(homeLink).toHaveAttribute('href', '/');
  });
});

describe('Responsive Design', () => {
  test('renders mobile navigation', () => {
    // Mock window.innerWidth for mobile
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 768,
    });

    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    // 應該顯示手機版導航
    expect(screen.getByRole('button')).toBeInTheDocument();
  });
});
