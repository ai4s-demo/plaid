import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
  CognitoUserAttribute,
  CognitoUserSession,
} from 'amazon-cognito-identity-js';
import { AUTH_CONFIG } from '../config/auth';

// 初始化 User Pool
const userPool = new CognitoUserPool({
  UserPoolId: AUTH_CONFIG.userPoolId,
  ClientId: AUTH_CONFIG.userPoolWebClientId,
});

export interface AuthUser {
  username: string;
  email: string;
  name?: string;
}

export interface SignUpParams {
  username: string;
  email: string;
  password: string;
  name?: string;
}

export interface SignInParams {
  username: string;
  password: string;
}

// 注册
export function signUp(params: SignUpParams): Promise<void> {
  return new Promise((resolve, reject) => {
    const attributeList = [
      new CognitoUserAttribute({ Name: 'email', Value: params.email }),
    ];
    
    if (params.name) {
      attributeList.push(
        new CognitoUserAttribute({ Name: 'name', Value: params.name })
      );
    }

    userPool.signUp(
      params.username,
      params.password,
      attributeList,
      [],
      (err, _result) => {
        if (err) {
          reject(err);
        } else {
          resolve();
        }
      }
    );
  });
}

// 确认注册（验证码）
export function confirmSignUp(username: string, code: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const cognitoUser = new CognitoUser({
      Username: username,
      Pool: userPool,
    });

    cognitoUser.confirmRegistration(code, true, (err, _result) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

// 登录
export function signIn(params: SignInParams): Promise<CognitoUserSession> {
  return new Promise((resolve, reject) => {
    const cognitoUser = new CognitoUser({
      Username: params.username,
      Pool: userPool,
    });

    const authDetails = new AuthenticationDetails({
      Username: params.username,
      Password: params.password,
    });

    // 使用 USER_PASSWORD_AUTH 而不是 SRP
    cognitoUser.authenticateUser(authDetails, {
      onSuccess: (session) => {
        console.log('[Auth] authenticateUser success');
        resolve(session);
      },
      onFailure: (err) => {
        console.log('[Auth] authenticateUser failed:', err);
        reject(err);
      },
      newPasswordRequired: (_userAttributes) => {
        // 首次登录需要修改密码的情况
        console.log('[Auth] newPasswordRequired');
        reject(new Error('NEW_PASSWORD_REQUIRED'));
      },
    });
  });
}

// 登出
export function signOut(): void {
  const cognitoUser = userPool.getCurrentUser();
  if (cognitoUser) {
    cognitoUser.signOut();
  }
}

// 获取当前用户
export function getCurrentUser(): Promise<AuthUser | null> {
  return new Promise((resolve, reject) => {
    const cognitoUser = userPool.getCurrentUser();
    
    if (!cognitoUser) {
      resolve(null);
      return;
    }

    cognitoUser.getSession((err: Error | null, session: CognitoUserSession | null) => {
      if (err || !session?.isValid()) {
        resolve(null);
        return;
      }

      cognitoUser.getUserAttributes((err, attributes) => {
        if (err) {
          reject(err);
          return;
        }

        const user: AuthUser = {
          username: cognitoUser.getUsername(),
          email: '',
        };

        attributes?.forEach((attr) => {
          if (attr.getName() === 'email') {
            user.email = attr.getValue();
          }
          if (attr.getName() === 'name') {
            user.name = attr.getValue();
          }
        });

        resolve(user);
      });
    });
  });
}

// 获取当前 session
export function getSession(): Promise<CognitoUserSession | null> {
  return new Promise((resolve, reject) => {
    const cognitoUser = userPool.getCurrentUser();
    
    if (!cognitoUser) {
      resolve(null);
      return;
    }

    cognitoUser.getSession((err: Error | null, session: CognitoUserSession | null) => {
      if (err) {
        reject(err);
      } else {
        resolve(session);
      }
    });
  });
}

// 获取 ID Token（用于 API 调用）
export async function getIdToken(): Promise<string | null> {
  const session = await getSession();
  return session?.getIdToken().getJwtToken() || null;
}

// 获取 Access Token
export async function getAccessToken(): Promise<string | null> {
  const session = await getSession();
  return session?.getAccessToken().getJwtToken() || null;
}

// 重新发送验证码
export function resendConfirmationCode(username: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const cognitoUser = new CognitoUser({
      Username: username,
      Pool: userPool,
    });

    cognitoUser.resendConfirmationCode((err, _result) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

// 忘记密码
export function forgotPassword(username: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const cognitoUser = new CognitoUser({
      Username: username,
      Pool: userPool,
    });

    cognitoUser.forgotPassword({
      onSuccess: () => resolve(),
      onFailure: (err) => reject(err),
    });
  });
}

// 确认新密码
export function confirmPassword(
  username: string,
  code: string,
  newPassword: string
): Promise<void> {
  return new Promise((resolve, reject) => {
    const cognitoUser = new CognitoUser({
      Username: username,
      Pool: userPool,
    });

    cognitoUser.confirmPassword(code, newPassword, {
      onSuccess: () => resolve(),
      onFailure: (err) => reject(err),
    });
  });
}
