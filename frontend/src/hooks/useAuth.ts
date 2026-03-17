import { useState, useEffect, useCallback } from 'react';
import {
  signIn as cognitoSignIn,
  signUp as cognitoSignUp,
  signOut as cognitoSignOut,
  confirmSignUp as cognitoConfirmSignUp,
  getCurrentUser,
  getIdToken,
  type AuthUser,
  type SignInParams,
  type SignUpParams,
} from '../services/auth';
import { isAuthConfigured } from '../config/auth';

interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
  needsConfirmation: boolean;
  pendingUsername: string | null;
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    error: null,
    needsConfirmation: false,
    pendingUsername: null,
  });

  // Check current login status
  useEffect(() => {
    if (!isAuthConfigured()) {
      console.log('[Auth] Auth not configured, skipping');
      setState(prev => ({ ...prev, isLoading: false }));
      return;
    }

    console.log('[Auth] Checking current user...');
    getCurrentUser()
      .then((user) => {
        console.log('[Auth] Current user:', user);
        setState({
          user,
          isLoading: false,
          isAuthenticated: !!user,
          error: null,
          needsConfirmation: false,
          pendingUsername: null,
        });
      })
      .catch((err) => {
        console.log('[Auth] Error getting current user:', err);
        setState(prev => ({
          ...prev,
          isLoading: false,
          isAuthenticated: false,
        }));
      });
  }, []);

  // Sign in
  const signIn = useCallback(async (params: SignInParams) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      console.log('[Auth] Signing in...');
      await cognitoSignIn(params);
      console.log('[Auth] Sign in successful, getting user...');
      const user = await getCurrentUser();
      console.log('[Auth] User:', user);
      
      // Force page reload to ensure state update
      window.location.reload();
    } catch (err: unknown) {
      const error = err as Error;
      let message = error.message || 'Sign in failed';
      
      if (error.name === 'UserNotConfirmedException') {
        setState(prev => ({
          ...prev,
          isLoading: false,
          needsConfirmation: true,
          pendingUsername: params.username,
          error: 'Please verify your email first',
        }));
        return;
      }
      
      if (error.name === 'NotAuthorizedException') {
        message = 'Incorrect username or password';
      }
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: message,
      }));
    }
  }, []);

  // Sign up
  const signUp = useCallback(async (params: SignUpParams) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      await cognitoSignUp(params);
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        needsConfirmation: true,
        pendingUsername: params.username,
      }));
    } catch (err: unknown) {
      const error = err as Error;
      let message = error.message || 'Sign up failed';
      
      if (error.name === 'UsernameExistsException') {
        message = 'Username already exists';
      }
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: message,
      }));
    }
  }, []);

  // Confirm sign up
  const confirmSignUp = useCallback(async (code: string) => {
    if (!state.pendingUsername) return;
    
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      await cognitoConfirmSignUp(state.pendingUsername, code);
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        needsConfirmation: false,
        error: null,
      }));
    } catch (err: unknown) {
      const error = err as Error;
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Verification failed',
      }));
    }
  }, [state.pendingUsername]);

  // Sign out
  const signOut = useCallback(() => {
    cognitoSignOut();
    setState({
      user: null,
      isLoading: false,
      isAuthenticated: false,
      error: null,
      needsConfirmation: false,
      pendingUsername: null,
    });
  }, []);

  // Clear error
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  return {
    ...state,
    signIn,
    signUp,
    confirmSignUp,
    signOut,
    clearError,
    getIdToken,
    isConfigured: isAuthConfigured(),
  };
}
