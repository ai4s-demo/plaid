"""Cognito User Pool stack for Smart Campaign Designer."""
from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    Duration,
    aws_cognito as cognito,
)
from constructs import Construct


class CognitoStack(Stack):
    """Cognito authentication stack."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # User Pool
        self.user_pool = cognito.UserPool(
            self,
            "UserPool",
            user_pool_name="smart-campaign-designer-users",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                email=True,
                username=True,
            ),
            auto_verify=cognito.AutoVerifiedAttrs(
                email=True,
            ),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=True,
                ),
                fullname=cognito.StandardAttribute(
                    required=False,
                    mutable=True,
                ),
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False,
                temp_password_validity=Duration.days(7),
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=RemovalPolicy.DESTROY,  # 开发环境用 DESTROY，生产环境改为 RETAIN
        )

        # App Client (for frontend)
        self.app_client = self.user_pool.add_client(
            "WebAppClient",
            user_pool_client_name="smart-campaign-designer-web",
            generate_secret=False,  # SPA 不需要 client secret
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=True,
                ),
                scopes=[
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.PROFILE,
                ],
                callback_urls=[
                    "http://localhost:5173/callback",
                    "http://localhost:5173/",
                    "https://*.cloudfront.net/callback",
                    "https://*.cloudfront.net/",
                ],
                logout_urls=[
                    "http://localhost:5173/",
                    "https://*.cloudfront.net/",
                ],
            ),
            access_token_validity=Duration.hours(1),
            id_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(30),
            prevent_user_existence_errors=True,
        )

        # Cognito Domain (for hosted UI)
        # 使用账号后8位生成唯一域名前缀（只允许小写字母、数字和连字符）
        domain_prefix = f"scd-{self.account[-8:].lower()}"
        self.user_pool_domain = self.user_pool.add_domain(
            "CognitoDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=domain_prefix,
            ),
        )

        # Outputs
        CfnOutput(
            self,
            "UserPoolId",
            value=self.user_pool.user_pool_id,
            description="Cognito User Pool ID",
            export_name="SmartCampaignUserPoolId",
        )

        CfnOutput(
            self,
            "UserPoolArn",
            value=self.user_pool.user_pool_arn,
            description="Cognito User Pool ARN",
            export_name="SmartCampaignUserPoolArn",
        )

        CfnOutput(
            self,
            "AppClientId",
            value=self.app_client.user_pool_client_id,
            description="Cognito App Client ID",
            export_name="SmartCampaignAppClientId",
        )

        CfnOutput(
            self,
            "CognitoDomain",
            value=self.user_pool_domain.domain_name,
            description="Cognito Domain",
            export_name="SmartCampaignCognitoDomain",
        )

        CfnOutput(
            self,
            "Region",
            value=self.region,
            description="AWS Region",
        )
