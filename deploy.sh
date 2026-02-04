#!/bin/bash
# Smart Campaign Designer - 一键部署脚本
# 用法: ./deploy.sh

set -e

echo "🚀 Smart Campaign Designer 部署脚本"
echo "=================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查依赖
check_dependencies() {
    echo -e "\n${YELLOW}[1/6] 检查依赖...${NC}"
    
    # 检查 AWS CLI
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI 未安装${NC}"
        echo "请安装: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        exit 1
    fi
    
    # 检查 AWS 凭证
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}❌ AWS 凭证未配置${NC}"
        echo "请运行: aws configure"
        exit 1
    fi
    
    # 检查 Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js 未安装${NC}"
        exit 1
    fi
    
    # 检查 npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm 未安装${NC}"
        exit 1
    fi
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 未安装${NC}"
        exit 1
    fi
    
    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker 未安装${NC}"
        exit 1
    fi
    
    # 检查 Docker 是否运行
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker 未运行，请启动 Docker${NC}"
        exit 1
    fi
    
    # 检查 CDK
    if ! command -v cdk &> /dev/null; then
        echo -e "${YELLOW}⚠️  CDK CLI 未安装，正在安装...${NC}"
        npm install -g aws-cdk
    fi
    
    echo -e "${GREEN}✅ 所有依赖检查通过${NC}"
}

# 安装项目依赖
install_dependencies() {
    echo -e "\n${YELLOW}[2/6] 安装项目依赖...${NC}"
    
    # 前端依赖
    echo "安装前端依赖..."
    cd frontend
    npm install
    cd ..
    
    # CDK 依赖
    echo "安装 CDK 依赖..."
    cd infra
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -q -r requirements.txt
    deactivate
    cd ..
    
    echo -e "${GREEN}✅ 依赖安装完成${NC}"
}

# 构建前端
build_frontend() {
    echo -e "\n${YELLOW}[3/6] 构建前端...${NC}"
    cd frontend
    npm run build
    cd ..
    echo -e "${GREEN}✅ 前端构建完成${NC}"
}

# CDK Bootstrap (如果需要)
cdk_bootstrap() {
    echo -e "\n${YELLOW}[4/6] 检查 CDK Bootstrap...${NC}"
    
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    REGION=${AWS_REGION:-us-east-1}
    
    # 检查是否已经 bootstrap
    if ! aws cloudformation describe-stacks --stack-name CDKToolkit --region $REGION &> /dev/null; then
        echo "执行 CDK Bootstrap..."
        cd infra
        source .venv/bin/activate
        cdk bootstrap aws://$ACCOUNT_ID/$REGION
        deactivate
        cd ..
    else
        echo "CDK 已经 Bootstrap"
    fi
    
    echo -e "${GREEN}✅ CDK Bootstrap 完成${NC}"
}

# 部署
deploy() {
    echo -e "\n${YELLOW}[5/6] 部署到 AWS...${NC}"
    
    cd infra
    source .venv/bin/activate
    
    # 静默 Node.js 版本警告
    export JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=1
    
    # 部署所有栈
    cdk deploy --all --require-approval never --outputs-file ../cdk-outputs.json
    
    deactivate
    cd ..
    
    echo -e "${GREEN}✅ 部署完成${NC}"
}

# 创建测试用户并显示信息
post_deploy() {
    echo -e "\n${YELLOW}[6/6] 配置完成...${NC}"
    
    # 读取输出
    if [ -f "cdk-outputs.json" ]; then
        USER_POOL_ID=$(cat cdk-outputs.json | python3 -c "import sys, json; print(json.load(sys.stdin)['SmartCampaignDesignerAuth']['UserPoolId'])")
        APP_CLIENT_ID=$(cat cdk-outputs.json | python3 -c "import sys, json; print(json.load(sys.stdin)['SmartCampaignDesignerAuth']['AppClientId'])")
        CLOUDFRONT_URL=$(cat cdk-outputs.json | python3 -c "import sys, json; print(json.load(sys.stdin)['SmartCampaignDesignerApp']['CloudFrontURL'])")
        BACKEND_URL=$(cat cdk-outputs.json | python3 -c "import sys, json; print(json.load(sys.stdin)['SmartCampaignDesignerApp']['BackendURL'])")
        
        # 更新前端配置
        cat > frontend/.env << EOF
# Cognito 配置
VITE_AWS_REGION=us-east-1
VITE_COGNITO_USER_POOL_ID=$USER_POOL_ID
VITE_COGNITO_APP_CLIENT_ID=$APP_CLIENT_ID

# API 配置 (生产环境通过 CloudFront 代理)
VITE_API_URL=
EOF
        
        # 重新构建并上传前端
        echo "更新前端配置..."
        cd frontend
        npm run build
        
        S3_BUCKET=$(cat ../cdk-outputs.json | python3 -c "import sys, json; print(json.load(sys.stdin)['SmartCampaignDesignerApp']['S3BucketName'])")
        aws s3 sync dist/ s3://$S3_BUCKET/ --delete
        
        # 获取 CloudFront Distribution ID 并刷新缓存
        DIST_DOMAIN=$(echo $CLOUDFRONT_URL | sed 's|https://||')
        DIST_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?DomainName=='$DIST_DOMAIN'].Id" --output text)
        if [ -n "$DIST_ID" ]; then
            aws cloudfront create-invalidation --distribution-id $DIST_ID --paths "/*" > /dev/null
        fi
        cd ..
        
        # 创建测试用户
        echo "创建测试用户..."
        aws cognito-idp admin-create-user \
            --user-pool-id $USER_POOL_ID \
            --username demouser \
            --user-attributes Name=email,Value=demo@example.com Name=email_verified,Value=true \
            --temporary-password "Demo@123" \
            --message-action SUPPRESS 2>/dev/null || true
        
        aws cognito-idp admin-set-user-password \
            --user-pool-id $USER_POOL_ID \
            --username demouser \
            --password "Demo@123" \
            --permanent 2>/dev/null || true
        
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}🎉 部署成功！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "📱 应用地址: ${YELLOW}$CLOUDFRONT_URL${NC}"
        echo -e "🔧 后端 API: ${YELLOW}https://$BACKEND_URL${NC}"
        echo ""
        echo -e "👤 测试账号:"
        echo -e "   用户名: ${YELLOW}demouser${NC}"
        echo -e "   密码:   ${YELLOW}Demo@123${NC}"
        echo ""
        echo -e "📝 Cognito 配置:"
        echo -e "   User Pool ID: $USER_POOL_ID"
        echo -e "   App Client ID: $APP_CLIENT_ID"
        echo ""
    fi
}

# 主流程
main() {
    check_dependencies
    install_dependencies
    build_frontend
    cdk_bootstrap
    deploy
    post_deploy
}

main
