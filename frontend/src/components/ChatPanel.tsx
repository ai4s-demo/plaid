import { useState, useRef, useEffect } from 'react';
import type { ChatMessage, PlateLayout } from '../types';
import { PlateView } from './PlateView';

interface ChatPanelProps {
  messages: ChatMessage[];
  isLoading: boolean;
  onSend: (message: string) => void;
  onStop: () => void;
  onSelectLayout?: (layout: PlateLayout) => void;
}

export function ChatPanel({ messages, isLoading, onSend, onStop, onSelectLayout }: ChatPanelProps) {
  const [input, setInput] = useState('');
  const [expandedLayouts, setExpandedLayouts] = useState<Set<string>>(new Set());
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSend(input.trim());
      setInput('');
    }
  };

  const toggleLayout = (messageId: string) => {
    setExpandedLayouts(prev => {
      const next = new Set(prev);
      if (next.has(messageId)) {
        next.delete(messageId);
      } else {
        next.add(messageId);
      }
      return next;
    });
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h2>💬 Smart Campaign Designer</h2>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-welcome">
            <p>👋 你好！我是 Smart Campaign Designer 助手。</p>
            <p>你可以：</p>
            <ul>
              <li>上传源板文件（Excel/CSV）</li>
              <li>描述你的实验设计需求</li>
              <li>让我帮你生成优化的板布局</li>
            </ul>
            <p>试试说："帮我生成一个96孔板布局，6个重复"</p>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              <div className="message-text">{msg.content}</div>
              
              {/* 显示关联的布局 */}
              {msg.layout && (
                <div className="message-layout">
                  <div 
                    className="layout-header"
                    onClick={() => toggleLayout(msg.id)}
                  >
                    <span>🧬 {msg.layout.plateFormat}孔板布局</span>
                    <span className="layout-toggle">
                      {expandedLayouts.has(msg.id) ? '▼ 收起' : '▶ 展开'}
                    </span>
                  </div>
                  
                  {expandedLayouts.has(msg.id) && (
                    <div className="layout-preview">
                      <PlateView 
                        layout={msg.layout} 
                        compact={true}
                        onLayoutChange={() => {}}
                      />
                      <button 
                        className="btn btn-select-layout"
                        onClick={() => onSelectLayout?.(msg.layout!)}
                      >
                        📋 使用此布局
                      </button>
                    </div>
                  )}
                </div>
              )}
              
              <div className="message-time">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="chat-message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="输入你的需求..."
          disabled={isLoading}
          className="chat-input"
        />
        {isLoading ? (
          <button type="button" onClick={onStop} className="btn btn-stop">
            ⏹ 停止
          </button>
        ) : (
          <button type="submit" disabled={!input.trim()} className="btn btn-send">
            发送 →
          </button>
        )}
      </form>
    </div>
  );
}
