#!/bin/bash
# Smart Campaign Designer - One-Click Deploy Script
# Usage:
#   ./deploy.sh                    Deploy everything
#   ./deploy.sh --destroy          Tear down all stacks
#   ./deploy.sh --diff             Preview CDK diff (no deploy)
#   ./deploy.sh --skip-frontend    Backend-only deploy (skip frontend build/upload)
#   INSTANCE_TYPE=c5.2xlarge ./deploy.sh   Custom instance type

set -euo pipefail

# ======================== Configuration ========================

INSTANCE_TYPE=${INSTANCE_TYPE:-c7i.xlarge}
REGION=${AWS_REGION:-us-east-1}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CDK_OUTPUTS_FILE="$SCRIPT_DIR/cdk-outputs.json"
INFRA_DIR="$SCRIPT_DIR/infra"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Flags (parsed from arguments)
FLAG_DESTROY=false
FLAG_DIFF=false
FLAG_SKIP_FRONTEND=false

# Track which step we are on for error reporting
CURRENT_STEP=""
DEPLOY_START_TIME=""

# ======================== Colors ========================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ======================== Error Handling ========================

cleanup_on_error() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo ""
        echo -e "${RED}============================================${NC}"
        echo -e "${RED} DEPLOY FAILED${NC}"
        echo -e "${RED}============================================${NC}"
        if [ -n "$CURRENT_STEP" ]; then
            echo -e "${RED} Failed during: ${BOLD}${CURRENT_STEP}${NC}"
        fi
        echo -e "${RED} Exit code: $exit_code${NC}"
        echo -e "${RED} Check the output above for details.${NC}"
        echo -e "${RED}============================================${NC}"
    fi
}

trap cleanup_on_error EXIT

# ======================== Argument Parsing ========================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --destroy)
                FLAG_DESTROY=true
                shift
                ;;
            --diff)
                FLAG_DIFF=true
                shift
                ;;
            --skip-frontend)
                FLAG_SKIP_FRONTEND=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    echo "Smart Campaign Designer - Deploy Script"
    echo ""
    echo "Usage: ./deploy.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --destroy          Tear down all AWS stacks"
    echo "  --diff             Show CDK diff without deploying"
    echo "  --skip-frontend    Skip frontend build and upload (backend only)"
    echo "  -h, --help         Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  INSTANCE_TYPE      EC2 instance type (default: c7i.xlarge)"
    echo "  AWS_REGION         AWS region (default: us-east-1)"
}

# ======================== Utility Functions ========================

# Activate the infra Python virtualenv
activate_venv() {
    source "$INFRA_DIR/.venv/bin/activate"
    export JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=1
}

# Read a value from cdk-outputs.json using python3
read_cdk_output() {
    local stack_name="$1"
    local key="$2"
    python3 -c "import sys, json; print(json.load(open('$CDK_OUTPUTS_FILE'))['$stack_name']['$key'])" 2>/dev/null || echo ""
}

# ======================== Step Functions ========================

check_dependencies() {
    CURRENT_STEP="Checking dependencies"
    echo -e "\n${YELLOW}[Step 1] Checking dependencies...${NC}"

    local missing=0

    if ! command -v aws &> /dev/null; then
        echo -e "${RED}  AWS CLI not installed${NC}"
        echo "  Install: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        missing=1
    fi

    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}  AWS credentials not configured${NC}"
        echo "  Run: aws configure"
        missing=1
    fi

    if ! command -v node &> /dev/null; then
        echo -e "${RED}  Node.js not installed${NC}"
        missing=1
    fi

    if ! command -v npm &> /dev/null; then
        echo -e "${RED}  npm not installed${NC}"
        missing=1
    fi

    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}  Python3 not installed${NC}"
        missing=1
    fi

    if ! command -v docker &> /dev/null; then
        echo -e "${RED}  Docker not installed${NC}"
        missing=1
    elif ! docker info &> /dev/null; then
        echo -e "${RED}  Docker is not running. Please start Docker.${NC}"
        missing=1
    fi

    if [ $missing -ne 0 ]; then
        echo -e "${RED}  Missing dependencies. Aborting.${NC}"
        exit 1
    fi

    # Install CDK CLI if missing
    if ! command -v cdk &> /dev/null; then
        echo -e "${YELLOW}  CDK CLI not found, installing...${NC}"
        npm install -g aws-cdk
    fi

    echo -e "${GREEN}  All dependencies OK${NC}"
}

