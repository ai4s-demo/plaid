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

  // Switch to confirmation mode if needed
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
          <p>AI-Powered Microplate Layout Design Tool</p>
        </div>

        {error && (
          <div className="auth-error">
            ⚠️ {error}
          </div>
        )}

        {mode === 'confirm' ? (
          <form onSubmit={handleConfirm} className="auth-form">
            <h2>Verify Email</h2>
            <p className="auth-hint">
              A verification code has been sent to {pendingUsername}'s email
            </p>
            
            <div className="form-group">
              <label>Verification Code</label>
              <input
                type="text"
                name="code"
                value={formData.code}
                onChange={handleChange}
                placeholder="Enter 6-digit code"
                required
                autoFocus
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={isLoading}>
              {isLoading ? 'Verifying...' : 'Confirm'}
            </button>

            <p className="auth-switch">
              <button type="button" onClick={() => setMode('signin')}>
                Back to Sign In
              </button>
            </p>
          </form>
        ) : mode === 'signup' ? (
          <form onSubmit={handleSignUp} className="auth-form">
            <h2>Sign Up</h2>
            
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter username"
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter email"
                required
              />
            </div>

            <div className="form-group">
              <label>Name (optional)</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter name"
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Min 8 chars, with upper/lowercase and numbers"
                required
                minLength={8}
              />
            </div>

            <div className="form-group">
              <label>Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Re-enter password"
                required
              />
              {formData.confirmPassword && formData.password !== formData.confirmPassword && (
                <span className="form-error">Passwords do not match</span>
              )}
            </div>

            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={isLoading || formData.password !== formData.confirmPassword}
            >
              {isLoading ? 'Signing up...' : 'Sign Up'}
            </button>

            <p className="auth-switch">
              Already have an account?
              <button type="button" onClick={() => setMode('signin')}>
                Sign In
              </button>
            </p>
          </form>
        ) : (
          <form onSubmit={handleSignIn} className="auth-form">
            <h2>Sign In</h2>
            
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter username"
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter password"
                required
              />
            </div>

            <button type="submit" className="btn btn-primary" disabled={isLoading}>
              {isLoading ? 'Signing in...' : 'Sign In'}
            </button>

            <p className="auth-switch">
              Don't have an account?
              <button type="button" onClick={() => setMode('signup')}>
                Sign Up
              </button>
            </p>
          </form>
        )}
      </div>
    </div>
  );
}
