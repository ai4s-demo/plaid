#!/bin/bash
# Smart Campaign Designer - 一键清理脚本
# 用法: ./destroy.sh

set -e

echo "🗑️  Smart Campaign Designer 清理脚本"
echo "===================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 确认
echo -e "${RED}⚠️  警告: 此操作将删除所有已部署的 AWS 资源！${NC}"
echo ""
read -p "确定要继续吗? (y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

echo -e "\n${YELLOW}正在删除 AWS 资源...${NC}"

cd infra

# 激活虚拟环境
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo -e "${RED}❌ CDK 虚拟环境不存在，请先运行 deploy.sh${NC}"
    exit 1
fi

# 静默 Node.js 版本警告
export JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=1

# 删除所有栈
cdk destroy --all --force

deactivate
cd ..

# 清理输出文件
rm -f cdk-outputs.json

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ 清理完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "所有 AWS 资源已删除 (CDKToolkit 栈保留)"
echo "如需完全清理，请手动删除 CDKToolkit 栈:"
echo "  aws cloudformation delete-stack --stack-name CDKToolkit"
