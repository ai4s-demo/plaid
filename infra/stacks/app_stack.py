"""Full application stack - Frontend (S3+CloudFront) + Backend (App Runner)."""
from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    Duration,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_ecr_assets as ecr_assets,
    aws_apprunner_alpha as apprunner,
    aws_iam as iam,
)
from constructs import Construct


class AppStack(Stack):
    """Full application deployment stack."""

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str,
        cognito_user_pool_id: str,
        cognito_app_client_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ==================== Backend (App Runner) ====================
        
        # Docker image from backend directory (force AMD64 for App Runner)
        backend_image = ecr_assets.DockerImageAsset(
            self,
            "BackendImage",
            directory="../backend",
            platform=ecr_assets.Platform.LINUX_AMD64,
        )

        # IAM role for App Runner
        instance_role = iam.Role(
            self,
            "AppRunnerInstanceRole",
            assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
        )
        
        # Grant Bedrock access
        instance_role.add_to_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
                resources=["*"],
            )
        )

        # App Runner service
        backend_service = apprunner.Service(
            self,
            "BackendService",
            source=apprunner.Source.from_asset(
                image_configuration=apprunner.ImageConfiguration(
                    port=8000,
                    environment_variables={
                        "COGNITO_USER_POOL_ID": cognito_user_pool_id,
                        "COGNITO_APP_CLIENT_ID": cognito_app_client_id,
                        "COGNITO_REGION": self.region,
                        "AWS_REGION": self.region,
                        "BEDROCK_MODEL_ID": "anthropic.claude-3-sonnet-20240229-v1:0",
                    },
                ),
                asset=backend_image,
            ),
            instance_role=instance_role,
            cpu=apprunner.Cpu.ONE_VCPU,
            memory=apprunner.Memory.TWO_GB,
        )

        # ==================== Frontend (S3 + CloudFront) ====================
        
        # S3 bucket for frontend
        frontend_bucket = s3.Bucket(
            self,
            "FrontendBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        # CloudFront OAC for S3
        oac = cloudfront.S3OriginAccessControl(
            self,
            "OAC",
            signing=cloudfront.Signing.SIGV4_ALWAYS,
        )

        # CloudFront distribution
        distribution = cloudfront.Distribution(
            self,
            "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(
                    frontend_bucket,
                    origin_access_control=oac,
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
            additional_behaviors={
                "/api/*": cloudfront.BehaviorOptions(
                    origin=origins.HttpOrigin(
                        backend_service.service_url.replace("https://", ""),
                    ),
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.HTTPS_ONLY,
                    allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                    cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                    origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
                ),
            },
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0),
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0),
                ),
            ],
        )

        # Grant CloudFront access to S3
        frontend_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[frontend_bucket.arn_for_objects("*")],
                principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{self.account}:distribution/{distribution.distribution_id}"
                    }
                },
            )
        )

        # Deploy frontend to S3
        s3_deploy.BucketDeployment(
            self,
            "DeployFrontend",
            sources=[s3_deploy.Source.asset("../frontend/dist")],
            destination_bucket=frontend_bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )

        # ==================== Outputs ====================
        
        CfnOutput(
            self,
            "CloudFrontURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="Application URL",
        )

        CfnOutput(
            self,
            "BackendURL",
            value=backend_service.service_url,
            description="Backend API URL",
        )

        CfnOutput(
            self,
            "S3BucketName",
            value=frontend_bucket.bucket_name,
            description="Frontend S3 Bucket",
        )
