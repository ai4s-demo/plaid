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

  // 检查当前登录状态
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

  // 登录
  const signIn = useCallback(async (params: SignInParams) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      console.log('[Auth] Signing in...');
      await cognitoSignIn(params);
      console.log('[Auth] Sign in successful, getting user...');
      const user = await getCurrentUser();
      console.log('[Auth] User:', user);
      
      // 强制刷新页面以确保状态更新
      window.location.reload();
    } catch (err: unknown) {
      const error = err as Error;
      let message = error.message || '登录失败';
      
      if (error.name === 'UserNotConfirmedException') {
        setState(prev => ({
          ...prev,
          isLoading: false,
          needsConfirmation: true,
          pendingUsername: params.username,
          error: '请先验证邮箱',
        }));
        return;
      }
      
      if (error.name === 'NotAuthorizedException') {
        message = '用户名或密码错误';
      }
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: message,
      }));
    }
  }, []);

  // 注册
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
      let message = error.message || '注册失败';
      
      if (error.name === 'UsernameExistsException') {
        message = '用户名已存在';
      }
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: message,
      }));
    }
  }, []);

  // 确认注册
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
        error: error.message || '验证失败',
      }));
    }
  }, [state.pendingUsername]);

  // 登出
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

  // 清除错误
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
