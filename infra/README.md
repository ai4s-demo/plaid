# Smart Campaign Designer - Infrastructure

AWS CDK 项目，用于部署 Cognito 认证资源。

## 前置条件

1. 安装 AWS CDK CLI:
```bash
npm install -g aws-cdk
```

2. 配置 AWS 凭证:
```bash
aws configure
```

## 部署步骤

1. 创建虚拟环境并安装依赖:
```bash
cd infra
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Bootstrap CDK (首次使用):
```bash
cdk bootstrap
```

3. 部署 Cognito 资源:
```bash
cdk deploy
```

4. 部署完成后，记录输出的值:
- `UserPoolId`: Cognito User Pool ID
- `AppClientId`: App Client ID
- `Region`: AWS Region

5. 将这些值配置到前端和后端。

## 清理资源

```bash
cdk destroy
```

## 资源说明

- **User Pool**: 用户池，支持邮箱注册和登录
- **App Client**: Web 应用客户端，用于前端认证
- **Cognito Domain**: 托管 UI 域名（可选使用）
