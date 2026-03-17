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
            <p>👋 Hello! I'm your Smart Campaign Designer assistant.</p>
            <p>You can:</p>
            <ul>
              <li>Upload a source plate file (Excel/CSV)</li>
              <li>Describe your experiment design requirements</li>
              <li>Let me generate an optimized plate layout for you</li>
            </ul>
            <p>Try saying: "Generate a 96-well plate layout with 6 replicates"</p>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              <div className="message-text">{msg.content}</div>
              
              {/* Display associated layout */}
              {msg.layout && (
                <div className="message-layout">
                  <div 
                    className="layout-header"
                    onClick={() => toggleLayout(msg.id)}
                  >
                    <span>🧬 {msg.layout.plateFormat}-Well Plate Layout</span>
                    <span className="layout-toggle">
                      {expandedLayouts.has(msg.id) ? '▼ Collapse' : '▶ Expand'}
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
                        📋 Use This Layout
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
          placeholder="Enter your request..."
          disabled={isLoading}
          className="chat-input"
        />
        {isLoading ? (
          <button type="button" onClick={onStop} className="btn btn-stop">
            ⏹ Stop
          </button>
        ) : (
          <button type="submit" disabled={!input.trim()} className="btn btn-send">
            Send →
          </button>
        )}
      </form>
    </div>
  );
}
