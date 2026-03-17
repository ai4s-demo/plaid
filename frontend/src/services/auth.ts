import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
  CognitoUserAttribute,
  CognitoUserSession,
} from 'amazon-cognito-identity-js';
import { AUTH_CONFIG } from '../config/auth';

// Initialize User Pool
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

// Sign up
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

// Confirm sign up (verification code)
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

// Sign in
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

    // Use USER_PASSWORD_AUTH instead of SRP
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
        // First login requires password change
        console.log('[Auth] newPasswordRequired');
        reject(new Error('NEW_PASSWORD_REQUIRED'));
      },
    });
  });
}

// Sign out
export function signOut(): void {
  const cognitoUser = userPool.getCurrentUser();
  if (cognitoUser) {
    cognitoUser.signOut();
  }
}

// Get current user
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

// Get current session
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

// Get ID Token (for API calls)
export async function getIdToken(): Promise<string | null> {
  const session = await getSession();
  return session?.getIdToken().getJwtToken() || null;
}

// Get Access Token
export async function getAccessToken(): Promise<string | null> {
  const session = await getSession();
  return session?.getAccessToken().getJwtToken() || null;
}

// Resend confirmation code
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

// Forgot password
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

// Confirm new password
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
