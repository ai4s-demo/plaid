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
    allLayouts: [],
    currentPlateIndex: 0,
    parameters: DEFAULT_PARAMETERS,
    messages: [],
    isLoading: false,
    error: null,
  });

  const abortRef = useRef<(() => void) | null>(null);
  
  // Use ref to keep latest state reference
  const stateRef = useRef(state);
  stateRef.current = state;

  // Send message
  const sendMessage = useCallback(async (content: string) => {
    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    const assistantId = generateId();
    let assistantContent = '';
    
    // Get the latest messages
    const currentMessages = stateRef.current.messages;
    const messagesWithUser = [...currentMessages, userMessage];
    
    // Build history to send to backend
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
      // onLayout - attach layout to the current assistant message
      (layout) => {
        setState((prev) => ({
          ...prev,
          currentLayout: layout,
          allLayouts: [layout],
          currentPlateIndex: 0,
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
      },
      // onLayouts - multiple plates
      (layouts) => {
        setState((prev) => ({
          ...prev,
          allLayouts: layouts,
          currentLayout: layouts[0],
          currentPlateIndex: 0,
          messages: prev.messages.map((m) =>
            m.id === assistantId ? { ...m, layouts } : m
          ),
        }));
      }
    );

    abortRef.current = abort;
  }, []);

  // Stop generation
  const stopGeneration = useCallback(() => {
    if (abortRef.current) {
      abortRef.current();
      abortRef.current = null;
      setState((prev) => ({ ...prev, isLoading: false }));
    }
  }, []);

  // Upload file
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
      const message = err instanceof Error ? err.message : 'File parsing failed';
      setState((prev) => ({ ...prev, error: message, isLoading: false }));
      throw err;
    }
  }, []);

  // Generate layout
  const createLayout = useCallback(async () => {
    if (!state.sourcePlate) {
      setState((prev) => ({ ...prev, error: 'Please upload a source plate file first' }));
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
      const message = err instanceof Error ? err.message : 'Layout generation failed';
      setState((prev) => ({ ...prev, error: message, isLoading: false }));
      throw err;
    }
  }, [state.sourcePlate, state.parameters]);

  // Update parameters
  const updateParameters = useCallback((params: Partial<DesignParameters>) => {
    setState((prev) => ({
      ...prev,
      parameters: { ...prev.parameters, ...params },
    }));
  }, []);

  // Update layout (after drag)
  const updateLayout = useCallback((layout: PlateLayout) => {
    setState((prev) => ({ ...prev, currentLayout: layout }));
  }, []);

  // Switch between plates
  const switchPlate = useCallback((index: number) => {
    setState((prev) => {
      if (index < 0 || index >= prev.allLayouts.length) return prev;
      return {
        ...prev,
        currentPlateIndex: index,
        currentLayout: prev.allLayouts[index],
      };
    });
  }, []);

  // Clear error
  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  // Reset
  const reset = useCallback(() => {
    setState({
      sourcePlate: null,
      currentLayout: null,
      allLayouts: [],
      currentPlateIndex: 0,
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
    switchPlate,
    clearError,
    reset,
  };
}
