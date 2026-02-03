# Smart Campaign Designer - 部署指南

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        CloudFront                                │
│                    (HTTPS + CDN 加速)                            │
├─────────────────────────────────────────────────────────────────┤
│         /                          │         /api/*              │
│         ↓                          │         ↓                   │
│    ┌─────────┐                     │    ┌──────────────┐        │
│    │   S3    │                     │    │  App Runner  │        │
│    │ (前端)  │                     │    │   (后端)     │        │
│    └─────────┘                     │    └──────────────┘        │
│                                    │         ↓                   │
│                                    │    ┌──────────────┐        │
│                                    │    │   Bedrock    │        │
│                                    │    │  (Claude 3)  │        │
│                                    │    └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                     │
                              ┌──────────────┐
                              │   Cognito    │
                              │   (认证)     │
                              └──────────────┘
```

## 前置条件

1. AWS CLI 已配置
2. Node.js 18+ 和 npm
3. Python 3.11+ 和 pip
4. Docker (用于构建后端镜像)
5. AWS CDK CLI (`npm install -g aws-cdk`)

## 部署步骤

### 1. 克隆项目并安装依赖

```bash
# 前端依赖
cd frontend
npm install

# 后端依赖
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# CDK 依赖
cd ../infra
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Bootstrap CDK (首次部署)

```bash
cd infra
cdk bootstrap aws://YOUR_ACCOUNT_ID/us-east-1
```

### 3. 构建前端

```bash
cd frontend
npm run build
```

### 4. 部署

```bash
cd infra
source .venv/bin/activate
cdk deploy --all --require-approval never
```

### 5. 创建测试用户

```bash
# 获取 User Pool ID (从 CDK 输出)
USER_POOL_ID=<从输出获取>

# 创建用户
aws cognito-idp admin-create-user \
  --user-pool-id $USER_POOL_ID \
  --username demouser \
  --user-attributes Name=email,Value=demo@example.com Name=email_verified,Value=true \
  --temporary-password "Demo@123" \
  --message-action SUPPRESS

# 设置永久密码
aws cognito-idp admin-set-user-password \
  --user-pool-id $USER_POOL_ID \
  --username demouser \
  --password "Demo@123" \
  --permanent
```

## 部署输出

部署完成后会输出：
- `CloudFrontURL`: 应用访问地址
- `BackendURL`: 后端 API 地址
- `UserPoolId`: Cognito User Pool ID
- `AppClientId`: Cognito App Client ID

## 更新前端

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://YOUR_BUCKET_NAME/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

## 清理资源

```bash
cd infra
cdk destroy --all
```

---

## CloudFormation 模板

以下是两个独立的 CloudFormation 模板，可以直接在 AWS Console 中部署。

### 注意事项

1. 需要先部署 Auth 栈，再部署 App 栈
2. App 栈需要预先构建 Docker 镜像并推送到 ECR
3. 前端代码需要手动上传到 S3

---

## 费用估算 (月)

| 服务 | 估算费用 |
|------|----------|
| App Runner (1 vCPU, 2GB) | ~$25-50 |
| CloudFront | ~$1-5 |
| S3 | < $1 |
| Cognito (< 50k MAU) | 免费 |
| Bedrock (按使用量) | 按需 |

**总计**: ~$30-60/月 (不含 Bedrock 使用费)
