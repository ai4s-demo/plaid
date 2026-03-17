// Cognito config - update these values after CDK deployment
export const AUTH_CONFIG = {
  region: import.meta.env.VITE_AWS_REGION || 'us-east-1',
  userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || '',
  userPoolWebClientId: import.meta.env.VITE_COGNITO_APP_CLIENT_ID || '',
};

// Check if auth is configured
export const isAuthConfigured = () => {
  return AUTH_CONFIG.userPoolId && AUTH_CONFIG.userPoolWebClientId;
};
