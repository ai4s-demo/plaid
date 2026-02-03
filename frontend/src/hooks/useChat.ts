import { useState, useCallback, useRef } from 'react';
import type {
  ChatMessage,
  PlateLayout,
  DesignParameters,
  AppState,
} from '../types';
import { DEFAULT_PARAMETERS } from '../types';
import { createChatStream, parseFile, generateLayout } from '../services/api';

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export function useChat() {
  const [state, setState] = useState<AppState>({
    sourcePlate: null,
    currentLayout: null,
    parameters: DEFAULT_PARAMETERS,
    messages: [],
    isLoading: false,
    error: null,
  });

  const abortRef = useRef<(() => void) | null>(null);
  
  // 使用 ref 保持最新状态引用
  const stateRef = useRef(state);
  stateRef.current = state;

  // 发送消息
  const sendMessage = useCallback(async (content: string) => {
    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    const assistantId = generateId();
    let assistantContent = '';
    
    // 获取当前最新的 messages
    const currentMessages = stateRef.current.messages;
    const messagesWithUser = [...currentMessages, userMessage];
    
    // 构建发送给后端的历史记录
    const historyForBackend = messagesWithUser.slice(-10).map(m => ({
      role: m.role,
      content: m.content,
    }));

    setState((prev) => ({
      ...prev,
      messages: [
        ...messagesWithUser,
        {
          id: assistantId,
          role: 'assistant',
          content: '',
          timestamp: new Date().toISOString(),
        },
      ],
      isLoading: true,
      error: null,
    }));

    const abort = createChatStream(
      {
        message: content,
        context: {
          sourcePlate: stateRef.current.sourcePlate,
          currentLayout: stateRef.current.currentLayout,
          parameters: stateRef.current.parameters,
        },
        history: historyForBackend,
      },
      // onMessage
      (text) => {
        assistantContent += text;
        setState((prev) => ({
          ...prev,
          messages: prev.messages.map((m) =>
            m.id === assistantId ? { ...m, content: assistantContent } : m
          ),
        }));
      },
      // onLayout - 将布局附加到当前助手消息
      (layout) => {
        setState((prev) => ({
          ...prev,
          currentLayout: layout,
          messages: prev.messages.map((m) =>
            m.id === assistantId ? { ...m, layout } : m
          ),
        }));
      },
      // onError
      (error) => {
        setState((prev) => ({
          ...prev,
          error,
          isLoading: false,
        }));
      },
      // onDone
      () => {
        setState((prev) => ({
          ...prev,
          isLoading: false,
        }));
      }
    );

    abortRef.current = abort;
  }, []);

  // 停止生成
  const stopGeneration = useCallback(() => {
    if (abortRef.current) {
      abortRef.current();
      abortRef.current = null;
      setState((prev) => ({ ...prev, isLoading: false }));
    }
  }, []);

  // 上传文件
  const uploadFile = useCallback(async (file: File) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));
    try {
      const sourcePlate = await parseFile(file);
      setState((prev) => ({
        ...prev,
        sourcePlate,
        isLoading: false,
      }));
      return sourcePlate;
    } catch (err) {
      const message = err instanceof Error ? err.message : '文件解析失败';
      setState((prev) => ({ ...prev, error: message, isLoading: false }));
      throw err;
    }
  }, []);

  // 生成布局
  const createLayout = useCallback(async () => {
    if (!state.sourcePlate) {
      setState((prev) => ({ ...prev, error: '请先上传源板文件' }));
      return;
    }
    setState((prev) => ({ ...prev, isLoading: true, error: null }));
    try {
      const layout = await generateLayout({
        sourcePlate: state.sourcePlate,
        parameters: state.parameters,
      });
      setState((prev) => ({
        ...prev,
        currentLayout: layout,
        isLoading: false,
      }));
      return layout;
    } catch (err) {
      const message = err instanceof Error ? err.message : '布局生成失败';
      setState((prev) => ({ ...prev, error: message, isLoading: false }));
      throw err;
    }
  }, [state.sourcePlate, state.parameters]);

  // 更新参数
  const updateParameters = useCallback((params: Partial<DesignParameters>) => {
    setState((prev) => ({
      ...prev,
      parameters: { ...prev.parameters, ...params },
    }));
  }, []);

  // 更新布局（拖拽后）
  const updateLayout = useCallback((layout: PlateLayout) => {
    setState((prev) => ({ ...prev, currentLayout: layout }));
  }, []);

  // 清除错误
  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  // 重置
  const reset = useCallback(() => {
    setState({
      sourcePlate: null,
      currentLayout: null,
      parameters: DEFAULT_PARAMETERS,
      messages: [],
      isLoading: false,
      error: null,
    });
  }, []);

  return {
    ...state,
    sendMessage,
    stopGeneration,
    uploadFile,
    createLayout,
    updateParameters,
    updateLayout,
    clearError,
    reset,
  };
}
