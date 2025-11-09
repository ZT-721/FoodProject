import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter } from 'react-router-dom';
import UploadPage from '../pages/UploadPage';

// Mock react-dropzone
jest.mock('react-dropzone', () => ({
  useDropzone: () => ({
    getRootProps: () => ({
      'data-testid': 'dropzone',
    }),
    getInputProps: () => ({
      'data-testid': 'file-input',
    }),
    isDragActive: false,
  }),
}));

// Mock react-hot-toast
jest.mock('react-hot-toast', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
  },
}));

// Mock API services
jest.mock('../services/api', () => ({
  analyzeIngredients: jest.fn(),
}));

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

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

describe('UploadPage Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders upload interface correctly', () => {
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    expect(screen.getByText('上傳食材照片')).toBeInTheDocument();
    expect(screen.getByText('拍攝或上傳冰箱中剩餘食材的照片，AI 將自動識別食材種類')).toBeInTheDocument();
  });

  test('shows file upload zone', () => {
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    expect(screen.getByTestId('dropzone')).toBeInTheDocument();
    expect(screen.getByTestId('file-input')).toBeInTheDocument();
  });

  test('handles file selection', async () => {
    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    
    await user.upload(fileInput, file);
    
    // 應該顯示已上傳的檔案
    await waitFor(() => {
      expect(screen.getByText('已上傳的圖片 (1)')).toBeInTheDocument();
    });
  });

  test('analyzes ingredients when analyze button is clicked', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockResolvedValue({
      ingredients: [
        { name: '番茄', confidence: 0.9, category: 'vegetables' },
        { name: '雞蛋', confidence: 0.8, category: 'others' }
      ]
    });

    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    // 上傳檔案
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    await user.upload(fileInput, file);
    
    // 點擊分析按鈕
    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      user.click(analyzeButton);
    });
    
    await waitFor(() => {
      expect(mockAnalyzeIngredients).toHaveBeenCalled();
    });
  });

  test('shows loading state during analysis', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ingredients: [{ name: '番茄', confidence: 0.9, category: 'vegetables' }]
      }), 1000))
    );

    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    // 上傳檔案
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    await user.upload(fileInput, file);
    
    // 點擊分析按鈕
    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      user.click(analyzeButton);
    });
    
    // 應該顯示載入狀態
    await waitFor(() => {
      expect(screen.getByText('分析中...')).toBeInTheDocument();
    });
  });

  test('displays analyzed ingredients', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockResolvedValue({
      ingredients: [
        { name: '番茄', confidence: 0.9, category: 'vegetables' },
        { name: '雞蛋', confidence: 0.8, category: 'others' }
      ]
    });

    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    // 上傳檔案並分析
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    await user.upload(fileInput, file);
    
    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      user.click(analyzeButton);
    });
    
    // 應該顯示識別到的食材
    await waitFor(() => {
      expect(screen.getByText('識別到的食材 (2)')).toBeInTheDocument();
      expect(screen.getByText('番茄')).toBeInTheDocument();
      expect(screen.getByText('雞蛋')).toBeInTheDocument();
    });
  });

  test('allows editing ingredients', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockResolvedValue({
      ingredients: [
        { name: '番茄', confidence: 0.9, category: 'vegetables' }
      ]
    });

    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    // 上傳檔案並分析
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    await user.upload(fileInput, file);
    
    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      user.click(analyzeButton);
    });
    
    // 點擊編輯按鈕
    await waitFor(() => {
      const editButton = screen.getByText('編輯清單');
      user.click(editButton);
    });
    
    // 應該顯示編輯模式
    await waitFor(() => {
      expect(screen.getByText('完成編輯')).toBeInTheDocument();
    });
  });

  test('handles analysis errors', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockRejectedValue(new Error('API Error'));

    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    // 上傳檔案
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    await user.upload(fileInput, file);
    
    // 點擊分析按鈕
    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      user.click(analyzeButton);
    });
    
    // 應該顯示錯誤訊息
    await waitFor(() => {
      expect(screen.getByText('食材識別失敗，請重試')).toBeInTheDocument();
    });
  });

  test('proceeds to recipes page with ingredients', async () => {
    const mockAnalyzeIngredients = require('../services/api').analyzeIngredients;
    mockAnalyzeIngredients.mockResolvedValue({
      ingredients: [
        { name: '番茄', confidence: 0.9, category: 'vegetables' }
      ]
    });

    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    // 上傳檔案並分析
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['test content'], 'test.jpg', { type: 'image/jpeg' });
    await user.upload(fileInput, file);
    
    await waitFor(() => {
      const analyzeButton = screen.getByText('開始分析食材');
      user.click(analyzeButton);
    });
    
    // 點擊查看推薦食譜按鈕
    await waitFor(() => {
      const proceedButton = screen.getByText('查看推薦食譜');
      user.click(proceedButton);
    });
    
    // 應該導航到食譜頁面
    await waitFor(() => {
      expect(window.location.pathname).toBe('/recipes');
    });
  });

  test('validates file types', async () => {
    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    const fileInput = screen.getByTestId('file-input');
    const invalidFile = new File(['test content'], 'test.txt', { type: 'text/plain' });
    
    await user.upload(fileInput, invalidFile);
    
    // 應該顯示錯誤訊息
    await waitFor(() => {
      expect(screen.getByText('部分檔案格式不支援或檔案過大')).toBeInTheDocument();
    });
  });

  test('handles multiple file uploads', async () => {
    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <UploadPage />
      </TestWrapper>
    );
    
    const fileInput = screen.getByTestId('file-input');
    const file1 = new File(['test content 1'], 'test1.jpg', { type: 'image/jpeg' });
    const file2 = new File(['test content 2'], 'test2.jpg', { type: 'image/jpeg' });
    
    await user.upload(fileInput, [file1, file2]);
    
    // 應該顯示已上傳的檔案數量
    await waitFor(() => {
      expect(screen.getByText('已上傳的圖片 (2)')).toBeInTheDocument();
    });
  });
});