install_dependencies() {
    CURRENT_STEP="Installing project dependencies"
    echo -e "\n${YELLOW}[Step 2] Installing project dependencies...${NC}"

    # Frontend dependencies (skip if --skip-frontend on a non-first deploy)
    if [ "$FLAG_SKIP_FRONTEND" = false ]; then
        echo "  Installing frontend dependencies..."
        (cd "$FRONTEND_DIR" && npm install)
    fi

    # CDK / infra dependencies
    echo "  Installing CDK dependencies..."
    if [ ! -d "$INFRA_DIR/.venv" ]; then
        python3 -m venv "$INFRA_DIR/.venv"
    fi
    (
        activate_venv
        pip install -q -r "$INFRA_DIR/requirements.txt"
    )

    echo -e "${GREEN}  Dependencies installed${NC}"
}

build_frontend() {
    if [ "$FLAG_SKIP_FRONTEND" = true ]; then
        echo -e "\n${YELLOW}[Step 3] Skipping frontend build (--skip-frontend)${NC}"
        return
    fi

    CURRENT_STEP="Building frontend"
    echo -e "\n${YELLOW}[Step 3] Building frontend...${NC}"
    (cd "$FRONTEND_DIR" && npm run build)
    echo -e "${GREEN}  Frontend build complete${NC}"
}

cdk_bootstrap() {
    CURRENT_STEP="CDK Bootstrap"
    echo -e "\n${YELLOW}[Step 4] Checking CDK Bootstrap...${NC}"

    local account_id
    account_id=$(aws sts get-caller-identity --query Account --output text)

    if ! aws cloudformation describe-stacks --stack-name CDKToolkit --region "$REGION" &> /dev/null; then
        echo "  Running CDK bootstrap..."
        (
            activate_venv
            cd "$INFRA_DIR"
            cdk bootstrap "aws://$account_id/$REGION"
        )
    else
        echo "  CDK already bootstrapped"
    fi

    echo -e "${GREEN}  CDK Bootstrap OK${NC}"
}

do_deploy() {
    CURRENT_STEP="CDK Deploy"
    echo -e "\n${YELLOW}[Step 5] Deploying to AWS...${NC}"
    echo -e "  Instance type: ${CYAN}${INSTANCE_TYPE}${NC}"
    echo -e "  Region:        ${CYAN}${REGION}${NC}"

    (
        activate_venv
        cd "$INFRA_DIR"
        cdk deploy --all --require-approval never \
            -c instance_type="$INSTANCE_TYPE" \
            --outputs-file "$CDK_OUTPUTS_FILE"
    )

    echo -e "${GREEN}  CDK deploy complete${NC}"
}

