import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

type AuthMode = 'signin' | 'signup' | 'confirm';

export function AuthPage() {
  const {
    isLoading,
    error,
    needsConfirmation,
    pendingUsername,
    signIn,
    signUp,
    confirmSignUp,
    clearError,
  } = useAuth();

  const [mode, setMode] = useState<AuthMode>('signin');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    code: '',
  });

  // 如果需要确认，切换到确认模式
  if (needsConfirmation && mode !== 'confirm') {
    setMode('confirm');
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
    clearError();
  };

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    await signIn({
      username: formData.username,
      password: formData.password,
    });
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      return;
    }
    
    await signUp({
      username: formData.username,
      email: formData.email,
      password: formData.password,
      name: formData.name || undefined,
    });
  };

  const handleConfirm = async (e: React.FormEvent) => {
    e.preventDefault();
    await confirmSignUp(formData.code);
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1>🧬 Smart Campaign Designer</h1>
          <p>AI 驱动的微孔板布局设计工具</p>
        </div>

        {error && (
          <div className="auth-error">
            ⚠️ {error}
          </div>
        )}

        {mode === 'confirm' ? (
          <form onSubmit={handleConfirm} className="auth-form">
            <h2>验证邮箱</h2>
            <p className="auth-hint">
              验证码已发送到 {pendingUsername} 的邮箱
            </p>
            
            <div className="form-group">
              <label>验证码</label>
              <input
                type="text"
                name="code"
                value={formData.code}
                onChange={handleChange}
                placeholder="输入6位验证码"
                required
                autoFocus
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={isLoading}>
              {isLoading ? '验证中...' : '确认'}
            </button>

            <p className="auth-switch">
              <button type="button" onClick={() => setMode('signin')}>
                返回登录
              </button>
            </p>
          </form>
        ) : mode === 'signup' ? (
          <form onSubmit={handleSignUp} className="auth-form">
            <h2>注册账号</h2>
            
            <div className="form-group">
              <label>用户名</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="输入用户名"
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <label>邮箱</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="输入邮箱"
                required
              />
            </div>

            <div className="form-group">
              <label>姓名（可选）</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="输入姓名"
              />
            </div>

            <div className="form-group">
              <label>密码</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="至少8位，包含大小写字母和数字"
                required
                minLength={8}
              />
            </div>

            <div className="form-group">
              <label>确认密码</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="再次输入密码"
                required
              />
              {formData.confirmPassword && formData.password !== formData.confirmPassword && (
                <span className="form-error">密码不匹配</span>
              )}
            </div>

            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={isLoading || formData.password !== formData.confirmPassword}
            >
              {isLoading ? '注册中...' : '注册'}
            </button>

            <p className="auth-switch">
              已有账号？
              <button type="button" onClick={() => setMode('signin')}>
                登录
              </button>
            </p>
          </form>
        ) : (
          <form onSubmit={handleSignIn} className="auth-form">
            <h2>登录</h2>
            
            <div className="form-group">
              <label>用户名</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="输入用户名"
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <label>密码</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="输入密码"
                required
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={isLoading}>
              {isLoading ? '登录中...' : '登录'}
            </button>

            <p className="auth-switch">
              没有账号？
              <button type="button" onClick={() => setMode('signup')}>
                注册
              </button>
            </p>
          </form>
        )}
      </div>
    </div>
  );
}
