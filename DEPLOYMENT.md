# Smart Campaign Designer - 部署指南

## 快速开始

### 一键部署

```bash
./deploy.sh
```

### 一键清理

```bash
./destroy.sh
```

---

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

| 工具 | 版本要求 | 安装链接 |
|------|----------|----------|
| AWS CLI | v2+ | [安装指南](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) |
| Node.js | 18+ | [下载](https://nodejs.org/) |
| Python | 3.11+ | [下载](https://www.python.org/) |
| Docker | 最新版 | [下载](https://www.docker.com/) |
| AWS CDK | 2.x | 自动安装 |

## 手动部署步骤

### 1. 安装依赖

```bash
# 前端依赖
cd frontend && npm install && cd ..

# CDK 依赖
cd infra
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..
```

### 2. Bootstrap CDK (首次部署)

```bash
cd infra
source .venv/bin/activate
cdk bootstrap aws://YOUR_ACCOUNT_ID/us-east-1
```

### 3. 构建前端

```bash
cd frontend && npm run build && cd ..
```

### 4. 部署

```bash
cd infra
source .venv/bin/activate
cdk deploy --all --require-approval never
```

### 5. 创建测试用户

```bash
USER_POOL_ID=<从输出获取>

aws cognito-idp admin-create-user \
  --user-pool-id $USER_POOL_ID \
  --username demouser \
  --user-attributes Name=email,Value=demo@example.com Name=email_verified,Value=true \
  --temporary-password "Demo@123" \
  --message-action SUPPRESS

aws cognito-idp admin-set-user-password \
  --user-pool-id $USER_POOL_ID \
  --username demouser \
  --password "Demo@123" \
  --permanent
```

## 更新部署

### 更新前端

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://YOUR_BUCKET_NAME/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### 更新后端

```bash
cd infra
source .venv/bin/activate
cdk deploy SmartCampaignDesignerApp --require-approval never
```

## 本地开发

### 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

## 费用估算 (月)

| 服务 | 估算费用 |
|------|----------|
| App Runner (1 vCPU, 2GB) | ~$25-50 |
| CloudFront | ~$1-5 |
| S3 | < $1 |
| Cognito (< 50k MAU) | 免费 |
| Bedrock (按使用量) | 按需 |

**总计**: ~$30-60/月 (不含 Bedrock 使用费)

## 故障排除

### Docker 构建失败

如果遇到网络超时，Dockerfile 已配置使用 AWS ECR Public Gallery 镜像：
```dockerfile
FROM public.ecr.aws/docker/library/python:3.11-slim
```

### CDK 命令找不到

```bash
npm install -g aws-cdk
```

### Python 模块找不到

```bash
cd infra
source .venv/bin/activate
pip install -r requirements.txt
```
