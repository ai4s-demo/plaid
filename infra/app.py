#!/usr/bin/env python3
"""CDK app for Smart Campaign Designer infrastructure."""
import os
import aws_cdk as cdk
from stacks.cognito_stack import CognitoStack
from stacks.app_stack import AppStack

app = cdk.App()

# 从环境变量或 context 获取配置
env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1")
)

# Cognito Stack
cognito_stack = CognitoStack(
    app, 
    "SmartCampaignDesignerAuth",
    env=env,
    description="Cognito authentication for Smart Campaign Designer"
)

# Application Stack (Frontend + Backend)
app_stack = AppStack(
    app,
    "SmartCampaignDesignerApp",
    env=env,
    cognito_user_pool_id=cognito_stack.user_pool.user_pool_id,
    cognito_app_client_id=cognito_stack.app_client.user_pool_client_id,
    description="Smart Campaign Designer Application"
)
app_stack.add_dependency(cognito_stack)

app.synth()
