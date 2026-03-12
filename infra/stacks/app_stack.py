"""Full application stack - Frontend (S3+CloudFront) + Backend (EC2)."""
from aws_cdk import (
    Stack,
    CfnOutput,
    CfnCondition,
    RemovalPolicy,
    Duration,
    Fn,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_ecr_assets as ecr_assets,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_cloudwatch as cloudwatch,
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
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Instance type from CDK context (default: c7i.xlarge)
        instance_type_str = self.node.try_get_context("instance_type") or "c7i.xlarge"

        # ==================== Backend (EC2) ====================

        # Docker image from backend directory (force AMD64)
        backend_image = ecr_assets.DockerImageAsset(
            self,
            "BackendImage",
            directory="../backend",
            platform=ecr_assets.Platform.LINUX_AMD64,
        )

        # VPC - 2 AZs, public subnets only, no NAT gateway
        vpc = ec2.Vpc(
            self,
            "Vpc",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
            ],
        )

        # Security group - allow port 8000 from CloudFront only
        sg = ec2.SecurityGroup(
            self,
            "BackendSG",
            vpc=vpc,
            description="Allow HTTP 8000 from CloudFront only",
            allow_all_outbound=True,
        )

        # Look up the AWS-managed CloudFront origin-facing prefix list
        cf_prefix_list = ec2.PrefixList.from_lookup(
            self,
            "CloudFrontPrefixList",
            prefix_list_name="com.amazonaws.global.cloudfront.origin-facing",
        )
        sg.add_ingress_rule(
            cf_prefix_list,
            ec2.Port.tcp(8000),
            "Allow API access on port 8000 from CloudFront only",
        )
        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH access",
        )

        # IAM role for EC2 instance
        instance_role = iam.Role(
            self,
            "EC2InstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonEC2ContainerRegistryReadOnly"
                ),
            ],
        )

        # Grant Bedrock access
        instance_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream",
                ],
                resources=["*"],
            )
        )

        # User data script: install Docker, pull image, run container
        # Robust version with retries, logging, and health check
        ecr_domain = f"{self.account}.dkr.ecr.{self.region}.amazonaws.com"
        image_uri = backend_image.image_uri

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash",
            "exec > >(tee /var/log/plaid-setup.log) 2>&1",
            "set -euxo pipefail",
            "",
            "echo '=== PLAID Backend Setup Starting ==='",
            "date",
            "",
            "# Install Docker",
            "yum update -y",
            "yum install -y docker",
            "systemctl enable docker && systemctl start docker",
            "echo 'Docker installed and started'",
            "",
            "# ECR login with retries",
            "set +e",
            "for i in 1 2 3 4 5; do",
            f"  aws ecr get-login-password --region {self.region}"
            f" | docker login --username AWS --password-stdin {ecr_domain}"
            " && break",
            '  echo "ECR login attempt $i failed, retrying in 10s..."',
            "  sleep 10",
            "done",
            "set -e",
            "",
            "# Pull image with retries",
            "set +e",
            "for i in 1 2 3 4 5; do",
            f"  docker pull {image_uri} && break",
            '  echo "Docker pull attempt $i failed, retrying in 15s..."',
            "  sleep 15",
            "done",
            "set -e",
            "",
            "# Run the container",
            f"docker run -d --restart=always --name plaid-backend"
            f" -p 8000:8000"
            f" -e COGNITO_USER_POOL_ID={cognito_user_pool_id}"
            f" -e COGNITO_APP_CLIENT_ID={cognito_app_client_id}"
            f" -e COGNITO_REGION={self.region}"
            f" -e AWS_REGION={self.region}"
            f' -e BEDROCK_MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"'
            f" -e SOLVER_TIMEOUT_SECONDS=180"
            f" {image_uri}",
            "",
            "# Health check: wait for container to respond",
            "echo 'Waiting for backend to become healthy...'",
            "set +e",
            "for i in $(seq 1 30); do",
            "  curl -sf http://localhost:8000/api/health > /dev/null 2>&1 && echo 'Backend is healthy!' && break",
            '  echo "Health check attempt $i/30 - not ready yet"',
            "  sleep 10",
            "done",
            "",
            "# Final status",
            "if curl -sf http://localhost:8000/api/health > /dev/null 2>&1; then",
            "  echo '=== PLAID Backend Setup Complete ==='",
            "else",
            "  echo '=== WARNING: Backend did not pass health check ==='",
            "  docker logs plaid-backend",
            "fi",
            "set -e",
            "date",
        )

        # EC2 instance
        instance = ec2.Instance(
            self,
            "BackendInstance",
            vpc=vpc,
            instance_type=ec2.InstanceType(instance_type_str),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            security_group=sg,
            role=instance_role,
            user_data=user_data,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        # Grant ECR pull to instance
        backend_image.repository.grant_pull(instance_role)

        # CloudWatch alarm for EC2 status check failures
        cloudwatch.Alarm(
            self,
            "StatusCheckAlarm",
            metric=cloudwatch.Metric(
                namespace="AWS/EC2",
                metric_name="StatusCheckFailed",
                dimensions_map={"InstanceId": instance.instance_id},
                period=Duration.minutes(1),
                statistic="Maximum",
            ),
            evaluation_periods=2,
            threshold=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            alarm_description="Alarm when EC2 instance fails status checks",
            treat_missing_data=cloudwatch.TreatMissingData.BREACHING,
        )

        # Condition for region-specific DNS format
        CfnCondition(
            self, "IsUsEast1",
            expression=Fn.condition_equals(self.region, "us-east-1"),
        )

        # Elastic IP for stable CloudFront origin
        eip = ec2.CfnEIP(self, "BackendEIP")
        ec2.CfnEIPAssociation(
            self,
            "BackendEIPAssoc",
            eip=eip.ref,
            instance_id=instance.instance_id,
        )

        # CloudFront requires a domain name, not an IP address.
        # Use the instance's public DNS (assigned after EIP association).
        # us-east-1: ec2-X-X-X-X.compute-1.amazonaws.com
        # other:     ec2-X-X-X-X.REGION.compute.amazonaws.com
        ip_dashed = Fn.join("-", Fn.split(".", eip.attr_public_ip))
        origin_domain = Fn.condition_if(
            "IsUsEast1",
            Fn.join("", ["ec2-", ip_dashed, ".compute-1.amazonaws.com"]),
            Fn.join("", ["ec2-", ip_dashed, ".", self.region, ".compute.amazonaws.com"]),
        ).to_string()

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
                        origin_domain,
                        http_port=8000,
                        protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                        read_timeout=Duration.seconds(180),
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
                        "AWS:SourceArn": (
                            f"arn:aws:cloudfront::{self.account}"
                            f":distribution/{distribution.distribution_id}"
                        )
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
            "BackendPublicIP",
            value=eip.ref,
            description="Backend EC2 Elastic IP",
        )

        CfnOutput(
            self,
            "BackendURL",
            value=f"http://{eip.ref}:8000",
            description="Backend API URL",
        )

        CfnOutput(
            self,
            "S3BucketName",
            value=frontend_bucket.bucket_name,
            description="Frontend S3 Bucket",
        )

        CfnOutput(
            self,
            "InstanceId",
            value=instance.instance_id,
            description="EC2 Instance ID (for SSM access)",
        )