post_deploy() {
    CURRENT_STEP="Post-deploy configuration"
    echo -e "\n${YELLOW}[Step 6] Post-deploy configuration...${NC}"

    if [ ! -f "$CDK_OUTPUTS_FILE" ]; then
        echo -e "${RED}  cdk-outputs.json not found. Cannot run post-deploy.${NC}"
        return 1
    fi

    local user_pool_id app_client_id cloudfront_url backend_url s3_bucket backend_ip instance_id
    user_pool_id=$(read_cdk_output "SmartCampaignDesignerAuth" "UserPoolId")
    app_client_id=$(read_cdk_output "SmartCampaignDesignerAuth" "AppClientId")
    cloudfront_url=$(read_cdk_output "SmartCampaignDesignerApp" "CloudFrontURL")
    backend_url=$(read_cdk_output "SmartCampaignDesignerApp" "BackendURL")
    backend_ip=$(read_cdk_output "SmartCampaignDesignerApp" "BackendPublicIP")
    s3_bucket=$(read_cdk_output "SmartCampaignDesignerApp" "S3BucketName")
    instance_id=$(read_cdk_output "SmartCampaignDesignerApp" "InstanceId")

    # Update frontend .env with Cognito config and rebuild/upload
    if [ "$FLAG_SKIP_FRONTEND" = false ]; then
        echo "  Updating frontend configuration..."
        cat > "$FRONTEND_DIR/.env" << EOF
# Cognito configuration (auto-generated by deploy.sh)
VITE_AWS_REGION=$REGION
VITE_COGNITO_USER_POOL_ID=$user_pool_id
VITE_COGNITO_APP_CLIENT_ID=$app_client_id

# API configuration (production uses CloudFront proxy)
VITE_API_URL=
EOF

        echo "  Rebuilding frontend with updated config..."
        (cd "$FRONTEND_DIR" && npm run build)

        echo "  Uploading frontend to S3..."
        aws s3 sync "$FRONTEND_DIR/dist/" "s3://$s3_bucket/" --delete

        # Invalidate CloudFront cache
        local dist_domain dist_id
        dist_domain=$(echo "$cloudfront_url" | sed 's|https://||')
        dist_id=$(aws cloudfront list-distributions \
            --query "DistributionList.Items[?DomainName=='$dist_domain'].Id" \
            --output text)
        if [ -n "$dist_id" ] && [ "$dist_id" != "None" ]; then
            echo "  Invalidating CloudFront cache..."
            aws cloudfront create-invalidation --distribution-id "$dist_id" --paths "/*" > /dev/null
        fi
    fi

    # Create demo user
    echo "  Creating demo user..."
    aws cognito-idp admin-create-user \
        --user-pool-id "$user_pool_id" \
        --username demouser \
        --user-attributes Name=email,Value=demo@example.com Name=email_verified,Value=true \
        --temporary-password "Demo@123" \
        --message-action SUPPRESS 2>/dev/null || true

    aws cognito-idp admin-set-user-password \
        --user-pool-id "$user_pool_id" \
        --username demouser \
        --password "Demo@123" \
        --permanent 2>/dev/null || true

    # Run health check via CloudFront (direct IP is blocked by SG)
    health_check "$cloudfront_url"

    # Print summary
    print_summary "$cloudfront_url" "$backend_url" "$backend_ip" "$s3_bucket" "$instance_id" "$user_pool_id" "$app_client_id"
}

# ======================== Health Check ========================

health_check() {
    local base_url="$1"
    local health_endpoint="${base_url}/api/health"
    local max_attempts=20
    local wait_seconds=15

    CURRENT_STEP="Backend health check"
    echo -e "\n${YELLOW}[Step 7] Running backend health check...${NC}"
    echo "  Endpoint: $health_endpoint"
    echo "  Waiting for EC2 instance to boot and start Docker container..."

    for attempt in $(seq 1 $max_attempts); do
        local http_code
        http_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "$health_endpoint" 2>/dev/null || echo "000")

        if [ "$http_code" = "200" ]; then
            echo -e "${GREEN}  Backend is healthy (HTTP 200) after attempt $attempt${NC}"
            return 0
        fi

        echo "  Attempt $attempt/$max_attempts - HTTP $http_code, retrying in ${wait_seconds}s..."
        sleep "$wait_seconds"
    done

    echo -e "${YELLOW}  WARNING: Backend did not respond with HTTP 200 after $max_attempts attempts.${NC}"
    echo -e "${YELLOW}  The EC2 instance may still be starting. Check manually:${NC}"
    echo -e "${YELLOW}    curl $health_endpoint${NC}"
    # Don't fail the deploy for a health check timeout
    return 0
}

# ======================== Summary ========================

