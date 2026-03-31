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
    allLayouts,
    currentPlateIndex,
    messages,
    isLoading,
    error,
    sendMessage,
    stopGeneration,
    uploadFile,
    updateLayout,
    switchPlate,
    clearError,
  } = useChat();

  // Select a layout from chat history
  const handleSelectLayout = (layout: PlateLayout) => {
    updateLayout(layout);
  };

  // Authentication loading
  if (authLoading) {
    return (
      <div className="app loading-screen">
        <div className="loading-content">
          <span className="loading-icon">🧬</span>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  // If auth is configured but user is not signed in, show login page
  if (authConfigured && !isAuthenticated) {
    return <AuthPage />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧬 Smart Campaign Designer</h1>
        <div className="header-right">
          <p>AI-Powered Microplate Layout Design Tool</p>
          {isAuthenticated && user && (
            <div className="user-info">
              <span>👤 {user.name || user.username}</span>
              <button className="btn btn-logout" onClick={signOut}>
                Sign Out
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
          {allLayouts.length > 1 && (
            <div className="plate-tabs">
              {allLayouts.map((_, i) => (
                <button
                  key={i}
                  className={`plate-tab ${i === currentPlateIndex ? 'active' : ''}`}
                  onClick={() => switchPlate(i)}
                >
                  Plate {i + 1}
                </button>
              ))}
            </div>
          )}
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
        <p>Powered by Amazon Bedrock & MiniZinc | PLAID Methodology</p>
      </footer>
    </div>
  );
}

export default App;
