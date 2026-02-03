import { useChat } from './hooks/useChat';
import { useAuth } from './hooks/useAuth';
import { ChatPanel } from './components/ChatPanel';
import { FileUpload } from './components/FileUpload';
import { PlateView } from './components/PlateView';
import { DownloadPanel } from './components/DownloadPanel';
import { AuthPage } from './components/AuthPage';
import type { PlateLayout } from './types';
import './index.css';

function App() {
  const {
    user,
    isLoading: authLoading,
    isAuthenticated,
    signOut,
    isConfigured: authConfigured,
  } = useAuth();

  const {
    sourcePlate,
    currentLayout,
    messages,
    isLoading,
    error,
    sendMessage,
    stopGeneration,
    uploadFile,
    updateLayout,
    clearError,
  } = useChat();

  // 从聊天历史中选择一个布局
  const handleSelectLayout = (layout: PlateLayout) => {
    updateLayout(layout);
  };

  // 认证加载中
  if (authLoading) {
    return (
      <div className="app loading-screen">
        <div className="loading-content">
          <span className="loading-icon">🧬</span>
          <p>加载中...</p>
        </div>
      </div>
    );
  }

  // 如果配置了认证但未登录，显示登录页
  if (authConfigured && !isAuthenticated) {
    return <AuthPage />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧬 Smart Campaign Designer</h1>
        <div className="header-right">
          <p>AI 驱动的微孔板布局设计工具</p>
          {isAuthenticated && user && (
            <div className="user-info">
              <span>👤 {user.name || user.username}</span>
              <button className="btn btn-logout" onClick={signOut}>
                退出
              </button>
            </div>
          )}
        </div>
      </header>

      {error && (
        <div className="error-banner" onClick={clearError}>
          ⚠️ {error}
          <button className="close-btn">×</button>
        </div>
      )}

      <main className="app-main">
        <aside className="sidebar">
          <FileUpload
            sourcePlate={sourcePlate}
            isLoading={isLoading}
            onUpload={uploadFile}
          />
          <DownloadPanel layout={currentLayout} sourcePlate={sourcePlate} />
        </aside>

        <section className="content">
          <div className="plate-container">
            <PlateView layout={currentLayout} onLayoutChange={updateLayout} />
          </div>
        </section>

        <aside className="chat-sidebar">
          <ChatPanel
            messages={messages}
            isLoading={isLoading}
            onSend={sendMessage}
            onStop={stopGeneration}
            onSelectLayout={handleSelectLayout}
          />
        </aside>
      </main>

      <footer className="app-footer">
        <p>Powered by Amazon Bedrock & OR-Tools | PLAID Methodology</p>
      </footer>
    </div>
  );
}

export default App;