print_summary() {
    local cloudfront_url="$1"
    local backend_url="$2"
    local backend_ip="$3"
    local s3_bucket="$4"
    local instance_id="$5"
    local user_pool_id="$6"
    local app_client_id="$7"

    local elapsed=""
    if [ -n "$DEPLOY_START_TIME" ]; then
        local end_time
        end_time=$(date +%s)
        local duration=$(( end_time - DEPLOY_START_TIME ))
        local mins=$(( duration / 60 ))
        local secs=$(( duration % 60 ))
        elapsed="${mins}m ${secs}s"
    fi

    echo ""
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${GREEN}                    DEPLOYMENT SUCCESSFUL                       ${NC}"
    echo -e "${GREEN}================================================================${NC}"
    echo ""
    echo -e "${BOLD}  Application${NC}"
    echo -e "  -----------------------------------------------"
    echo -e "  CloudFront URL :  ${CYAN}${cloudfront_url}${NC}"
    echo -e "  Backend API    :  ${CYAN}${backend_url}${NC}"
    echo -e "  Backend IP     :  ${CYAN}${backend_ip}${NC}"
    echo ""
    echo -e "${BOLD}  Infrastructure${NC}"
    echo -e "  -----------------------------------------------"
    echo -e "  Region         :  ${CYAN}${REGION}${NC}"
    echo -e "  Instance Type  :  ${CYAN}${INSTANCE_TYPE}${NC}"
    echo -e "  Instance ID    :  ${CYAN}${instance_id}${NC}"
    echo -e "  S3 Bucket      :  ${CYAN}${s3_bucket}${NC}"
    echo ""
    echo -e "${BOLD}  Authentication${NC}"
    echo -e "  -----------------------------------------------"
    echo -e "  User Pool ID   :  ${CYAN}${user_pool_id}${NC}"
    echo -e "  App Client ID  :  ${CYAN}${app_client_id}${NC}"
    echo ""
    echo -e "${BOLD}  Demo Account${NC}"
    echo -e "  -----------------------------------------------"
    echo -e "  Username       :  ${CYAN}demouser${NC}"
    echo -e "  Password       :  ${CYAN}Demo@123${NC}"
    if [ -n "$elapsed" ]; then
        echo ""
        echo -e "  Total time     :  ${CYAN}${elapsed}${NC}"
    fi
    echo ""
    echo -e "${GREEN}================================================================${NC}"
}

# ======================== Destroy ========================

do_destroy() {
    CURRENT_STEP="CDK Destroy"
    echo -e "\n${YELLOW}Destroying all stacks...${NC}"
    echo -e "${RED}This will delete ALL deployed resources.${NC}"

    (
        activate_venv
        cd "$INFRA_DIR"
        cdk destroy --all --force
    )

    echo -e "${GREEN}All stacks destroyed.${NC}"
}

# ======================== Diff ========================

do_diff() {
    CURRENT_STEP="CDK Diff"
    echo -e "\n${YELLOW}Running CDK diff...${NC}"

    (
        activate_venv
        cd "$INFRA_DIR"
        cdk diff --all -c instance_type="$INSTANCE_TYPE"
    )
}

# ======================== Main ========================

main() {
    parse_args "$@"

    echo "Smart Campaign Designer - Deploy Script"
    echo "========================================"
    echo -e "  Instance type : ${CYAN}${INSTANCE_TYPE}${NC}"
    echo -e "  Region        : ${CYAN}${REGION}${NC}"

    # --destroy mode
    if [ "$FLAG_DESTROY" = true ]; then
        check_dependencies
        install_dependencies
        do_destroy
        exit 0
    fi

    # --diff mode
    if [ "$FLAG_DIFF" = true ]; then
        check_dependencies
        install_dependencies
        do_diff
        exit 0
    fi

    # Full deploy
    DEPLOY_START_TIME=$(date +%s)
    check_dependencies
    install_dependencies
    build_frontend
    cdk_bootstrap
    do_deploy
    post_deploy
}

main "$@"
