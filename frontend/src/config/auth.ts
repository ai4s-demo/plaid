// Cognito 配置 - 部署 CDK 后更新这些值
export const AUTH_CONFIG = {
  region: import.meta.env.VITE_AWS_REGION || 'us-east-1',
  userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || '',
  userPoolWebClientId: import.meta.env.VITE_COGNITO_APP_CLIENT_ID || '',
};

// 检查是否已配置
export const isAuthConfigured = () => {
  return AUTH_CONFIG.userPoolId && AUTH_CONFIG.userPoolWebClientId;
};
