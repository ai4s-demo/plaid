r'''
# AWS::AppRunner Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_apprunner_alpha as apprunner
```

## Introduction

AWS App Runner is a fully managed service that makes it easy for developers to quickly deploy containerized web applications and APIs, at scale and with no prior infrastructure experience required. Start with your source code or a container image. App Runner automatically builds and deploys the web application and load balances traffic with encryption. App Runner also scales up or down automatically to meet your traffic needs. With App Runner, rather than thinking about servers or scaling, you have more time to focus on your applications.

## Service

The `Service` construct allows you to create AWS App Runner services with `ECR Public`, `ECR` or `Github` with the `source` property in the following scenarios:

* `Source.fromEcr()` - To define the source repository from `ECR`.
* `Source.fromEcrPublic()` - To define the source repository from `ECR Public`.
* `Source.fromGitHub()` - To define the source repository from the `Github repository`.
* `Source.fromAsset()` - To define the source from local asset directory.

The `Service` construct implements `IGrantable`.

## ECR Public

To create a `Service` with ECR Public:

```python
apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    )
)
```

## ECR

To create a `Service` from an existing ECR repository:

```python
import aws_cdk.aws_ecr as ecr


apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr(
        image_configuration=apprunner.ImageConfiguration(port=80),
        repository=ecr.Repository.from_repository_name(self, "NginxRepository", "nginx"),
        tag_or_digest="latest"
    )
)
```

To create a `Service` from local docker image asset directory built and pushed to Amazon ECR:

You can specify whether to enable continuous integration from the source repository with the `autoDeploymentsEnabled` flag.

```python
import aws_cdk.aws_ecr_assets as assets


image_asset = assets.DockerImageAsset(self, "ImageAssets",
    directory=path.join(__dirname, "docker.assets")
)
apprunner.Service(self, "Service",
    source=apprunner.Source.from_asset(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        asset=image_asset
    ),
    auto_deployments_enabled=True
)
```

## GitHub

To create a `Service` from the GitHub repository, you need to specify an existing App Runner `Connection`.

See [Managing App Runner connections](https://docs.aws.amazon.com/apprunner/latest/dg/manage-connections.html) for more details.

```python
apprunner.Service(self, "Service",
    source=apprunner.Source.from_git_hub(
        repository_url="https://github.com/aws-containers/hello-app-runner",
        branch="main",
        configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
        connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
    )
)
```

Use `codeConfigurationValues` to override configuration values with the `API` configuration source type.

```python
apprunner.Service(self, "Service",
    source=apprunner.Source.from_git_hub(
        repository_url="https://github.com/aws-containers/hello-app-runner",
        branch="main",
        configuration_source=apprunner.ConfigurationSourceType.API,
        code_configuration_values=apprunner.CodeConfigurationValues(
            runtime=apprunner.Runtime.PYTHON_3,
            port="8000",
            start_command="python app.py",
            build_command="yum install -y pycairo && pip install -r requirements.txt"
        ),
        connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
    )
)
```

## IAM Roles

You are allowed to define `instanceRole` and `accessRole` for the `Service`.

`instanceRole` - The IAM role that provides permissions to your App Runner service. These are permissions that
your code needs when it calls any AWS APIs. If not defined, a new instance role will be generated
when required.

To add IAM policy statements to this role, use `addToRolePolicy()`:

```python
import aws_cdk.aws_iam as iam


service = apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    )
)

service.add_to_role_policy(iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    actions=["s3:GetObject"],
    resources=["*"]
))
```

`accessRole` - The IAM role that grants the App Runner service access to a source repository. It's required for
ECR image repositories (but not for ECR Public repositories). If not defined, a new access role will be generated
when required.

See [App Runner IAM Roles](https://docs.aws.amazon.com/apprunner/latest/dg/security_iam_service-with-iam.html#security_iam_service-with-iam-roles) for more details.

## Auto Scaling Configuration

To associate an App Runner service with a custom Auto Scaling Configuration, define `autoScalingConfiguration` for the service.

```python
auto_scaling_configuration = apprunner.AutoScalingConfiguration(self, "AutoScalingConfiguration",
    auto_scaling_configuration_name="MyAutoScalingConfiguration",
    max_concurrency=150,
    max_size=20,
    min_size=5
)

apprunner.Service(self, "DemoService",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    ),
    auto_scaling_configuration=auto_scaling_configuration
)
```

## VPC Connector

To associate an App Runner service with a custom VPC, define `vpcConnector` for the service.

```python
import aws_cdk.aws_ec2 as ec2


vpc = ec2.Vpc(self, "Vpc",
    ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16")
)

vpc_connector = apprunner.VpcConnector(self, "VpcConnector",
    vpc=vpc,
    vpc_subnets=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC),
    vpc_connector_name="MyVpcConnector"
)

apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    ),
    vpc_connector=vpc_connector
)
```

## VPC Ingress Connection

To make your App Runner service private and only accessible from within a VPC use the `isPubliclyAccessible` property and associate it to a `VpcIngressConnection` resource.

To set up a `VpcIngressConnection`, specify a VPC, a VPC Interface Endpoint, and the App Runner service.
Also you must set `isPubliclyAccessible` property in ther `Service` to `false`.

For more information, see [Enabling Private endpoint for incoming traffic](https://docs.aws.amazon.com/apprunner/latest/dg/network-pl.html).

```python
import aws_cdk.aws_ec2 as ec2

# vpc: ec2.Vpc


interface_vpc_endpoint = ec2.InterfaceVpcEndpoint(self, "MyVpcEndpoint",
    vpc=vpc,
    service=ec2.InterfaceVpcEndpointAwsService.APP_RUNNER_REQUESTS,
    private_dns_enabled=False
)

service = apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(
            port=8000
        ),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    ),
    is_publicly_accessible=False
)

apprunner.VpcIngressConnection(self, "VpcIngressConnection",
    vpc=vpc,
    interface_vpc_endpoint=interface_vpc_endpoint,
    service=service
)
```

## Dual Stack

To use dual stack (IPv4 and IPv6) for your incoming public network configuration, set `ipAddressType` to `IpAddressType.DUAL_STACK`.

```python
apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    ),
    ip_address_type=apprunner.IpAddressType.DUAL_STACK
)
```

**Note**: Currently, App Runner supports dual stack for only Public endpoint.
Only IPv4 is supported for Private endpoint.
If you update a service that's using dual-stack Public endpoint to a Private endpoint,
your App Runner service will default to support only IPv4 for Private endpoint and fail
to receive traffic originating from IPv6 endpoint.

## Secrets Manager

To include environment variables integrated with AWS Secrets Manager, use the `environmentSecrets` attribute.
You can use the `addSecret` method from the App Runner `Service` class to include secrets from outside the
service definition.

```python
import aws_cdk.aws_secretsmanager as secretsmanager
import aws_cdk.aws_ssm as ssm

# stack: Stack


secret = secretsmanager.Secret(stack, "Secret")
parameter = ssm.StringParameter.from_secure_string_parameter_attributes(stack, "Parameter",
    parameter_name="/name",
    version=1
)

service = apprunner.Service(stack, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(
            port=8000,
            environment_secrets={
                "SECRET": apprunner.Secret.from_secrets_manager(secret),
                "PARAMETER": apprunner.Secret.from_ssm_parameter(parameter),
                "SECRET_ID": apprunner.Secret.from_secrets_manager_version(secret, version_id="version-id"),
                "SECRET_STAGE": apprunner.Secret.from_secrets_manager_version(secret, version_stage="version-stage")
            }
        ),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    )
)

service.add_secret("LATER_SECRET", apprunner.Secret.from_secrets_manager(secret, "field"))
```

## Use a customer managed key

To use a customer managed key for your source encryption, use the `kmsKey` attribute.

```python
import aws_cdk.aws_kms as kms

# kms_key: kms.IKey


apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    ),
    kms_key=kms_key
)
```

## HealthCheck

To configure the health check for the service, use the `healthCheck` attribute.

You can specify it by static methods `HealthCheck.http` or `HealthCheck.tcp`.

```python
apprunner.Service(self, "Service",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    ),
    health_check=apprunner.HealthCheck.http(
        healthy_threshold=5,
        interval=Duration.seconds(10),
        path="/",
        timeout=Duration.seconds(10),
        unhealthy_threshold=10
    )
)
```

## Observability Configuration

To associate an App Runner service with a custom observability configuration, use the `observabilityConfiguration` property.

```python
observability_configuration = apprunner.ObservabilityConfiguration(self, "ObservabilityConfiguration",
    observability_configuration_name="MyObservabilityConfiguration",
    trace_configuration_vendor=apprunner.TraceConfigurationVendor.AWSXRAY
)

apprunner.Service(self, "DemoService",
    source=apprunner.Source.from_ecr_public(
        image_configuration=apprunner.ImageConfiguration(port=8000),
        image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
    ),
    observability_configuration=observability_configuration
)
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_apprunner as _aws_cdk_aws_apprunner_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_ceddda9d
import aws_cdk.aws_ecr_assets as _aws_cdk_aws_ecr_assets_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d
import aws_cdk.interfaces.aws_kms as _aws_cdk_interfaces_aws_kms_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.AssetProps",
    jsii_struct_bases=[],
    name_mapping={"asset": "asset", "image_configuration": "imageConfiguration"},
)
class AssetProps:
    def __init__(
        self,
        *,
        asset: "_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset",
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of the image repository for ``Source.fromAsset()``.

        :param asset: (experimental) Represents the docker image asset.
        :param image_configuration: (experimental) The image configuration for the image built from the asset. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ecr_assets as assets
            
            
            image_asset = assets.DockerImageAsset(self, "ImageAssets",
                directory=path.join(__dirname, "docker.assets")
            )
            apprunner.Service(self, "Service",
                source=apprunner.Source.from_asset(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    asset=image_asset
                ),
                auto_deployments_enabled=True
            )
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08a8fbd7cfe007fa7ce008c1d8a55a2e2ebe4d254c9dd541108007ec6a8e6e5)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset": asset,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration

    @builtins.property
    def asset(self) -> "_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset":
        '''(experimental) Represents the docker image asset.

        :stability: experimental
        '''
        result = self._values.get("asset")
        assert result is not None, "Required property 'asset' is missing"
        return typing.cast("_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset", result)

    @builtins.property
    def image_configuration(self) -> typing.Optional["ImageConfiguration"]:
        '''(experimental) The image configuration for the image built from the asset.

        :default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
        :stability: experimental
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["ImageConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.AutoScalingConfigurationAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_configuration_name": "autoScalingConfigurationName",
        "auto_scaling_configuration_revision": "autoScalingConfigurationRevision",
    },
)
class AutoScalingConfigurationAttributes:
    def __init__(
        self,
        *,
        auto_scaling_configuration_name: builtins.str,
        auto_scaling_configuration_revision: jsii.Number,
    ) -> None:
        '''(experimental) Attributes for the App Runner Auto Scaling Configuration.

        :param auto_scaling_configuration_name: (experimental) The name of the Auto Scaling Configuration.
        :param auto_scaling_configuration_revision: (experimental) The revision of the Auto Scaling Configuration.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            
            auto_scaling_configuration_attributes = apprunner_alpha.AutoScalingConfigurationAttributes(
                auto_scaling_configuration_name="autoScalingConfigurationName",
                auto_scaling_configuration_revision=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f04f1b647655a9262a279fbe04c1b04be071f7dcc95c2b4faec882a230929f6)
            check_type(argname="argument auto_scaling_configuration_name", value=auto_scaling_configuration_name, expected_type=type_hints["auto_scaling_configuration_name"])
            check_type(argname="argument auto_scaling_configuration_revision", value=auto_scaling_configuration_revision, expected_type=type_hints["auto_scaling_configuration_revision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_scaling_configuration_name": auto_scaling_configuration_name,
            "auto_scaling_configuration_revision": auto_scaling_configuration_revision,
        }

    @builtins.property
    def auto_scaling_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the Auto Scaling Configuration.

        :stability: experimental
        '''
        result = self._values.get("auto_scaling_configuration_name")
        assert result is not None, "Required property 'auto_scaling_configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_scaling_configuration_revision(self) -> jsii.Number:
        '''(experimental) The revision of the Auto Scaling Configuration.

        :stability: experimental
        '''
        result = self._values.get("auto_scaling_configuration_revision")
        assert result is not None, "Required property 'auto_scaling_configuration_revision' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalingConfigurationAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.AutoScalingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_configuration_name": "autoScalingConfigurationName",
        "max_concurrency": "maxConcurrency",
        "max_size": "maxSize",
        "min_size": "minSize",
    },
)
class AutoScalingConfigurationProps:
    def __init__(
        self,
        *,
        auto_scaling_configuration_name: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[jsii.Number] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties of the App Runner Auto Scaling Configuration.

        :param auto_scaling_configuration_name: (experimental) The name for the Auto Scaling Configuration. Default: - a name generated by CloudFormation
        :param max_concurrency: (experimental) The maximum number of concurrent requests that an instance processes. If the number of concurrent requests exceeds this limit, App Runner scales the service up. Must be between 1 and 200. Default: 100
        :param max_size: (experimental) The maximum number of instances that a service scales up to. At most maxSize instances actively serve traffic for your service. Must be between 1 and 25. Default: 25
        :param min_size: (experimental) The minimum number of instances that App Runner provisions for a service. The service always has at least minSize provisioned instances. Must be between 1 and 25. Default: 1

        :stability: experimental
        :exampleMetadata: infused

        Example::

            auto_scaling_configuration = apprunner.AutoScalingConfiguration(self, "AutoScalingConfiguration",
                auto_scaling_configuration_name="MyAutoScalingConfiguration",
                max_concurrency=150,
                max_size=20,
                min_size=5
            )
            
            apprunner.Service(self, "DemoService",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                ),
                auto_scaling_configuration=auto_scaling_configuration
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d409b1d530a639b5498bf567d8dcb90e3d933f850862a29f70518344ec6b1623)
            check_type(argname="argument auto_scaling_configuration_name", value=auto_scaling_configuration_name, expected_type=type_hints["auto_scaling_configuration_name"])
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_configuration_name is not None:
            self._values["auto_scaling_configuration_name"] = auto_scaling_configuration_name
        if max_concurrency is not None:
            self._values["max_concurrency"] = max_concurrency
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size

    @builtins.property
    def auto_scaling_configuration_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the Auto Scaling Configuration.

        :default: - a name generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("auto_scaling_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrency(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of concurrent requests that an instance processes.

        If the number of concurrent requests exceeds this limit, App Runner scales the service up.

        Must be between 1 and 200.

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("max_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of instances that a service scales up to.

        At most maxSize instances actively serve traffic for your service.

        Must be between 1 and 25.

        :default: 25

        :stability: experimental
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum number of instances that App Runner provisions for a service.

        The service always has at least minSize provisioned instances.

        Must be between 1 and 25.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.CodeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_source": "configurationSource",
        "configuration_values": "configurationValues",
    },
)
class CodeConfiguration:
    def __init__(
        self,
        *,
        configuration_source: "ConfigurationSourceType",
        configuration_values: typing.Optional[typing.Union["CodeConfigurationValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Describes the configuration that AWS App Runner uses to build and run an App Runner service from a source code repository.

        :param configuration_source: (experimental) The source of the App Runner configuration.
        :param configuration_values: (experimental) The basic configuration for building and running the App Runner service. Use it to quickly launch an App Runner service without providing a apprunner.yaml file in the source code repository (or ignoring the file if it exists). Default: - not specified. Use ``apprunner.yaml`` instead.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfiguration.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            
            # runtime: apprunner_alpha.Runtime
            # secret: apprunner_alpha.Secret
            
            code_configuration = apprunner_alpha.CodeConfiguration(
                configuration_source=apprunner_alpha.ConfigurationSourceType.REPOSITORY,
            
                # the properties below are optional
                configuration_values=apprunner_alpha.CodeConfigurationValues(
                    runtime=runtime,
            
                    # the properties below are optional
                    build_command="buildCommand",
                    environment={
                        "environment_key": "environment"
                    },
                    environment_secrets={
                        "environment_secrets_key": secret
                    },
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    port="port",
                    start_command="startCommand"
                )
            )
        '''
        if isinstance(configuration_values, dict):
            configuration_values = CodeConfigurationValues(**configuration_values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae937db922ae6dad5990a7f5c386f8b91b134eb32d1e222b6397b08cd185df6)
            check_type(argname="argument configuration_source", value=configuration_source, expected_type=type_hints["configuration_source"])
            check_type(argname="argument configuration_values", value=configuration_values, expected_type=type_hints["configuration_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_source": configuration_source,
        }
        if configuration_values is not None:
            self._values["configuration_values"] = configuration_values

    @builtins.property
    def configuration_source(self) -> "ConfigurationSourceType":
        '''(experimental) The source of the App Runner configuration.

        :stability: experimental
        '''
        result = self._values.get("configuration_source")
        assert result is not None, "Required property 'configuration_source' is missing"
        return typing.cast("ConfigurationSourceType", result)

    @builtins.property
    def configuration_values(self) -> typing.Optional["CodeConfigurationValues"]:
        '''(experimental) The basic configuration for building and running the App Runner service.

        Use it to quickly launch an App Runner service without providing a apprunner.yaml file in the
        source code repository (or ignoring the file if it exists).

        :default: - not specified. Use ``apprunner.yaml`` instead.

        :stability: experimental
        '''
        result = self._values.get("configuration_values")
        return typing.cast(typing.Optional["CodeConfigurationValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.CodeConfigurationValues",
    jsii_struct_bases=[],
    name_mapping={
        "runtime": "runtime",
        "build_command": "buildCommand",
        "environment": "environment",
        "environment_secrets": "environmentSecrets",
        "environment_variables": "environmentVariables",
        "port": "port",
        "start_command": "startCommand",
    },
)
class CodeConfigurationValues:
    def __init__(
        self,
        *,
        runtime: "Runtime",
        build_command: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_secrets: typing.Optional[typing.Mapping[builtins.str, "Secret"]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        port: typing.Optional[builtins.str] = None,
        start_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Describes the basic configuration needed for building and running an AWS App Runner service.

        This type doesn't support the full set of possible configuration options. Fur full configuration capabilities,
        use a ``apprunner.yaml`` file in the source code repository.

        :param runtime: (experimental) A runtime environment type for building and running an App Runner service. It represents a programming language runtime.
        :param build_command: (experimental) The command App Runner runs to build your application. Default: - no build command.
        :param environment: (deprecated) The environment variables that are available to your running App Runner service. Default: - no environment variables.
        :param environment_secrets: (experimental) The environment secrets that are available to your running App Runner service. Default: - no environment secrets.
        :param environment_variables: (experimental) The environment variables that are available to your running App Runner service. Default: - no environment variables.
        :param port: (experimental) The port that your application listens to in the container. Default: 8080
        :param start_command: (experimental) The command App Runner runs to start your application. Default: - no start command.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            apprunner.Service(self, "Service",
                source=apprunner.Source.from_git_hub(
                    repository_url="https://github.com/aws-containers/hello-app-runner",
                    branch="main",
                    configuration_source=apprunner.ConfigurationSourceType.API,
                    code_configuration_values=apprunner.CodeConfigurationValues(
                        runtime=apprunner.Runtime.PYTHON_3,
                        port="8000",
                        start_command="python app.py",
                        build_command="yum install -y pycairo && pip install -r requirements.txt"
                    ),
                    connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfca01cbfa9c6291b2ceb7b79d2e8973e68667f4752762fc65620ae5c1d16bec)
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_secrets", value=environment_secrets, expected_type=type_hints["environment_secrets"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "runtime": runtime,
        }
        if build_command is not None:
            self._values["build_command"] = build_command
        if environment is not None:
            self._values["environment"] = environment
        if environment_secrets is not None:
            self._values["environment_secrets"] = environment_secrets
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if port is not None:
            self._values["port"] = port
        if start_command is not None:
            self._values["start_command"] = start_command

    @builtins.property
    def runtime(self) -> "Runtime":
        '''(experimental) A runtime environment type for building and running an App Runner service.

        It represents
        a programming language runtime.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast("Runtime", result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The command App Runner runs to build your application.

        :default: - no build command.

        :stability: experimental
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) The environment variables that are available to your running App Runner service.

        :default: - no environment variables.

        :deprecated: use environmentVariables.

        :stability: deprecated
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "Secret"]]:
        '''(experimental) The environment secrets that are available to your running App Runner service.

        :default: - no environment secrets.

        :stability: experimental
        '''
        result = self._values.get("environment_secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "Secret"]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables that are available to your running App Runner service.

        :default: - no environment variables.

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''(experimental) The port that your application listens to in the container.

        :default: 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The command App Runner runs to start your application.

        :default: - no start command.

        :stability: experimental
        '''
        result = self._values.get("start_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfigurationValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.CodeRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "code_configuration": "codeConfiguration",
        "connection": "connection",
        "repository_url": "repositoryUrl",
        "source_code_version": "sourceCodeVersion",
    },
)
class CodeRepositoryProps:
    def __init__(
        self,
        *,
        code_configuration: typing.Union["CodeConfiguration", typing.Dict[builtins.str, typing.Any]],
        connection: "GitHubConnection",
        repository_url: builtins.str,
        source_code_version: typing.Union["SourceCodeVersion", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties of the CodeRepository.

        :param code_configuration: (experimental) Configuration for building and running the service from a source code repository.
        :param connection: (experimental) The App Runner connection for GitHub.
        :param repository_url: (experimental) The location of the repository that contains the source code.
        :param source_code_version: (experimental) The version that should be used within the source code repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            
            # git_hub_connection: apprunner_alpha.GitHubConnection
            # runtime: apprunner_alpha.Runtime
            # secret: apprunner_alpha.Secret
            
            code_repository_props = apprunner_alpha.CodeRepositoryProps(
                code_configuration=apprunner_alpha.CodeConfiguration(
                    configuration_source=apprunner_alpha.ConfigurationSourceType.REPOSITORY,
            
                    # the properties below are optional
                    configuration_values=apprunner_alpha.CodeConfigurationValues(
                        runtime=runtime,
            
                        # the properties below are optional
                        build_command="buildCommand",
                        environment={
                            "environment_key": "environment"
                        },
                        environment_secrets={
                            "environment_secrets_key": secret
                        },
                        environment_variables={
                            "environment_variables_key": "environmentVariables"
                        },
                        port="port",
                        start_command="startCommand"
                    )
                ),
                connection=git_hub_connection,
                repository_url="repositoryUrl",
                source_code_version=apprunner_alpha.SourceCodeVersion(
                    type="type",
                    value="value"
                )
            )
        '''
        if isinstance(code_configuration, dict):
            code_configuration = CodeConfiguration(**code_configuration)
        if isinstance(source_code_version, dict):
            source_code_version = SourceCodeVersion(**source_code_version)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8f6208c6ccadbd7f2f6a081b0c3ce8ee7e55504225e9ba72fd0d33a99d04d6)
            check_type(argname="argument code_configuration", value=code_configuration, expected_type=type_hints["code_configuration"])
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            check_type(argname="argument source_code_version", value=source_code_version, expected_type=type_hints["source_code_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code_configuration": code_configuration,
            "connection": connection,
            "repository_url": repository_url,
            "source_code_version": source_code_version,
        }

    @builtins.property
    def code_configuration(self) -> "CodeConfiguration":
        '''(experimental) Configuration for building and running the service from a source code repository.

        :stability: experimental
        '''
        result = self._values.get("code_configuration")
        assert result is not None, "Required property 'code_configuration' is missing"
        return typing.cast("CodeConfiguration", result)

    @builtins.property
    def connection(self) -> "GitHubConnection":
        '''(experimental) The App Runner connection for GitHub.

        :stability: experimental
        '''
        result = self._values.get("connection")
        assert result is not None, "Required property 'connection' is missing"
        return typing.cast("GitHubConnection", result)

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''(experimental) The location of the repository that contains the source code.

        :stability: experimental
        '''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_code_version(self) -> "SourceCodeVersion":
        '''(experimental) The version that should be used within the source code repository.

        :stability: experimental
        '''
        result = self._values.get("source_code_version")
        assert result is not None, "Required property 'source_code_version' is missing"
        return typing.cast("SourceCodeVersion", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apprunner-alpha.ConfigurationSourceType")
class ConfigurationSourceType(enum.Enum):
    '''(experimental) The source of the App Runner configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apprunner.Service(self, "Service",
            source=apprunner.Source.from_git_hub(
                repository_url="https://github.com/aws-containers/hello-app-runner",
                branch="main",
                configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
                connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
            )
        )
    '''

    REPOSITORY = "REPOSITORY"
    '''(experimental) App Runner reads configuration values from ``the apprunner.yaml`` file in the source code repository and ignores ``configurationValues``.

    :stability: experimental
    '''
    API = "API"
    '''(experimental) App Runner uses configuration values provided in ``configurationValues`` and ignores the ``apprunner.yaml`` file in the source code repository.

    :stability: experimental
    '''


class Cpu(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apprunner-alpha.Cpu"):
    '''(experimental) The number of CPU units reserved for each instance of your App Runner service.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner_alpha as apprunner_alpha
        
        cpu = apprunner_alpha.Cpu.FOUR_VCPU
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, unit: builtins.str) -> "Cpu":
        '''(experimental) Custom CPU unit.

        :param unit: custom CPU unit.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-cpu
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb36987110835c7df289907b6abce68377a8816dcc626b59e4634b110b68502a)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        return typing.cast("Cpu", jsii.sinvoke(cls, "of", [unit]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FOUR_VCPU")
    def FOUR_VCPU(cls) -> "Cpu":
        '''(experimental) 4 vCPU.

        :stability: experimental
        '''
        return typing.cast("Cpu", jsii.sget(cls, "FOUR_VCPU"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HALF_VCPU")
    def HALF_VCPU(cls) -> "Cpu":
        '''(experimental) 0.5 vCPU.

        :stability: experimental
        '''
        return typing.cast("Cpu", jsii.sget(cls, "HALF_VCPU"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ONE_VCPU")
    def ONE_VCPU(cls) -> "Cpu":
        '''(experimental) 1 vCPU.

        :stability: experimental
        '''
        return typing.cast("Cpu", jsii.sget(cls, "ONE_VCPU"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="QUARTER_VCPU")
    def QUARTER_VCPU(cls) -> "Cpu":
        '''(experimental) 0.25 vCPU.

        :stability: experimental
        '''
        return typing.cast("Cpu", jsii.sget(cls, "QUARTER_VCPU"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TWO_VCPU")
    def TWO_VCPU(cls) -> "Cpu":
        '''(experimental) 2 vCPU.

        :stability: experimental
        '''
        return typing.cast("Cpu", jsii.sget(cls, "TWO_VCPU"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        '''(experimental) The unit of CPU.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "unit"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.EcrProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository": "repository",
        "image_configuration": "imageConfiguration",
        "tag": "tag",
        "tag_or_digest": "tagOrDigest",
    },
)
class EcrProps:
    def __init__(
        self,
        *,
        repository: "_aws_cdk_aws_ecr_ceddda9d.IRepository",
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[builtins.str] = None,
        tag_or_digest: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties of the image repository for ``Source.fromEcr()``.

        :param repository: (experimental) Represents the ECR repository.
        :param image_configuration: (experimental) The image configuration for the image from ECR. Default: - no image configuration will be passed. The default ``port`` will be 8080.
        :param tag: (deprecated) Image tag. Default: - 'latest'
        :param tag_or_digest: (experimental) Image tag or digest (digests must start with ``sha256:``). Default: - 'latest'

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ecr as ecr
            
            
            apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr(
                    image_configuration=apprunner.ImageConfiguration(port=80),
                    repository=ecr.Repository.from_repository_name(self, "NginxRepository", "nginx"),
                    tag_or_digest="latest"
                )
            )
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d314b79b8d81f041cdd01718f3ef34ccc715997cf7fd3d81583ef7cdd22d75a)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument tag_or_digest", value=tag_or_digest, expected_type=type_hints["tag_or_digest"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration
        if tag is not None:
            self._values["tag"] = tag
        if tag_or_digest is not None:
            self._values["tag_or_digest"] = tag_or_digest

    @builtins.property
    def repository(self) -> "_aws_cdk_aws_ecr_ceddda9d.IRepository":
        '''(experimental) Represents the ECR repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast("_aws_cdk_aws_ecr_ceddda9d.IRepository", result)

    @builtins.property
    def image_configuration(self) -> typing.Optional["ImageConfiguration"]:
        '''(experimental) The image configuration for the image from ECR.

        :default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
        :stability: experimental
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["ImageConfiguration"], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Image tag.

        :default: - 'latest'

        :deprecated: use ``tagOrDigest``

        :stability: deprecated
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_or_digest(self) -> typing.Optional[builtins.str]:
        '''(experimental) Image tag or digest (digests must start with ``sha256:``).

        :default: - 'latest'

        :stability: experimental
        '''
        result = self._values.get("tag_or_digest")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.EcrPublicProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_identifier": "imageIdentifier",
        "image_configuration": "imageConfiguration",
    },
)
class EcrPublicProps:
    def __init__(
        self,
        *,
        image_identifier: builtins.str,
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of the image repository for ``Source.fromEcrPublic()``.

        :param image_identifier: (experimental) The ECR Public image URI.
        :param image_configuration: (experimental) The image configuration for the image from ECR Public. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iam as iam
            
            
            service = apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                )
            )
            
            service.add_to_role_policy(iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=["*"]
            ))
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c946837bfdb36bdd4b295396580cb8fb7d16dbdf8cd7e7d26f40af21c98350)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_identifier": image_identifier,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration

    @builtins.property
    def image_identifier(self) -> builtins.str:
        '''(experimental) The ECR Public image URI.

        :stability: experimental
        '''
        result = self._values.get("image_identifier")
        assert result is not None, "Required property 'image_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_configuration(self) -> typing.Optional["ImageConfiguration"]:
        '''(experimental) The image configuration for the image from ECR Public.

        :default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
        :stability: experimental
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["ImageConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrPublicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubConnection(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.GitHubConnection",
):
    '''(experimental) Represents the App Runner connection that enables the App Runner service to connect to a source repository.

    It's required for GitHub code repositories.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apprunner.Service(self, "Service",
            source=apprunner.Source.from_git_hub(
                repository_url="https://github.com/aws-containers/hello-app-runner",
                branch="main",
                configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
                connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
            )
        )
    '''

    def __init__(self, arn: builtins.str) -> None:
        '''
        :param arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa88c7a5842afea11022e7d7cb6979e91cfb24043dd76ce07670f71189675f3f)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        jsii.create(self.__class__, self, [arn])

    @jsii.member(jsii_name="fromConnectionArn")
    @builtins.classmethod
    def from_connection_arn(cls, arn: builtins.str) -> "GitHubConnection":
        '''(experimental) Using existing App Runner connection by specifying the connection ARN.

        :param arn: connection ARN.

        :return: Connection

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f2a8dc46245c67294c19ebb6e56670f52e1c8498f08a6f3cc64085d586c648)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast("GitHubConnection", jsii.sinvoke(cls, "fromConnectionArn", [arn]))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Connection for App Runner service to connect to the repository.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.GithubRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_source": "configurationSource",
        "connection": "connection",
        "repository_url": "repositoryUrl",
        "branch": "branch",
        "code_configuration_values": "codeConfigurationValues",
    },
)
class GithubRepositoryProps:
    def __init__(
        self,
        *,
        configuration_source: "ConfigurationSourceType",
        connection: "GitHubConnection",
        repository_url: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        code_configuration_values: typing.Optional[typing.Union["CodeConfigurationValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of the Github repository for ``Source.fromGitHub()``.

        :param configuration_source: (experimental) The source of the App Runner configuration.
        :param connection: (experimental) ARN of the connection to Github. Only required for Github source.
        :param repository_url: (experimental) The location of the repository that contains the source code.
        :param branch: (experimental) The branch name that represents a specific version for the repository. Default: main
        :param code_configuration_values: (experimental) The code configuration values. Will be ignored if configurationSource is ``REPOSITORY``. Default: - no values will be passed. The ``apprunner.yaml`` from the github reopsitory will be used instead.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            apprunner.Service(self, "Service",
                source=apprunner.Source.from_git_hub(
                    repository_url="https://github.com/aws-containers/hello-app-runner",
                    branch="main",
                    configuration_source=apprunner.ConfigurationSourceType.REPOSITORY,
                    connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
                )
            )
        '''
        if isinstance(code_configuration_values, dict):
            code_configuration_values = CodeConfigurationValues(**code_configuration_values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d401724ed1ffda098b7c914516349006ef7826c8ceec08ba31a7c624efd3db14)
            check_type(argname="argument configuration_source", value=configuration_source, expected_type=type_hints["configuration_source"])
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument code_configuration_values", value=code_configuration_values, expected_type=type_hints["code_configuration_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_source": configuration_source,
            "connection": connection,
            "repository_url": repository_url,
        }
        if branch is not None:
            self._values["branch"] = branch
        if code_configuration_values is not None:
            self._values["code_configuration_values"] = code_configuration_values

    @builtins.property
    def configuration_source(self) -> "ConfigurationSourceType":
        '''(experimental) The source of the App Runner configuration.

        :stability: experimental
        '''
        result = self._values.get("configuration_source")
        assert result is not None, "Required property 'configuration_source' is missing"
        return typing.cast("ConfigurationSourceType", result)

    @builtins.property
    def connection(self) -> "GitHubConnection":
        '''(experimental) ARN of the connection to Github.

        Only required for Github source.

        :stability: experimental
        '''
        result = self._values.get("connection")
        assert result is not None, "Required property 'connection' is missing"
        return typing.cast("GitHubConnection", result)

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''(experimental) The location of the repository that contains the source code.

        :stability: experimental
        '''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The branch name that represents a specific version for the repository.

        :default: main

        :stability: experimental
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_configuration_values(self) -> typing.Optional["CodeConfigurationValues"]:
        '''(experimental) The code configuration values.

        Will be ignored if configurationSource is ``REPOSITORY``.

        :default: - no values will be passed. The ``apprunner.yaml`` from the github reopsitory will be used instead.

        :stability: experimental
        '''
        result = self._values.get("code_configuration_values")
        return typing.cast(typing.Optional["CodeConfigurationValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HealthCheck(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.HealthCheck",
):
    '''(experimental) Contains static factory methods for creating health checks for different protocols.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apprunner.Service(self, "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            ),
            health_check=apprunner.HealthCheck.http(
                healthy_threshold=5,
                interval=Duration.seconds(10),
                path="/",
                timeout=Duration.seconds(10),
                unhealthy_threshold=10
            )
        )
    '''

    @jsii.member(jsii_name="http")
    @builtins.classmethod
    def http(
        cls,
        *,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> "HealthCheck":
        '''(experimental) Construct a HTTP health check.

        :param healthy_threshold: (experimental) The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Default: 1
        :param interval: (experimental) The time interval, in seconds, between health checks. Default: Duration.seconds(5)
        :param path: (experimental) The URL that health check requests are sent to. Default: /
        :param timeout: (experimental) The time, in seconds, to wait for a health check response before deciding it failed. Default: Duration.seconds(2)
        :param unhealthy_threshold: (experimental) The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Default: 5

        :stability: experimental
        '''
        options = HttpHealthCheckOptions(
            healthy_threshold=healthy_threshold,
            interval=interval,
            path=path,
            timeout=timeout,
            unhealthy_threshold=unhealthy_threshold,
        )

        return typing.cast("HealthCheck", jsii.sinvoke(cls, "http", [options]))

    @jsii.member(jsii_name="tcp")
    @builtins.classmethod
    def tcp(
        cls,
        *,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> "HealthCheck":
        '''(experimental) Construct a TCP health check.

        :param healthy_threshold: (experimental) The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Default: 1
        :param interval: (experimental) The time interval, in seconds, between health checks. Default: Duration.seconds(5)
        :param timeout: (experimental) The time, in seconds, to wait for a health check response before deciding it failed. Default: Duration.seconds(2)
        :param unhealthy_threshold: (experimental) The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Default: 5

        :stability: experimental
        '''
        options = TcpHealthCheckOptions(
            healthy_threshold=healthy_threshold,
            interval=interval,
            timeout=timeout,
            unhealthy_threshold=unhealthy_threshold,
        )

        return typing.cast("HealthCheck", jsii.sinvoke(cls, "tcp", [options]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
    ) -> "_aws_cdk_aws_apprunner_ceddda9d.CfnService.HealthCheckConfigurationProperty":
        '''
        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_apprunner_ceddda9d.CfnService.HealthCheckConfigurationProperty", jsii.invoke(self, "bind", []))

    @builtins.property
    @jsii.member(jsii_name="healthCheckProtocolType")
    def health_check_protocol_type(self) -> "HealthCheckProtocolType":
        '''
        :stability: experimental
        '''
        return typing.cast("HealthCheckProtocolType", jsii.get(self, "healthCheckProtocolType"))

    @builtins.property
    @jsii.member(jsii_name="healthyThreshold")
    def healthy_threshold(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "healthyThreshold"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> "_aws_cdk_ceddda9d.Duration":
        '''
        :stability: experimental
        '''
        return typing.cast("_aws_cdk_ceddda9d.Duration", jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "_aws_cdk_ceddda9d.Duration":
        '''
        :stability: experimental
        '''
        return typing.cast("_aws_cdk_ceddda9d.Duration", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="unhealthyThreshold")
    def unhealthy_threshold(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "unhealthyThreshold"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))


@jsii.enum(jsii_type="@aws-cdk/aws-apprunner-alpha.HealthCheckProtocolType")
class HealthCheckProtocolType(enum.Enum):
    '''(experimental) The health check protocol type.

    :stability: experimental
    '''

    HTTP = "HTTP"
    '''(experimental) HTTP protocol.

    :stability: experimental
    '''
    TCP = "TCP"
    '''(experimental) TCP protocol.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.HttpHealthCheckOptions",
    jsii_struct_bases=[],
    name_mapping={
        "healthy_threshold": "healthyThreshold",
        "interval": "interval",
        "path": "path",
        "timeout": "timeout",
        "unhealthy_threshold": "unhealthyThreshold",
    },
)
class HttpHealthCheckOptions:
    def __init__(
        self,
        *,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties used to define HTTP Based healthchecks.

        :param healthy_threshold: (experimental) The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Default: 1
        :param interval: (experimental) The time interval, in seconds, between health checks. Default: Duration.seconds(5)
        :param path: (experimental) The URL that health check requests are sent to. Default: /
        :param timeout: (experimental) The time, in seconds, to wait for a health check response before deciding it failed. Default: Duration.seconds(2)
        :param unhealthy_threshold: (experimental) The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Default: 5

        :stability: experimental
        :exampleMetadata: infused

        Example::

            apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                ),
                health_check=apprunner.HealthCheck.http(
                    healthy_threshold=5,
                    interval=Duration.seconds(10),
                    path="/",
                    timeout=Duration.seconds(10),
                    unhealthy_threshold=10
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29cfd6afd364301a292f444ae0cb2af3e2fbd32a8e5c375cbc091c6d48b6083)
            check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if healthy_threshold is not None:
            self._values["healthy_threshold"] = healthy_threshold
        if interval is not None:
            self._values["interval"] = interval
        if path is not None:
            self._values["path"] = path
        if timeout is not None:
            self._values["timeout"] = timeout
        if unhealthy_threshold is not None:
            self._values["unhealthy_threshold"] = unhealthy_threshold

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of consecutive checks that must succeed before App Runner decides that the service is healthy.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("healthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The time interval, in seconds, between health checks.

        :default: Duration.seconds(5)

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL that health check requests are sent to.

        :default: /

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The time, in seconds, to wait for a health check response before deciding it failed.

        :default: Duration.seconds(2)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of consecutive checks that must fail before App Runner decides that the service is unhealthy.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("unhealthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpHealthCheckOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-apprunner-alpha.IAutoScalingConfiguration")
class IAutoScalingConfiguration(
    _aws_cdk_ceddda9d.IResource,
    typing_extensions.Protocol,
):
    '''(experimental) Represents the App Runner Auto Scaling Configuration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationArn")
    def auto_scaling_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationName")
    def auto_scaling_configuration_name(self) -> builtins.str:
        '''(experimental) The Name of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationRevision")
    def auto_scaling_configuration_revision(self) -> jsii.Number:
        '''(experimental) The revision of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAutoScalingConfigurationProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents the App Runner Auto Scaling Configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apprunner-alpha.IAutoScalingConfiguration"

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationArn")
    def auto_scaling_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "autoScalingConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationName")
    def auto_scaling_configuration_name(self) -> builtins.str:
        '''(experimental) The Name of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "autoScalingConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationRevision")
    def auto_scaling_configuration_revision(self) -> jsii.Number:
        '''(experimental) The revision of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "autoScalingConfigurationRevision"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAutoScalingConfiguration).__jsii_proxy_class__ = lambda : _IAutoScalingConfigurationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apprunner-alpha.IObservabilityConfiguration")
class IObservabilityConfiguration(
    _aws_cdk_ceddda9d.IResource,
    typing_extensions.Protocol,
):
    '''(experimental) Represents the App Runner Observability configuration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationArn")
    def observability_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationName")
    def observability_configuration_name(self) -> builtins.str:
        '''(experimental) The Name of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationRevision")
    def observability_configuration_revision(self) -> jsii.Number:
        '''(experimental) The revision of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IObservabilityConfigurationProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents the App Runner Observability configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apprunner-alpha.IObservabilityConfiguration"

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationArn")
    def observability_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "observabilityConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationName")
    def observability_configuration_name(self) -> builtins.str:
        '''(experimental) The Name of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "observabilityConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationRevision")
    def observability_configuration_revision(self) -> jsii.Number:
        '''(experimental) The revision of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "observabilityConfigurationRevision"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IObservabilityConfiguration).__jsii_proxy_class__ = lambda : _IObservabilityConfigurationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apprunner-alpha.IService")
class IService(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents the App Runner Service.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The ARN of the service.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) The Name of the service.

        :stability: experimental
        '''
        ...


class _IServiceProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents the App Runner Service.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apprunner-alpha.IService"

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The ARN of the service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) The Name of the service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IService).__jsii_proxy_class__ = lambda : _IServiceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apprunner-alpha.IVpcConnector")
class IVpcConnector(
    _aws_cdk_ceddda9d.IResource,
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    typing_extensions.Protocol,
):
    '''(experimental) Represents the App Runner VPC Connector.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorArn")
    def vpc_connector_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorName")
    def vpc_connector_name(self) -> builtins.str:
        '''(experimental) The Name of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorRevision")
    def vpc_connector_revision(self) -> jsii.Number:
        '''(experimental) The revision of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IVpcConnectorProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
):
    '''(experimental) Represents the App Runner VPC Connector.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apprunner-alpha.IVpcConnector"

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorArn")
    def vpc_connector_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorArn"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorName")
    def vpc_connector_name(self) -> builtins.str:
        '''(experimental) The Name of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorName"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorRevision")
    def vpc_connector_revision(self) -> jsii.Number:
        '''(experimental) The revision of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "vpcConnectorRevision"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVpcConnector).__jsii_proxy_class__ = lambda : _IVpcConnectorProxy


@jsii.interface(jsii_type="@aws-cdk/aws-apprunner-alpha.IVpcIngressConnection")
class IVpcIngressConnection(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents the App Runner VPC Ingress Connection.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="vpcIngressConnectionArn")
    def vpc_ingress_connection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the VPC Ingress Connection.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcIngressConnectionName")
    def vpc_ingress_connection_name(self) -> builtins.str:
        '''(experimental) The name of the VPC Ingress Connection.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IVpcIngressConnectionProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents the App Runner VPC Ingress Connection.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apprunner-alpha.IVpcIngressConnection"

    @builtins.property
    @jsii.member(jsii_name="vpcIngressConnectionArn")
    def vpc_ingress_connection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the VPC Ingress Connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcIngressConnectionArn"))

    @builtins.property
    @jsii.member(jsii_name="vpcIngressConnectionName")
    def vpc_ingress_connection_name(self) -> builtins.str:
        '''(experimental) The name of the VPC Ingress Connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcIngressConnectionName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVpcIngressConnection).__jsii_proxy_class__ = lambda : _IVpcIngressConnectionProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.ImageConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "environment": "environment",
        "environment_secrets": "environmentSecrets",
        "environment_variables": "environmentVariables",
        "port": "port",
        "start_command": "startCommand",
    },
)
class ImageConfiguration:
    def __init__(
        self,
        *,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_secrets: typing.Optional[typing.Mapping[builtins.str, "Secret"]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        port: typing.Optional[jsii.Number] = None,
        start_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Describes the configuration that AWS App Runner uses to run an App Runner service using an image pulled from a source image repository.

        :param environment: (deprecated) Environment variables that are available to your running App Runner service. Default: - no environment variables
        :param environment_secrets: (experimental) Environment secrets that are available to your running App Runner service. Default: - no environment secrets
        :param environment_variables: (experimental) Environment variables that are available to your running App Runner service. Default: - no environment variables
        :param port: (experimental) The port that your application listens to in the container. Default: 8080
        :param start_command: (experimental) An optional command that App Runner runs to start the application in the source image. If specified, this command overrides the Docker image’s default start command. Default: - no start command

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iam as iam
            
            
            service = apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                )
            )
            
            service.add_to_role_policy(iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=["*"]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada5ceaac12328ac3e20c585b8447f90f84c0d2bf9b8461f994b196a6f5ca778)
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_secrets", value=environment_secrets, expected_type=type_hints["environment_secrets"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument start_command", value=start_command, expected_type=type_hints["start_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if environment is not None:
            self._values["environment"] = environment
        if environment_secrets is not None:
            self._values["environment_secrets"] = environment_secrets
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if port is not None:
            self._values["port"] = port
        if start_command is not None:
            self._values["start_command"] = start_command

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) Environment variables that are available to your running App Runner service.

        :default: - no environment variables

        :deprecated: use environmentVariables.

        :stability: deprecated
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "Secret"]]:
        '''(experimental) Environment secrets that are available to your running App Runner service.

        :default: - no environment secrets

        :stability: experimental
        '''
        result = self._values.get("environment_secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "Secret"]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables that are available to your running App Runner service.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port that your application listens to in the container.

        :default: 8080

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional command that App Runner runs to start the application in the source image.

        If specified, this command overrides the Docker image’s default start command.

        :default: - no start command

        :stability: experimental
        '''
        result = self._values.get("start_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.ImageRepository",
    jsii_struct_bases=[],
    name_mapping={
        "image_identifier": "imageIdentifier",
        "image_repository_type": "imageRepositoryType",
        "image_configuration": "imageConfiguration",
    },
)
class ImageRepository:
    def __init__(
        self,
        *,
        image_identifier: builtins.str,
        image_repository_type: "ImageRepositoryType",
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Describes a source image repository.

        :param image_identifier: (experimental) The identifier of the image. For ``ECR_PUBLIC`` imageRepositoryType, the identifier domain should always be ``public.ecr.aws``. For ``ECR``, the pattern should be ``([0-9]{12}.dkr.ecr.[a-z\\-]+-[0-9]{1}.amazonaws.com\\/.*)``.
        :param image_repository_type: (experimental) The type of the image repository. This reflects the repository provider and whether the repository is private or public.
        :param image_configuration: (experimental) Configuration for running the identified image. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            
            # secret: apprunner_alpha.Secret
            
            image_repository = apprunner_alpha.ImageRepository(
                image_identifier="imageIdentifier",
                image_repository_type=apprunner_alpha.ImageRepositoryType.ECR_PUBLIC,
            
                # the properties below are optional
                image_configuration=apprunner_alpha.ImageConfiguration(
                    environment={
                        "environment_key": "environment"
                    },
                    environment_secrets={
                        "environment_secrets_key": secret
                    },
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    port=123,
                    start_command="startCommand"
                )
            )
        '''
        if isinstance(image_configuration, dict):
            image_configuration = ImageConfiguration(**image_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5739f9e0d186c5ae07f20de42ed39073fd22f6a1e220dd2c9b94782477260351)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
            check_type(argname="argument image_repository_type", value=image_repository_type, expected_type=type_hints["image_repository_type"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_identifier": image_identifier,
            "image_repository_type": image_repository_type,
        }
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration

    @builtins.property
    def image_identifier(self) -> builtins.str:
        '''(experimental) The identifier of the image.

        For ``ECR_PUBLIC`` imageRepositoryType, the identifier domain should
        always be ``public.ecr.aws``. For ``ECR``, the pattern should be
        ``([0-9]{12}.dkr.ecr.[a-z\\-]+-[0-9]{1}.amazonaws.com\\/.*)``.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imagerepository.html
        :stability: experimental
        '''
        result = self._values.get("image_identifier")
        assert result is not None, "Required property 'image_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_repository_type(self) -> "ImageRepositoryType":
        '''(experimental) The type of the image repository.

        This reflects the repository provider and whether
        the repository is private or public.

        :stability: experimental
        '''
        result = self._values.get("image_repository_type")
        assert result is not None, "Required property 'image_repository_type' is missing"
        return typing.cast("ImageRepositoryType", result)

    @builtins.property
    def image_configuration(self) -> typing.Optional["ImageConfiguration"]:
        '''(experimental) Configuration for running the identified image.

        :default: - no image configuration will be passed. The default ``port`` will be 8080.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-imageconfiguration.html#cfn-apprunner-service-imageconfiguration-port
        :stability: experimental
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["ImageConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apprunner-alpha.ImageRepositoryType")
class ImageRepositoryType(enum.Enum):
    '''(experimental) The image repository types.

    :stability: experimental
    '''

    ECR_PUBLIC = "ECR_PUBLIC"
    '''(experimental) Amazon ECR Public.

    :stability: experimental
    '''
    ECR = "ECR"
    '''(experimental) Amazon ECR.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-apprunner-alpha.IpAddressType")
class IpAddressType(enum.Enum):
    '''(experimental) The IP address type for your incoming public network configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apprunner.Service(self, "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            ),
            ip_address_type=apprunner.IpAddressType.DUAL_STACK
        )
    '''

    IPV4 = "IPV4"
    '''(experimental) IPV4.

    :stability: experimental
    '''
    DUAL_STACK = "DUAL_STACK"
    '''(experimental) DUAL_STACK.

    :stability: experimental
    '''


class Memory(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apprunner-alpha.Memory"):
    '''(experimental) The amount of memory reserved for each instance of your App Runner service.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner_alpha as apprunner_alpha
        
        memory = apprunner_alpha.Memory.EIGHT_GB
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, unit: builtins.str) -> "Memory":
        '''(experimental) Custom Memory unit.

        :param unit: custom Memory unit.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-instanceconfiguration.html#cfn-apprunner-service-instanceconfiguration-memory
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aef99b08abb67e03d37b29a11f144ec6ca20853863c7f628ad9b0aa4181206e)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        return typing.cast("Memory", jsii.sinvoke(cls, "of", [unit]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EIGHT_GB")
    def EIGHT_GB(cls) -> "Memory":
        '''(experimental) 8 GB(for 4 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "EIGHT_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FOUR_GB")
    def FOUR_GB(cls) -> "Memory":
        '''(experimental) 4 GB(for 1 or 2 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "FOUR_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HALF_GB")
    def HALF_GB(cls) -> "Memory":
        '''(experimental) 0.5 GB(for 0.25 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "HALF_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ONE_GB")
    def ONE_GB(cls) -> "Memory":
        '''(experimental) 1 GB(for 0.25 or 0.5 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "ONE_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SIX_GB")
    def SIX_GB(cls) -> "Memory":
        '''(experimental) 6 GB(for 2 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "SIX_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TEN_GB")
    def TEN_GB(cls) -> "Memory":
        '''(experimental) 10 GB(for 4 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "TEN_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="THREE_GB")
    def THREE_GB(cls) -> "Memory":
        '''(experimental) 3 GB(for 1 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "THREE_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TWELVE_GB")
    def TWELVE_GB(cls) -> "Memory":
        '''(experimental) 12 GB(for 4 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "TWELVE_GB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TWO_GB")
    def TWO_GB(cls) -> "Memory":
        '''(experimental) 2 GB(for 1 vCPU).

        :stability: experimental
        '''
        return typing.cast("Memory", jsii.sget(cls, "TWO_GB"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        '''(experimental) The unit of memory.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "unit"))


@jsii.implements(IObservabilityConfiguration)
class ObservabilityConfiguration(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.ObservabilityConfiguration",
):
    '''(experimental) The App Runner Observability configuration.

    :stability: experimental
    :resource: AWS::AppRunner::ObservabilityConfiguration
    :exampleMetadata: infused

    Example::

        observability_configuration = apprunner.ObservabilityConfiguration(self, "ObservabilityConfiguration",
            observability_configuration_name="MyObservabilityConfiguration",
            trace_configuration_vendor=apprunner.TraceConfigurationVendor.AWSXRAY
        )
        
        apprunner.Service(self, "DemoService",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            ),
            observability_configuration=observability_configuration
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        trace_configuration_vendor: "TraceConfigurationVendor",
        observability_configuration_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param trace_configuration_vendor: (experimental) The implementation provider chosen for tracing App Runner services.
        :param observability_configuration_name: (experimental) The name for the ObservabilityConfiguration. Default: - a name generated by CloudFormation

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421591e7b88a9ca05adf379a20784325b1be3eedc888d670052b856051ee10aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ObservabilityConfigurationProps(
            trace_configuration_vendor=trace_configuration_vendor,
            observability_configuration_name=observability_configuration_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        observability_configuration_arn: builtins.str,
    ) -> "IObservabilityConfiguration":
        '''(experimental) Imports an App Runner Observability Configuration from its ARN.

        :param scope: -
        :param id: -
        :param observability_configuration_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b8985e0f2351adfd5874d7295c72db8512a2ddf22cc04e25d61e3a0649da91)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument observability_configuration_arn", value=observability_configuration_arn, expected_type=type_hints["observability_configuration_arn"])
        return typing.cast("IObservabilityConfiguration", jsii.sinvoke(cls, "fromArn", [scope, id, observability_configuration_arn]))

    @jsii.member(jsii_name="fromObservabilityConfigurationAttributes")
    @builtins.classmethod
    def from_observability_configuration_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        observability_configuration_name: builtins.str,
        observability_configuration_revision: jsii.Number,
    ) -> "IObservabilityConfiguration":
        '''(experimental) Imports an App Runner Observability Configuration from attributes.

        :param scope: -
        :param id: -
        :param observability_configuration_name: (experimental) The name of the Observability configuration.
        :param observability_configuration_revision: (experimental) The revision of the Observability configuration.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9c656cd02cc4dd8667796a9860a8e89b2774a2728bd9d9bdee1fe1c8222387)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ObservabilityConfigurationAttributes(
            observability_configuration_name=observability_configuration_name,
            observability_configuration_revision=observability_configuration_revision,
        )

        return typing.cast("IObservabilityConfiguration", jsii.sinvoke(cls, "fromObservabilityConfigurationAttributes", [scope, id, attrs]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationArn")
    def observability_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "observabilityConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationName")
    def observability_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "observabilityConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="observabilityConfigurationRevision")
    def observability_configuration_revision(self) -> jsii.Number:
        '''(experimental) The revision of the Observability configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "observabilityConfigurationRevision"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.ObservabilityConfigurationAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "observability_configuration_name": "observabilityConfigurationName",
        "observability_configuration_revision": "observabilityConfigurationRevision",
    },
)
class ObservabilityConfigurationAttributes:
    def __init__(
        self,
        *,
        observability_configuration_name: builtins.str,
        observability_configuration_revision: jsii.Number,
    ) -> None:
        '''(experimental) Attributes for the App Runner Observability configuration.

        :param observability_configuration_name: (experimental) The name of the Observability configuration.
        :param observability_configuration_revision: (experimental) The revision of the Observability configuration.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            
            observability_configuration_attributes = apprunner_alpha.ObservabilityConfigurationAttributes(
                observability_configuration_name="observabilityConfigurationName",
                observability_configuration_revision=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996b375337e44a1fc2e0188aa768043611d92db57b51134bfc70c46cd87178f3)
            check_type(argname="argument observability_configuration_name", value=observability_configuration_name, expected_type=type_hints["observability_configuration_name"])
            check_type(argname="argument observability_configuration_revision", value=observability_configuration_revision, expected_type=type_hints["observability_configuration_revision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "observability_configuration_name": observability_configuration_name,
            "observability_configuration_revision": observability_configuration_revision,
        }

    @builtins.property
    def observability_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the Observability configuration.

        :stability: experimental
        '''
        result = self._values.get("observability_configuration_name")
        assert result is not None, "Required property 'observability_configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def observability_configuration_revision(self) -> jsii.Number:
        '''(experimental) The revision of the Observability configuration.

        :stability: experimental
        '''
        result = self._values.get("observability_configuration_revision")
        assert result is not None, "Required property 'observability_configuration_revision' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityConfigurationAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.ObservabilityConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "trace_configuration_vendor": "traceConfigurationVendor",
        "observability_configuration_name": "observabilityConfigurationName",
    },
)
class ObservabilityConfigurationProps:
    def __init__(
        self,
        *,
        trace_configuration_vendor: "TraceConfigurationVendor",
        observability_configuration_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties of the AppRunner Observability configuration.

        :param trace_configuration_vendor: (experimental) The implementation provider chosen for tracing App Runner services.
        :param observability_configuration_name: (experimental) The name for the ObservabilityConfiguration. Default: - a name generated by CloudFormation

        :stability: experimental
        :exampleMetadata: infused

        Example::

            observability_configuration = apprunner.ObservabilityConfiguration(self, "ObservabilityConfiguration",
                observability_configuration_name="MyObservabilityConfiguration",
                trace_configuration_vendor=apprunner.TraceConfigurationVendor.AWSXRAY
            )
            
            apprunner.Service(self, "DemoService",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                ),
                observability_configuration=observability_configuration
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b324b5f514dc536d9d0d42556461942a8bb167ffa704ba3b757ee33b93849384)
            check_type(argname="argument trace_configuration_vendor", value=trace_configuration_vendor, expected_type=type_hints["trace_configuration_vendor"])
            check_type(argname="argument observability_configuration_name", value=observability_configuration_name, expected_type=type_hints["observability_configuration_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trace_configuration_vendor": trace_configuration_vendor,
        }
        if observability_configuration_name is not None:
            self._values["observability_configuration_name"] = observability_configuration_name

    @builtins.property
    def trace_configuration_vendor(self) -> "TraceConfigurationVendor":
        '''(experimental) The implementation provider chosen for tracing App Runner services.

        :stability: experimental
        '''
        result = self._values.get("trace_configuration_vendor")
        assert result is not None, "Required property 'trace_configuration_vendor' is missing"
        return typing.cast("TraceConfigurationVendor", result)

    @builtins.property
    def observability_configuration_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the ObservabilityConfiguration.

        :default: - a name generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("observability_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Runtime(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.Runtime",
):
    '''(experimental) The code runtimes.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        apprunner.Service(self, "Service",
            source=apprunner.Source.from_git_hub(
                repository_url="https://github.com/aws-containers/hello-app-runner",
                branch="main",
                configuration_source=apprunner.ConfigurationSourceType.API,
                code_configuration_values=apprunner.CodeConfigurationValues(
                    runtime=apprunner.Runtime.PYTHON_3,
                    port="8000",
                    start_command="python app.py",
                    build_command="yum install -y pycairo && pip install -r requirements.txt"
                ),
                connection=apprunner.GitHubConnection.from_connection_arn("CONNECTION_ARN")
            )
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "Runtime":
        '''(experimental) Other runtimes.

        :param name: runtime name.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-codeconfigurationvalues.html#cfn-apprunner-service-codeconfigurationvalues-runtime for all available runtimes.
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb5ee8b6854f81974bb8bee14dcd006f98f0b3c2cf8d852ea034c6fe09f2e35)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("Runtime", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CORRETTO_11")
    def CORRETTO_11(cls) -> "Runtime":
        '''(experimental) CORRETTO 11.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "CORRETTO_11"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CORRETTO_8")
    def CORRETTO_8(cls) -> "Runtime":
        '''(experimental) CORRETTO 8.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "CORRETTO_8"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_6")
    def DOTNET_6(cls) -> "Runtime":
        '''(experimental) .NET 6.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "DOTNET_6"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GO_1")
    def GO_1(cls) -> "Runtime":
        '''(experimental) Go 1.18.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "GO_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_12")
    def NODEJS_12(cls) -> "Runtime":
        '''(experimental) NodeJS 12.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "NODEJS_12"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_14")
    def NODEJS_14(cls) -> "Runtime":
        '''(experimental) NodeJS 14.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "NODEJS_14"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_16")
    def NODEJS_16(cls) -> "Runtime":
        '''(experimental) NodeJS 16.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "NODEJS_16"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_18")
    def NODEJS_18(cls) -> "Runtime":
        '''(experimental) NodeJS 18.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "NODEJS_18"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_22")
    def NODEJS_22(cls) -> "Runtime":
        '''(experimental) NodeJS 22.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "NODEJS_22"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PHP_81")
    def PHP_81(cls) -> "Runtime":
        '''(experimental) PHP 8.1.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "PHP_81"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_3")
    def PYTHON_3(cls) -> "Runtime":
        '''(experimental) Python 3.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "PYTHON_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_311")
    def PYTHON_311(cls) -> "Runtime":
        '''(experimental) Python 3.11.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "PYTHON_311"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RUBY_31")
    def RUBY_31(cls) -> "Runtime":
        '''(experimental) Ruby 3.1.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "RUBY_31"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The runtime name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class Secret(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-apprunner-alpha.Secret",
):
    '''(experimental) A secret environment variable.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_secretsmanager as secretsmanager
        import aws_cdk.aws_ssm as ssm
        
        # stack: Stack
        
        
        secret = secretsmanager.Secret(stack, "Secret")
        parameter = ssm.StringParameter.from_secure_string_parameter_attributes(stack, "Parameter",
            parameter_name="/name",
            version=1
        )
        
        service = apprunner.Service(stack, "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(
                    port=8000,
                    environment_secrets={
                        "SECRET": apprunner.Secret.from_secrets_manager(secret),
                        "PARAMETER": apprunner.Secret.from_ssm_parameter(parameter),
                        "SECRET_ID": apprunner.Secret.from_secrets_manager_version(secret, version_id="version-id"),
                        "SECRET_STAGE": apprunner.Secret.from_secrets_manager_version(secret, version_stage="version-stage")
                    }
                ),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            )
        )
        
        service.add_secret("LATER_SECRET", apprunner.Secret.from_secrets_manager(secret, "field"))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromSecretsManager")
    @builtins.classmethod
    def from_secrets_manager(
        cls,
        secret: "_aws_cdk_aws_secretsmanager_ceddda9d.ISecret",
        field: typing.Optional[builtins.str] = None,
    ) -> "Secret":
        '''(experimental) Creates a environment variable value from a secret stored in AWS Secrets Manager.

        :param secret: the secret stored in AWS Secrets Manager.
        :param field: the name of the field with the value that you want to set as the environment variable value. Only values in JSON format are supported. If you do not specify a JSON field, then the full content of the secret is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f059432ff1a488be31a6b1d8f1a5752dafa5774b88cec265c7bc1c9f73a4e5)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast("Secret", jsii.sinvoke(cls, "fromSecretsManager", [secret, field]))

    @jsii.member(jsii_name="fromSecretsManagerVersion")
    @builtins.classmethod
    def from_secrets_manager_version(
        cls,
        secret: "_aws_cdk_aws_secretsmanager_ceddda9d.ISecret",
        version_info: typing.Union["SecretVersionInfo", typing.Dict[builtins.str, typing.Any]],
        field: typing.Optional[builtins.str] = None,
    ) -> "Secret":
        '''(experimental) Creates a environment variable value from a secret stored in AWS Secrets Manager.

        :param secret: the secret stored in AWS Secrets Manager.
        :param version_info: the version information to reference the secret.
        :param field: the name of the field with the value that you want to set as the environment variable value. Only values in JSON format are supported. If you do not specify a JSON field, then the full content of the secret is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b639ee831f5eec1269609ed8aaace2c8c854af8a0a99896bf57f1ec44feec01d)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument version_info", value=version_info, expected_type=type_hints["version_info"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast("Secret", jsii.sinvoke(cls, "fromSecretsManagerVersion", [secret, version_info, field]))

    @jsii.member(jsii_name="fromSsmParameter")
    @builtins.classmethod
    def from_ssm_parameter(
        cls,
        parameter: "_aws_cdk_aws_ssm_ceddda9d.IParameter",
    ) -> "Secret":
        '''(experimental) Creates an environment variable value from a parameter stored in AWS Systems Manager Parameter Store.

        :param parameter: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cf075f1b7a42d19d2404c921c8ea9deeb7507e3c967f80806510dd249b0e77)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast("Secret", jsii.sinvoke(cls, "fromSsmParameter", [parameter]))

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grants reading the secret to a principal.

        [disable-awslint:no-grants]

        :param grantee: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="arn")
    @abc.abstractmethod
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the secret.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="hasField")
    @abc.abstractmethod
    def has_field(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this secret uses a specific JSON field.

        :stability: experimental
        '''
        ...


class _SecretProxy(Secret):
    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grants reading the secret to a principal.

        [disable-awslint:no-grants]

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd282bba973b7a15360293a7363341363c526b874ed3ef1f9c1b62187cd9f09)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the secret.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="hasField")
    def has_field(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this secret uses a specific JSON field.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "hasField"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Secret).__jsii_proxy_class__ = lambda : _SecretProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.SecretVersionInfo",
    jsii_struct_bases=[],
    name_mapping={"version_id": "versionId", "version_stage": "versionStage"},
)
class SecretVersionInfo:
    def __init__(
        self,
        *,
        version_id: typing.Optional[builtins.str] = None,
        version_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Specify the secret's version id or version stage.

        :param version_id: (experimental) version id of the secret. Default: - use default version id
        :param version_stage: (experimental) version stage of the secret. Default: - use default version stage

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_secretsmanager as secretsmanager
            import aws_cdk.aws_ssm as ssm
            
            # stack: Stack
            
            
            secret = secretsmanager.Secret(stack, "Secret")
            parameter = ssm.StringParameter.from_secure_string_parameter_attributes(stack, "Parameter",
                parameter_name="/name",
                version=1
            )
            
            service = apprunner.Service(stack, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(
                        port=8000,
                        environment_secrets={
                            "SECRET": apprunner.Secret.from_secrets_manager(secret),
                            "PARAMETER": apprunner.Secret.from_ssm_parameter(parameter),
                            "SECRET_ID": apprunner.Secret.from_secrets_manager_version(secret, version_id="version-id"),
                            "SECRET_STAGE": apprunner.Secret.from_secrets_manager_version(secret, version_stage="version-stage")
                        }
                    ),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                )
            )
            
            service.add_secret("LATER_SECRET", apprunner.Secret.from_secrets_manager(secret, "field"))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb5825ef7d4a37f927b0ae1f338a89941dd65787b02e3e4604e036461d23cc0)
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            check_type(argname="argument version_stage", value=version_stage, expected_type=type_hints["version_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if version_id is not None:
            self._values["version_id"] = version_id
        if version_stage is not None:
            self._values["version_stage"] = version_stage

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) version id of the secret.

        :default: - use default version id

        :stability: experimental
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) version stage of the secret.

        :default: - use default version stage

        :stability: experimental
        '''
        result = self._values.get("version_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretVersionInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IService, _aws_cdk_aws_iam_ceddda9d.IGrantable)
class Service(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.Service",
):
    '''(experimental) The App Runner Service.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iam as iam
        
        
        service = apprunner.Service(self, "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            )
        )
        
        service.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["s3:GetObject"],
            resources=["*"]
        ))
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        source: "Source",
        access_role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
        auto_deployments_enabled: typing.Optional[builtins.bool] = None,
        auto_scaling_configuration: typing.Optional["IAutoScalingConfiguration"] = None,
        cpu: typing.Optional["Cpu"] = None,
        health_check: typing.Optional["HealthCheck"] = None,
        instance_role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
        ip_address_type: typing.Optional["IpAddressType"] = None,
        is_publicly_accessible: typing.Optional[builtins.bool] = None,
        kms_key: typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"] = None,
        memory: typing.Optional["Memory"] = None,
        observability_configuration: typing.Optional["IObservabilityConfiguration"] = None,
        service_name: typing.Optional[builtins.str] = None,
        vpc_connector: typing.Optional["IVpcConnector"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source: (experimental) The source of the repository for the service.
        :param access_role: (experimental) The IAM role that grants the App Runner service access to a source repository. It's required for ECR image repositories (but not for ECR Public repositories). The role must be assumable by the 'build.apprunner.amazonaws.com' service principal. Default: - generate a new access role.
        :param auto_deployments_enabled: (experimental) Specifies whether to enable continuous integration from the source repository. If true, continuous integration from the source repository is enabled for the App Runner service. Each repository change (including any source code commit or new image version) starts a deployment. By default, App Runner sets to false for a source image that uses an ECR Public repository or an ECR repository that's in an AWS account other than the one that the service is in. App Runner sets to true in all other cases (which currently include a source code repository or a source image using a same-account ECR repository). Default: - no value will be passed.
        :param auto_scaling_configuration: (experimental) Specifies an App Runner Auto Scaling Configuration. A default configuration is either the AWS recommended configuration, or the configuration you set as the default. Default: - the latest revision of a default auto scaling configuration is used.
        :param cpu: (experimental) The number of CPU units reserved for each instance of your App Runner service. Default: Cpu.ONE_VCPU
        :param health_check: (experimental) Settings for the health check that AWS App Runner performs to monitor the health of a service. You can specify it by static methods ``HealthCheck.http`` or ``HealthCheck.tcp``. Default: - no health check configuration
        :param instance_role: (experimental) The IAM role that provides permissions to your App Runner service. These are permissions that your code needs when it calls any AWS APIs. The role must be assumable by the 'tasks.apprunner.amazonaws.com' service principal. Default: - generate a new instance role.
        :param ip_address_type: (experimental) The IP address type for your incoming public network configuration. Default: - IpAddressType.IPV4
        :param is_publicly_accessible: (experimental) Specifies whether your App Runner service is publicly accessible. If you use ``VpcIngressConnection``, you must set this property to ``false``. Default: true
        :param kms_key: (experimental) The customer managed key that AWS App Runner uses to encrypt copies of the source repository and service logs. Default: - Use an AWS managed key
        :param memory: (experimental) The amount of memory reserved for each instance of your App Runner service. Default: Memory.TWO_GB
        :param observability_configuration: (experimental) Settings for an App Runner observability configuration. Default: - no observability configuration resource is associated with the service.
        :param service_name: (experimental) Name of the service. Default: - auto-generated if undefined.
        :param vpc_connector: (experimental) Settings for an App Runner VPC connector to associate with the service. Default: - no VPC connector, uses the DEFAULT egress type instead

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d7d688c20ccfdaf4ead5ff12fa6ddcb24fd014e98a55a23b275e5f19aba35f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServiceProps(
            source=source,
            access_role=access_role,
            auto_deployments_enabled=auto_deployments_enabled,
            auto_scaling_configuration=auto_scaling_configuration,
            cpu=cpu,
            health_check=health_check,
            instance_role=instance_role,
            ip_address_type=ip_address_type,
            is_publicly_accessible=is_publicly_accessible,
            kms_key=kms_key,
            memory=memory,
            observability_configuration=observability_configuration,
            service_name=service_name,
            vpc_connector=vpc_connector,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromServiceAttributes")
    @builtins.classmethod
    def from_service_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        service_arn: builtins.str,
        service_name: builtins.str,
        service_status: builtins.str,
        service_url: builtins.str,
    ) -> "IService":
        '''(experimental) Import from service attributes.

        :param scope: -
        :param id: -
        :param service_arn: (experimental) The ARN of the service.
        :param service_name: (experimental) The name of the service.
        :param service_status: (experimental) The status of the service.
        :param service_url: (experimental) The URL of the service.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8409d8e0abf02901118bc4d7766649b9864e2eeb9bf9cb3aac48e20660a74c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ServiceAttributes(
            service_arn=service_arn,
            service_name=service_name,
            service_status=service_status,
            service_url=service_url,
        )

        return typing.cast("IService", jsii.sinvoke(cls, "fromServiceAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromServiceName")
    @builtins.classmethod
    def from_service_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        service_name: builtins.str,
    ) -> "IService":
        '''(experimental) Import from service name.

        :param scope: -
        :param id: -
        :param service_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150c152e2ac6267c6d21bd0cbf987659618d73bdd8ab39737c8f485109edb498)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        return typing.cast("IService", jsii.sinvoke(cls, "fromServiceName", [scope, id, service_name]))

    @jsii.member(jsii_name="addEnvironmentVariable")
    def add_environment_variable(self, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) This method adds an environment variable to the App Runner service.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f84babe1afe98a87221e6e76763e715d187e385c835bebec2fa7128a092bd4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addEnvironmentVariable", [name, value]))

    @jsii.member(jsii_name="addSecret")
    def add_secret(self, name: builtins.str, secret: "Secret") -> None:
        '''(experimental) This method adds a secret as environment variable to the App Runner service.

        :param name: -
        :param secret: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc967eafc1f0b4b004e18edc573b5becb1d10a6ea57ccc980fa0b326fd15f4b1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        return typing.cast(None, jsii.invoke(self, "addSecret", [name, secret]))

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(
        self,
        statement: "_aws_cdk_aws_iam_ceddda9d.PolicyStatement",
    ) -> None:
        '''(experimental) Adds a statement to the instance role.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5351c83ee7c098c1c4aac40f6a190c1c06bbd214351029437128b80b6a431a49)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(deprecated) Environment variables for this service.

        :deprecated: use environmentVariables.

        :stability: deprecated
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "_aws_cdk_aws_iam_ceddda9d.IPrincipal":
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.IPrincipal", jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''(experimental) The ID of the Service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) The name of the service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @builtins.property
    @jsii.member(jsii_name="serviceStatus")
    def service_status(self) -> builtins.str:
        '''(experimental) The status of the Service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceStatus"))

    @builtins.property
    @jsii.member(jsii_name="serviceUrl")
    def service_url(self) -> builtins.str:
        '''(experimental) The URL of the Service.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceUrl"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.ServiceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "service_arn": "serviceArn",
        "service_name": "serviceName",
        "service_status": "serviceStatus",
        "service_url": "serviceUrl",
    },
)
class ServiceAttributes:
    def __init__(
        self,
        *,
        service_arn: builtins.str,
        service_name: builtins.str,
        service_status: builtins.str,
        service_url: builtins.str,
    ) -> None:
        '''(experimental) Attributes for the App Runner Service.

        :param service_arn: (experimental) The ARN of the service.
        :param service_name: (experimental) The name of the service.
        :param service_status: (experimental) The status of the service.
        :param service_url: (experimental) The URL of the service.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            
            service_attributes = apprunner_alpha.ServiceAttributes(
                service_arn="serviceArn",
                service_name="serviceName",
                service_status="serviceStatus",
                service_url="serviceUrl"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c46766384c012b61899cf246f3108c023b5f905a313bafaeafc7f4429fa6fb6)
            check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument service_status", value=service_status, expected_type=type_hints["service_status"])
            check_type(argname="argument service_url", value=service_url, expected_type=type_hints["service_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_arn": service_arn,
            "service_name": service_name,
            "service_status": service_status,
            "service_url": service_url,
        }

    @builtins.property
    def service_arn(self) -> builtins.str:
        '''(experimental) The ARN of the service.

        :stability: experimental
        '''
        result = self._values.get("service_arn")
        assert result is not None, "Required property 'service_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''(experimental) The name of the service.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_status(self) -> builtins.str:
        '''(experimental) The status of the service.

        :stability: experimental
        '''
        result = self._values.get("service_status")
        assert result is not None, "Required property 'service_status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_url(self) -> builtins.str:
        '''(experimental) The URL of the service.

        :stability: experimental
        '''
        result = self._values.get("service_url")
        assert result is not None, "Required property 'service_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.ServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "access_role": "accessRole",
        "auto_deployments_enabled": "autoDeploymentsEnabled",
        "auto_scaling_configuration": "autoScalingConfiguration",
        "cpu": "cpu",
        "health_check": "healthCheck",
        "instance_role": "instanceRole",
        "ip_address_type": "ipAddressType",
        "is_publicly_accessible": "isPubliclyAccessible",
        "kms_key": "kmsKey",
        "memory": "memory",
        "observability_configuration": "observabilityConfiguration",
        "service_name": "serviceName",
        "vpc_connector": "vpcConnector",
    },
)
class ServiceProps:
    def __init__(
        self,
        *,
        source: "Source",
        access_role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
        auto_deployments_enabled: typing.Optional[builtins.bool] = None,
        auto_scaling_configuration: typing.Optional["IAutoScalingConfiguration"] = None,
        cpu: typing.Optional["Cpu"] = None,
        health_check: typing.Optional["HealthCheck"] = None,
        instance_role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
        ip_address_type: typing.Optional["IpAddressType"] = None,
        is_publicly_accessible: typing.Optional[builtins.bool] = None,
        kms_key: typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"] = None,
        memory: typing.Optional["Memory"] = None,
        observability_configuration: typing.Optional["IObservabilityConfiguration"] = None,
        service_name: typing.Optional[builtins.str] = None,
        vpc_connector: typing.Optional["IVpcConnector"] = None,
    ) -> None:
        '''(experimental) Properties of the AppRunner Service.

        :param source: (experimental) The source of the repository for the service.
        :param access_role: (experimental) The IAM role that grants the App Runner service access to a source repository. It's required for ECR image repositories (but not for ECR Public repositories). The role must be assumable by the 'build.apprunner.amazonaws.com' service principal. Default: - generate a new access role.
        :param auto_deployments_enabled: (experimental) Specifies whether to enable continuous integration from the source repository. If true, continuous integration from the source repository is enabled for the App Runner service. Each repository change (including any source code commit or new image version) starts a deployment. By default, App Runner sets to false for a source image that uses an ECR Public repository or an ECR repository that's in an AWS account other than the one that the service is in. App Runner sets to true in all other cases (which currently include a source code repository or a source image using a same-account ECR repository). Default: - no value will be passed.
        :param auto_scaling_configuration: (experimental) Specifies an App Runner Auto Scaling Configuration. A default configuration is either the AWS recommended configuration, or the configuration you set as the default. Default: - the latest revision of a default auto scaling configuration is used.
        :param cpu: (experimental) The number of CPU units reserved for each instance of your App Runner service. Default: Cpu.ONE_VCPU
        :param health_check: (experimental) Settings for the health check that AWS App Runner performs to monitor the health of a service. You can specify it by static methods ``HealthCheck.http`` or ``HealthCheck.tcp``. Default: - no health check configuration
        :param instance_role: (experimental) The IAM role that provides permissions to your App Runner service. These are permissions that your code needs when it calls any AWS APIs. The role must be assumable by the 'tasks.apprunner.amazonaws.com' service principal. Default: - generate a new instance role.
        :param ip_address_type: (experimental) The IP address type for your incoming public network configuration. Default: - IpAddressType.IPV4
        :param is_publicly_accessible: (experimental) Specifies whether your App Runner service is publicly accessible. If you use ``VpcIngressConnection``, you must set this property to ``false``. Default: true
        :param kms_key: (experimental) The customer managed key that AWS App Runner uses to encrypt copies of the source repository and service logs. Default: - Use an AWS managed key
        :param memory: (experimental) The amount of memory reserved for each instance of your App Runner service. Default: Memory.TWO_GB
        :param observability_configuration: (experimental) Settings for an App Runner observability configuration. Default: - no observability configuration resource is associated with the service.
        :param service_name: (experimental) Name of the service. Default: - auto-generated if undefined.
        :param vpc_connector: (experimental) Settings for an App Runner VPC connector to associate with the service. Default: - no VPC connector, uses the DEFAULT egress type instead

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iam as iam
            
            
            service = apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                )
            )
            
            service.add_to_role_policy(iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=["*"]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbb5d2c5a8f10a3d012f0035d55423352f4a7eff0eb19c057f0e1898a751cb6)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
            check_type(argname="argument auto_deployments_enabled", value=auto_deployments_enabled, expected_type=type_hints["auto_deployments_enabled"])
            check_type(argname="argument auto_scaling_configuration", value=auto_scaling_configuration, expected_type=type_hints["auto_scaling_configuration"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument is_publicly_accessible", value=is_publicly_accessible, expected_type=type_hints["is_publicly_accessible"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument observability_configuration", value=observability_configuration, expected_type=type_hints["observability_configuration"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument vpc_connector", value=vpc_connector, expected_type=type_hints["vpc_connector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if access_role is not None:
            self._values["access_role"] = access_role
        if auto_deployments_enabled is not None:
            self._values["auto_deployments_enabled"] = auto_deployments_enabled
        if auto_scaling_configuration is not None:
            self._values["auto_scaling_configuration"] = auto_scaling_configuration
        if cpu is not None:
            self._values["cpu"] = cpu
        if health_check is not None:
            self._values["health_check"] = health_check
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if is_publicly_accessible is not None:
            self._values["is_publicly_accessible"] = is_publicly_accessible
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if memory is not None:
            self._values["memory"] = memory
        if observability_configuration is not None:
            self._values["observability_configuration"] = observability_configuration
        if service_name is not None:
            self._values["service_name"] = service_name
        if vpc_connector is not None:
            self._values["vpc_connector"] = vpc_connector

    @builtins.property
    def source(self) -> "Source":
        '''(experimental) The source of the repository for the service.

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("Source", result)

    @builtins.property
    def access_role(self) -> typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"]:
        '''(experimental) The IAM role that grants the App Runner service access to a source repository.

        It's required for ECR image repositories (but not for ECR Public repositories).

        The role must be assumable by the 'build.apprunner.amazonaws.com' service principal.

        :default: - generate a new access role.

        :see: https://docs.aws.amazon.com/apprunner/latest/dg/security_iam_service-with-iam.html#security_iam_service-with-iam-roles-service.access
        :stability: experimental
        '''
        result = self._values.get("access_role")
        return typing.cast(typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"], result)

    @builtins.property
    def auto_deployments_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to enable continuous integration from the source repository.

        If true, continuous integration from the source repository is enabled for the App Runner service.
        Each repository change (including any source code commit or new image version) starts a deployment.
        By default, App Runner sets to false for a source image that uses an ECR Public repository or an ECR repository that's in an AWS account other than the one that the service is in.
        App Runner sets to true in all other cases (which currently include a source code repository or a source image using a same-account ECR repository).

        :default: - no value will be passed.

        :stability: experimental
        '''
        result = self._values.get("auto_deployments_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_scaling_configuration(
        self,
    ) -> typing.Optional["IAutoScalingConfiguration"]:
        '''(experimental) Specifies an App Runner Auto Scaling Configuration.

        A default configuration is either the AWS recommended configuration,
        or the configuration you set as the default.

        :default: - the latest revision of a default auto scaling configuration is used.

        :see: https://docs.aws.amazon.com/apprunner/latest/dg/manage-autoscaling.html
        :stability: experimental
        '''
        result = self._values.get("auto_scaling_configuration")
        return typing.cast(typing.Optional["IAutoScalingConfiguration"], result)

    @builtins.property
    def cpu(self) -> typing.Optional["Cpu"]:
        '''(experimental) The number of CPU units reserved for each instance of your App Runner service.

        :default: Cpu.ONE_VCPU

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional["Cpu"], result)

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        '''(experimental) Settings for the health check that AWS App Runner performs to monitor the health of a service.

        You can specify it by static methods ``HealthCheck.http`` or ``HealthCheck.tcp``.

        :default: - no health check configuration

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["HealthCheck"], result)

    @builtins.property
    def instance_role(self) -> typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"]:
        '''(experimental) The IAM role that provides permissions to your App Runner service.

        These are permissions that your code needs when it calls any AWS APIs.

        The role must be assumable by the 'tasks.apprunner.amazonaws.com' service principal.

        :default: - generate a new instance role.

        :see: https://docs.aws.amazon.com/apprunner/latest/dg/security_iam_service-with-iam.html#security_iam_service-with-iam-roles-service.instance
        :stability: experimental
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional["IpAddressType"]:
        '''(experimental) The IP address type for your incoming public network configuration.

        :default: - IpAddressType.IPV4

        :stability: experimental
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional["IpAddressType"], result)

    @builtins.property
    def is_publicly_accessible(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether your App Runner service is publicly accessible.

        If you use ``VpcIngressConnection``, you must set this property to ``false``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("is_publicly_accessible")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def kms_key(
        self,
    ) -> typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"]:
        '''(experimental) The customer managed key that AWS App Runner uses to encrypt copies of the source repository and service logs.

        :default: - Use an AWS managed key

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"], result)

    @builtins.property
    def memory(self) -> typing.Optional["Memory"]:
        '''(experimental) The amount of memory reserved for each instance of your App Runner service.

        :default: Memory.TWO_GB

        :stability: experimental
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional["Memory"], result)

    @builtins.property
    def observability_configuration(
        self,
    ) -> typing.Optional["IObservabilityConfiguration"]:
        '''(experimental) Settings for an App Runner observability configuration.

        :default: - no observability configuration resource is associated with the service.

        :stability: experimental
        '''
        result = self._values.get("observability_configuration")
        return typing.cast(typing.Optional["IObservabilityConfiguration"], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the service.

        :default: - auto-generated if undefined.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_connector(self) -> typing.Optional["IVpcConnector"]:
        '''(experimental) Settings for an App Runner VPC connector to associate with the service.

        :default: - no VPC connector, uses the DEFAULT egress type instead

        :stability: experimental
        '''
        result = self._values.get("vpc_connector")
        return typing.cast(typing.Optional["IVpcConnector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Source(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-apprunner-alpha.Source",
):
    '''(experimental) Represents the App Runner service source.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iam as iam
        
        
        service = apprunner.Service(self, "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            )
        )
        
        service.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["s3:GetObject"],
            resources=["*"]
        ))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        *,
        asset: "_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset",
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "AssetSource":
        '''(experimental) Source from local assets.

        :param asset: (experimental) Represents the docker image asset.
        :param image_configuration: (experimental) The image configuration for the image built from the asset. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        '''
        props = AssetProps(asset=asset, image_configuration=image_configuration)

        return typing.cast("AssetSource", jsii.sinvoke(cls, "fromAsset", [props]))

    @jsii.member(jsii_name="fromEcr")
    @builtins.classmethod
    def from_ecr(
        cls,
        *,
        repository: "_aws_cdk_aws_ecr_ceddda9d.IRepository",
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[builtins.str] = None,
        tag_or_digest: typing.Optional[builtins.str] = None,
    ) -> "EcrSource":
        '''(experimental) Source from the ECR repository.

        :param repository: (experimental) Represents the ECR repository.
        :param image_configuration: (experimental) The image configuration for the image from ECR. Default: - no image configuration will be passed. The default ``port`` will be 8080.
        :param tag: (deprecated) Image tag. Default: - 'latest'
        :param tag_or_digest: (experimental) Image tag or digest (digests must start with ``sha256:``). Default: - 'latest'

        :stability: experimental
        '''
        props = EcrProps(
            repository=repository,
            image_configuration=image_configuration,
            tag=tag,
            tag_or_digest=tag_or_digest,
        )

        return typing.cast("EcrSource", jsii.sinvoke(cls, "fromEcr", [props]))

    @jsii.member(jsii_name="fromEcrPublic")
    @builtins.classmethod
    def from_ecr_public(
        cls,
        *,
        image_identifier: builtins.str,
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "EcrPublicSource":
        '''(experimental) Source from the ECR Public repository.

        :param image_identifier: (experimental) The ECR Public image URI.
        :param image_configuration: (experimental) The image configuration for the image from ECR Public. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        '''
        props = EcrPublicProps(
            image_identifier=image_identifier, image_configuration=image_configuration
        )

        return typing.cast("EcrPublicSource", jsii.sinvoke(cls, "fromEcrPublic", [props]))

    @jsii.member(jsii_name="fromGitHub")
    @builtins.classmethod
    def from_git_hub(
        cls,
        *,
        configuration_source: "ConfigurationSourceType",
        connection: "GitHubConnection",
        repository_url: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        code_configuration_values: typing.Optional[typing.Union["CodeConfigurationValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "GithubSource":
        '''(experimental) Source from the GitHub repository.

        :param configuration_source: (experimental) The source of the App Runner configuration.
        :param connection: (experimental) ARN of the connection to Github. Only required for Github source.
        :param repository_url: (experimental) The location of the repository that contains the source code.
        :param branch: (experimental) The branch name that represents a specific version for the repository. Default: main
        :param code_configuration_values: (experimental) The code configuration values. Will be ignored if configurationSource is ``REPOSITORY``. Default: - no values will be passed. The ``apprunner.yaml`` from the github reopsitory will be used instead.

        :stability: experimental
        '''
        props = GithubRepositoryProps(
            configuration_source=configuration_source,
            connection=connection,
            repository_url=repository_url,
            branch=branch,
            code_configuration_values=code_configuration_values,
        )

        return typing.cast("GithubSource", jsii.sinvoke(cls, "fromGitHub", [props]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: "_constructs_77d1e7e8.Construct") -> "SourceConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param scope: -

        :stability: experimental
        '''
        ...


class _SourceProxy(Source):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: "_constructs_77d1e7e8.Construct") -> "SourceConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d725d56b2be3dba3a270f32f351b1b275b1b9c11bbcb6a012cc4a5f897ca1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("SourceConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Source).__jsii_proxy_class__ = lambda : _SourceProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.SourceCodeVersion",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SourceCodeVersion:
    def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
        '''(experimental) Identifies a version of code that AWS App Runner refers to within a source code repository.

        :param type: (experimental) The type of version identifier.
        :param value: (experimental) A source code version.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apprunner-service-sourcecodeversion.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            
            source_code_version = apprunner_alpha.SourceCodeVersion(
                type="type",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949d9e931cb062829d4a475b7bd2b7486cdb86b88c3d21205da596876e5e1894)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) The type of version identifier.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) A source code version.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceCodeVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.SourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "code_repository": "codeRepository",
        "ecr_repository": "ecrRepository",
        "image_repository": "imageRepository",
    },
)
class SourceConfig:
    def __init__(
        self,
        *,
        code_repository: typing.Optional[typing.Union["CodeRepositoryProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ecr_repository: typing.Optional["_aws_cdk_aws_ecr_ceddda9d.IRepository"] = None,
        image_repository: typing.Optional[typing.Union["ImageRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Result of binding ``Source`` into a ``Service``.

        :param code_repository: (experimental) The code repository configuration (mutually exclusive with ``imageRepository``). Default: - no code repository.
        :param ecr_repository: (experimental) The ECR repository (required to grant the pull privileges for the iam role). Default: - no ECR repository.
        :param image_repository: (experimental) The image repository configuration (mutually exclusive with ``codeRepository``). Default: - no image repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            from aws_cdk import aws_ecr as ecr
            
            # git_hub_connection: apprunner_alpha.GitHubConnection
            # repository: ecr.Repository
            # runtime: apprunner_alpha.Runtime
            # secret: apprunner_alpha.Secret
            
            source_config = apprunner_alpha.SourceConfig(
                code_repository=apprunner_alpha.CodeRepositoryProps(
                    code_configuration=apprunner_alpha.CodeConfiguration(
                        configuration_source=apprunner_alpha.ConfigurationSourceType.REPOSITORY,
            
                        # the properties below are optional
                        configuration_values=apprunner_alpha.CodeConfigurationValues(
                            runtime=runtime,
            
                            # the properties below are optional
                            build_command="buildCommand",
                            environment={
                                "environment_key": "environment"
                            },
                            environment_secrets={
                                "environment_secrets_key": secret
                            },
                            environment_variables={
                                "environment_variables_key": "environmentVariables"
                            },
                            port="port",
                            start_command="startCommand"
                        )
                    ),
                    connection=git_hub_connection,
                    repository_url="repositoryUrl",
                    source_code_version=apprunner_alpha.SourceCodeVersion(
                        type="type",
                        value="value"
                    )
                ),
                ecr_repository=repository,
                image_repository=apprunner_alpha.ImageRepository(
                    image_identifier="imageIdentifier",
                    image_repository_type=apprunner_alpha.ImageRepositoryType.ECR_PUBLIC,
            
                    # the properties below are optional
                    image_configuration=apprunner_alpha.ImageConfiguration(
                        environment={
                            "environment_key": "environment"
                        },
                        environment_secrets={
                            "environment_secrets_key": secret
                        },
                        environment_variables={
                            "environment_variables_key": "environmentVariables"
                        },
                        port=123,
                        start_command="startCommand"
                    )
                )
            )
        '''
        if isinstance(code_repository, dict):
            code_repository = CodeRepositoryProps(**code_repository)
        if isinstance(image_repository, dict):
            image_repository = ImageRepository(**image_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8ae249276fa295c9d7707d2b3ac313afc8daaaabc6dd3c9700bece30447312)
            check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
            check_type(argname="argument ecr_repository", value=ecr_repository, expected_type=type_hints["ecr_repository"])
            check_type(argname="argument image_repository", value=image_repository, expected_type=type_hints["image_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code_repository is not None:
            self._values["code_repository"] = code_repository
        if ecr_repository is not None:
            self._values["ecr_repository"] = ecr_repository
        if image_repository is not None:
            self._values["image_repository"] = image_repository

    @builtins.property
    def code_repository(self) -> typing.Optional["CodeRepositoryProps"]:
        '''(experimental) The code repository configuration (mutually exclusive  with ``imageRepository``).

        :default: - no code repository.

        :stability: experimental
        '''
        result = self._values.get("code_repository")
        return typing.cast(typing.Optional["CodeRepositoryProps"], result)

    @builtins.property
    def ecr_repository(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ecr_ceddda9d.IRepository"]:
        '''(experimental) The ECR repository (required to grant the pull privileges for the iam role).

        :default: - no ECR repository.

        :stability: experimental
        '''
        result = self._values.get("ecr_repository")
        return typing.cast(typing.Optional["_aws_cdk_aws_ecr_ceddda9d.IRepository"], result)

    @builtins.property
    def image_repository(self) -> typing.Optional["ImageRepository"]:
        '''(experimental) The image repository configuration (mutually exclusive  with ``codeRepository``).

        :default: - no image repository.

        :stability: experimental
        '''
        result = self._values.get("image_repository")
        return typing.cast(typing.Optional["ImageRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.TcpHealthCheckOptions",
    jsii_struct_bases=[],
    name_mapping={
        "healthy_threshold": "healthyThreshold",
        "interval": "interval",
        "timeout": "timeout",
        "unhealthy_threshold": "unhealthyThreshold",
    },
)
class TcpHealthCheckOptions:
    def __init__(
        self,
        *,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties used to define TCP Based healthchecks.

        :param healthy_threshold: (experimental) The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Default: 1
        :param interval: (experimental) The time interval, in seconds, between health checks. Default: Duration.seconds(5)
        :param timeout: (experimental) The time, in seconds, to wait for a health check response before deciding it failed. Default: Duration.seconds(2)
        :param unhealthy_threshold: (experimental) The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Default: 5

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            import aws_cdk as cdk
            
            tcp_health_check_options = apprunner_alpha.TcpHealthCheckOptions(
                healthy_threshold=123,
                interval=cdk.Duration.minutes(30),
                timeout=cdk.Duration.minutes(30),
                unhealthy_threshold=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac3cebf8ddb2593557fb2d26011f693f14d4099c4a43de1369aa1e30d559f03)
            check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if healthy_threshold is not None:
            self._values["healthy_threshold"] = healthy_threshold
        if interval is not None:
            self._values["interval"] = interval
        if timeout is not None:
            self._values["timeout"] = timeout
        if unhealthy_threshold is not None:
            self._values["unhealthy_threshold"] = unhealthy_threshold

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of consecutive checks that must succeed before App Runner decides that the service is healthy.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("healthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The time interval, in seconds, between health checks.

        :default: Duration.seconds(5)

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The time, in seconds, to wait for a health check response before deciding it failed.

        :default: Duration.seconds(2)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of consecutive checks that must fail before App Runner decides that the service is unhealthy.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("unhealthy_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TcpHealthCheckOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apprunner-alpha.TraceConfigurationVendor")
class TraceConfigurationVendor(enum.Enum):
    '''(experimental) The implementation provider chosen for tracing App Runner services.

    :see: https://docs.aws.amazon.com/apprunner/latest/dg/monitor.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        observability_configuration = apprunner.ObservabilityConfiguration(self, "ObservabilityConfiguration",
            observability_configuration_name="MyObservabilityConfiguration",
            trace_configuration_vendor=apprunner.TraceConfigurationVendor.AWSXRAY
        )
        
        apprunner.Service(self, "DemoService",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            ),
            observability_configuration=observability_configuration
        )
    '''

    AWSXRAY = "AWSXRAY"
    '''(experimental) Tracing (X-Ray).

    :stability: experimental
    '''


@jsii.implements(IVpcConnector)
class VpcConnector(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.VpcConnector",
):
    '''(experimental) The App Runner VPC Connector.

    :stability: experimental
    :resource: AWS::AppRunner::VpcConnector
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ec2 as ec2
        
        
        vpc = ec2.Vpc(self, "Vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16")
        )
        
        vpc_connector = apprunner.VpcConnector(self, "VpcConnector",
            vpc=vpc,
            vpc_subnets=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC),
            vpc_connector_name="MyVpcConnector"
        )
        
        apprunner.Service(self, "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            ),
            vpc_connector=vpc_connector
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        vpc_connector_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) The VPC for the VPC Connector.
        :param security_groups: (experimental) A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets. Default: - a new security group will be created in the specified VPC
        :param vpc_connector_name: (experimental) The name for the VpcConnector. Default: - a name generated by CloudFormation
        :param vpc_subnets: (experimental) Where to place the VPC Connector within the VPC. Default: - Private subnets.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c2727e7b20522fb91a3f09b12d7ff62896b2b6d9d43a47521aac4b5a1f95b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcConnectorProps(
            vpc=vpc,
            security_groups=security_groups,
            vpc_connector_name=vpc_connector_name,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromVpcConnectorAttributes")
    @builtins.classmethod
    def from_vpc_connector_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        security_groups: typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"],
        vpc_connector_arn: builtins.str,
        vpc_connector_name: builtins.str,
        vpc_connector_revision: jsii.Number,
    ) -> "IVpcConnector":
        '''(experimental) Import from VPC connector attributes.

        :param scope: -
        :param id: -
        :param security_groups: (experimental) The security groups associated with the VPC connector.
        :param vpc_connector_arn: (experimental) The ARN of the VPC connector.
        :param vpc_connector_name: (experimental) The name of the VPC connector.
        :param vpc_connector_revision: (experimental) The revision of the VPC connector.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7694a840b363f1de81784418c84e977ddf3407154c0520684431271bfa580005)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = VpcConnectorAttributes(
            security_groups=security_groups,
            vpc_connector_arn=vpc_connector_arn,
            vpc_connector_name=vpc_connector_name,
            vpc_connector_revision=vpc_connector_revision,
        )

        return typing.cast("IVpcConnector", jsii.sinvoke(cls, "fromVpcConnectorAttributes", [scope, id, attrs]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) Allows specifying security group connections for the VPC connector.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorArn")
    def vpc_connector_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorArn"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorName")
    def vpc_connector_name(self) -> builtins.str:
        '''(experimental) The name of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorName"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorRevision")
    def vpc_connector_revision(self) -> jsii.Number:
        '''(experimental) The revision of the VPC connector.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "vpcConnectorRevision"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.VpcConnectorAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "security_groups": "securityGroups",
        "vpc_connector_arn": "vpcConnectorArn",
        "vpc_connector_name": "vpcConnectorName",
        "vpc_connector_revision": "vpcConnectorRevision",
    },
)
class VpcConnectorAttributes:
    def __init__(
        self,
        *,
        security_groups: typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"],
        vpc_connector_arn: builtins.str,
        vpc_connector_name: builtins.str,
        vpc_connector_revision: jsii.Number,
    ) -> None:
        '''(experimental) Attributes for the App Runner VPC Connector.

        :param security_groups: (experimental) The security groups associated with the VPC connector.
        :param vpc_connector_arn: (experimental) The ARN of the VPC connector.
        :param vpc_connector_name: (experimental) The name of the VPC connector.
        :param vpc_connector_revision: (experimental) The revision of the VPC connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # security_group: ec2.SecurityGroup
            
            vpc_connector_attributes = apprunner_alpha.VpcConnectorAttributes(
                security_groups=[security_group],
                vpc_connector_arn="vpcConnectorArn",
                vpc_connector_name="vpcConnectorName",
                vpc_connector_revision=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__558ce3e1e73be190b0f0325aa59459ce6505f908a7ee62c96a492894ec1d92ff)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc_connector_arn", value=vpc_connector_arn, expected_type=type_hints["vpc_connector_arn"])
            check_type(argname="argument vpc_connector_name", value=vpc_connector_name, expected_type=type_hints["vpc_connector_name"])
            check_type(argname="argument vpc_connector_revision", value=vpc_connector_revision, expected_type=type_hints["vpc_connector_revision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_groups": security_groups,
            "vpc_connector_arn": vpc_connector_arn,
            "vpc_connector_name": vpc_connector_name,
            "vpc_connector_revision": vpc_connector_revision,
        }

    @builtins.property
    def security_groups(
        self,
    ) -> typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(experimental) The security groups associated with the VPC connector.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def vpc_connector_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC connector.

        :stability: experimental
        '''
        result = self._values.get("vpc_connector_arn")
        assert result is not None, "Required property 'vpc_connector_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_connector_name(self) -> builtins.str:
        '''(experimental) The name of the VPC connector.

        :stability: experimental
        '''
        result = self._values.get("vpc_connector_name")
        assert result is not None, "Required property 'vpc_connector_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_connector_revision(self) -> jsii.Number:
        '''(experimental) The revision of the VPC connector.

        :stability: experimental
        '''
        result = self._values.get("vpc_connector_revision")
        assert result is not None, "Required property 'vpc_connector_revision' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcConnectorAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.VpcConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "security_groups": "securityGroups",
        "vpc_connector_name": "vpcConnectorName",
        "vpc_subnets": "vpcSubnets",
    },
)
class VpcConnectorProps:
    def __init__(
        self,
        *,
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        vpc_connector_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties of the AppRunner VPC Connector.

        :param vpc: (experimental) The VPC for the VPC Connector.
        :param security_groups: (experimental) A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets. Default: - a new security group will be created in the specified VPC
        :param vpc_connector_name: (experimental) The name for the VpcConnector. Default: - a name generated by CloudFormation
        :param vpc_subnets: (experimental) Where to place the VPC Connector within the VPC. Default: - Private subnets.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ec2 as ec2
            
            
            vpc = ec2.Vpc(self, "Vpc",
                ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16")
            )
            
            vpc_connector = apprunner.VpcConnector(self, "VpcConnector",
                vpc=vpc,
                vpc_subnets=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC),
                vpc_connector_name="MyVpcConnector"
            )
            
            apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(port=8000),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                ),
                vpc_connector=vpc_connector
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71fa89821720bc591fe5e6fb3e6314cb7258e32cc0a905888155847181cce9c0)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc_connector_name", value=vpc_connector_name, expected_type=type_hints["vpc_connector_name"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc_connector_name is not None:
            self._values["vpc_connector_name"] = vpc_connector_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> "_aws_cdk_aws_ec2_ceddda9d.IVpc":
        '''(experimental) The VPC for the VPC Connector.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.IVpc", result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) A list of IDs of security groups that App Runner should use for access to AWS resources under the specified subnets.

        :default: - a new security group will be created in the specified VPC

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def vpc_connector_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the VpcConnector.

        :default: - a name generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("vpc_connector_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_subnets(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Where to place the VPC Connector within the VPC.

        :default: - Private subnets.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVpcIngressConnection)
class VpcIngressConnection(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.VpcIngressConnection",
):
    '''(experimental) The App Runner VPC Ingress Connection.

    :stability: experimental
    :resource: AWS::AppRunner::VpcIngressConnection
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ec2 as ec2
        
        # vpc: ec2.Vpc
        
        
        interface_vpc_endpoint = ec2.InterfaceVpcEndpoint(self, "MyVpcEndpoint",
            vpc=vpc,
            service=ec2.InterfaceVpcEndpointAwsService.APP_RUNNER_REQUESTS,
            private_dns_enabled=False
        )
        
        service = apprunner.Service(self, "Service",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(
                    port=8000
                ),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            ),
            is_publicly_accessible=False
        )
        
        apprunner.VpcIngressConnection(self, "VpcIngressConnection",
            vpc=vpc,
            interface_vpc_endpoint=interface_vpc_endpoint,
            service=service
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        interface_vpc_endpoint: "_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint",
        service: "IService",
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param interface_vpc_endpoint: (experimental) The VPC Interface Endpoint for the VPC Ingress Connection.
        :param service: (experimental) The service to connect.
        :param vpc: (experimental) The VPC for the VPC Ingress Connection.
        :param vpc_ingress_connection_name: (experimental) The name for the VPC Ingress Connection. Default: - a name generated by CloudFormation

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2444dea5f1a77b286d4e07ad1d439ff2d134a07a51e48680c7bd7e52bc6f4fd9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcIngressConnectionProps(
            interface_vpc_endpoint=interface_vpc_endpoint,
            service=service,
            vpc=vpc,
            vpc_ingress_connection_name=vpc_ingress_connection_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        vpc_ingress_connection_arn: builtins.str,
    ) -> "IVpcIngressConnection":
        '''(experimental) Imports an App Runner VPC Ingress Connection from its ARN.

        :param scope: -
        :param id: -
        :param vpc_ingress_connection_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be112ae1759d62dac20b14d707319781c955b5b9f7a881738d6dc6a5cdb0d90a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument vpc_ingress_connection_arn", value=vpc_ingress_connection_arn, expected_type=type_hints["vpc_ingress_connection_arn"])
        return typing.cast("IVpcIngressConnection", jsii.sinvoke(cls, "fromArn", [scope, id, vpc_ingress_connection_arn]))

    @jsii.member(jsii_name="fromVpcIngressConnectionAttributes")
    @builtins.classmethod
    def from_vpc_ingress_connection_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        domain_name: builtins.str,
        status: builtins.str,
        vpc_ingress_connection_arn: builtins.str,
        vpc_ingress_connection_name: builtins.str,
    ) -> "IVpcIngressConnection":
        '''(experimental) Import from VPC Ingress Connection from attributes.

        :param scope: -
        :param id: -
        :param domain_name: (experimental) The domain name associated with the VPC Ingress Connection resource.
        :param status: (experimental) The current status of the VPC Ingress Connection.
        :param vpc_ingress_connection_arn: (experimental) The Amazon Resource Name (ARN) of the VPC Ingress Connection.
        :param vpc_ingress_connection_name: (experimental) The name of the VPC Ingress Connection.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f765077463a26c42e05e524008ca4c66c0c4a74dd9f8b30786b632d2b00990f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = VpcIngressConnectionAttributes(
            domain_name=domain_name,
            status=status,
            vpc_ingress_connection_arn=vpc_ingress_connection_arn,
            vpc_ingress_connection_name=vpc_ingress_connection_name,
        )

        return typing.cast("IVpcIngressConnection", jsii.sinvoke(cls, "fromVpcIngressConnectionAttributes", [scope, id, attrs]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) The domain name associated with the VPC Ingress Connection resource.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        '''(experimental) The current status of the VPC Ingress Connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="vpcIngressConnectionArn")
    def vpc_ingress_connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the VPC Ingress Connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcIngressConnectionArn"))

    @builtins.property
    @jsii.member(jsii_name="vpcIngressConnectionName")
    def vpc_ingress_connection_name(self) -> builtins.str:
        '''(experimental) The name of the VPC Ingress Connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcIngressConnectionName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.VpcIngressConnectionAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "status": "status",
        "vpc_ingress_connection_arn": "vpcIngressConnectionArn",
        "vpc_ingress_connection_name": "vpcIngressConnectionName",
    },
)
class VpcIngressConnectionAttributes:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        status: builtins.str,
        vpc_ingress_connection_arn: builtins.str,
        vpc_ingress_connection_name: builtins.str,
    ) -> None:
        '''(experimental) Attributes for the App Runner VPC Ingress Connection.

        :param domain_name: (experimental) The domain name associated with the VPC Ingress Connection resource.
        :param status: (experimental) The current status of the VPC Ingress Connection.
        :param vpc_ingress_connection_arn: (experimental) The Amazon Resource Name (ARN) of the VPC Ingress Connection.
        :param vpc_ingress_connection_name: (experimental) The name of the VPC Ingress Connection.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apprunner_alpha as apprunner_alpha
            
            vpc_ingress_connection_attributes = apprunner_alpha.VpcIngressConnectionAttributes(
                domain_name="domainName",
                status="status",
                vpc_ingress_connection_arn="vpcIngressConnectionArn",
                vpc_ingress_connection_name="vpcIngressConnectionName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147d6424d71cd2ebc7ba8c76443f7075084f8f726817a40aae39979dcf9eab5d)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument vpc_ingress_connection_arn", value=vpc_ingress_connection_arn, expected_type=type_hints["vpc_ingress_connection_arn"])
            check_type(argname="argument vpc_ingress_connection_name", value=vpc_ingress_connection_name, expected_type=type_hints["vpc_ingress_connection_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "status": status,
            "vpc_ingress_connection_arn": vpc_ingress_connection_arn,
            "vpc_ingress_connection_name": vpc_ingress_connection_name,
        }

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''(experimental) The domain name associated with the VPC Ingress Connection resource.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''(experimental) The current status of the VPC Ingress Connection.

        :stability: experimental
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_ingress_connection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the VPC Ingress Connection.

        :stability: experimental
        '''
        result = self._values.get("vpc_ingress_connection_arn")
        assert result is not None, "Required property 'vpc_ingress_connection_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_ingress_connection_name(self) -> builtins.str:
        '''(experimental) The name of the VPC Ingress Connection.

        :stability: experimental
        '''
        result = self._values.get("vpc_ingress_connection_name")
        assert result is not None, "Required property 'vpc_ingress_connection_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcIngressConnectionAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apprunner-alpha.VpcIngressConnectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "interface_vpc_endpoint": "interfaceVpcEndpoint",
        "service": "service",
        "vpc": "vpc",
        "vpc_ingress_connection_name": "vpcIngressConnectionName",
    },
)
class VpcIngressConnectionProps:
    def __init__(
        self,
        *,
        interface_vpc_endpoint: "_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint",
        service: "IService",
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties of the AppRunner VPC Ingress Connection.

        :param interface_vpc_endpoint: (experimental) The VPC Interface Endpoint for the VPC Ingress Connection.
        :param service: (experimental) The service to connect.
        :param vpc: (experimental) The VPC for the VPC Ingress Connection.
        :param vpc_ingress_connection_name: (experimental) The name for the VPC Ingress Connection. Default: - a name generated by CloudFormation

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ec2 as ec2
            
            # vpc: ec2.Vpc
            
            
            interface_vpc_endpoint = ec2.InterfaceVpcEndpoint(self, "MyVpcEndpoint",
                vpc=vpc,
                service=ec2.InterfaceVpcEndpointAwsService.APP_RUNNER_REQUESTS,
                private_dns_enabled=False
            )
            
            service = apprunner.Service(self, "Service",
                source=apprunner.Source.from_ecr_public(
                    image_configuration=apprunner.ImageConfiguration(
                        port=8000
                    ),
                    image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
                ),
                is_publicly_accessible=False
            )
            
            apprunner.VpcIngressConnection(self, "VpcIngressConnection",
                vpc=vpc,
                interface_vpc_endpoint=interface_vpc_endpoint,
                service=service
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2228ce28d31ba34a5673b0601bb2704194861b2eb9da3c03a7d3933a1018f9b2)
            check_type(argname="argument interface_vpc_endpoint", value=interface_vpc_endpoint, expected_type=type_hints["interface_vpc_endpoint"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_ingress_connection_name", value=vpc_ingress_connection_name, expected_type=type_hints["vpc_ingress_connection_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface_vpc_endpoint": interface_vpc_endpoint,
            "service": service,
            "vpc": vpc,
        }
        if vpc_ingress_connection_name is not None:
            self._values["vpc_ingress_connection_name"] = vpc_ingress_connection_name

    @builtins.property
    def interface_vpc_endpoint(
        self,
    ) -> "_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint":
        '''(experimental) The VPC Interface Endpoint for the VPC Ingress Connection.

        :stability: experimental
        '''
        result = self._values.get("interface_vpc_endpoint")
        assert result is not None, "Required property 'interface_vpc_endpoint' is missing"
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint", result)

    @builtins.property
    def service(self) -> "IService":
        '''(experimental) The service to connect.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast("IService", result)

    @builtins.property
    def vpc(self) -> "_aws_cdk_aws_ec2_ceddda9d.IVpc":
        '''(experimental) The VPC for the VPC Ingress Connection.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.IVpc", result)

    @builtins.property
    def vpc_ingress_connection_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the VPC Ingress Connection.

        :default: - a name generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("vpc_ingress_connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcIngressConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssetSource(
    Source,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.AssetSource",
):
    '''(experimental) Represents the source from local assets.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner_alpha as apprunner_alpha
        from aws_cdk import aws_ecr_assets as ecr_assets
        
        # docker_image_asset: ecr_assets.DockerImageAsset
        # secret: apprunner_alpha.Secret
        
        asset_source = apprunner_alpha.AssetSource(
            asset=docker_image_asset,
        
            # the properties below are optional
            image_configuration=apprunner_alpha.ImageConfiguration(
                environment={
                    "environment_key": "environment"
                },
                environment_secrets={
                    "environment_secrets_key": secret
                },
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                port=123,
                start_command="startCommand"
            )
        )
    '''

    def __init__(
        self,
        *,
        asset: "_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset",
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param asset: (experimental) Represents the docker image asset.
        :param image_configuration: (experimental) The image configuration for the image built from the asset. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        '''
        props = AssetProps(asset=asset, image_configuration=image_configuration)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: "_constructs_77d1e7e8.Construct") -> "SourceConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816e091a385df2e47be65a182df3765591f8f56e636bfd16e69e0cdbe27ca53a)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast("SourceConfig", jsii.invoke(self, "bind", [_scope]))


@jsii.implements(IAutoScalingConfiguration)
class AutoScalingConfiguration(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.AutoScalingConfiguration",
):
    '''(experimental) The App Runner Auto Scaling Configuration.

    :stability: experimental
    :resource: AWS::AppRunner::AutoScalingConfiguration
    :exampleMetadata: infused

    Example::

        auto_scaling_configuration = apprunner.AutoScalingConfiguration(self, "AutoScalingConfiguration",
            auto_scaling_configuration_name="MyAutoScalingConfiguration",
            max_concurrency=150,
            max_size=20,
            min_size=5
        )
        
        apprunner.Service(self, "DemoService",
            source=apprunner.Source.from_ecr_public(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                image_identifier="public.ecr.aws/aws-containers/hello-app-runner:latest"
            ),
            auto_scaling_configuration=auto_scaling_configuration
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        auto_scaling_configuration_name: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[jsii.Number] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param auto_scaling_configuration_name: (experimental) The name for the Auto Scaling Configuration. Default: - a name generated by CloudFormation
        :param max_concurrency: (experimental) The maximum number of concurrent requests that an instance processes. If the number of concurrent requests exceeds this limit, App Runner scales the service up. Must be between 1 and 200. Default: 100
        :param max_size: (experimental) The maximum number of instances that a service scales up to. At most maxSize instances actively serve traffic for your service. Must be between 1 and 25. Default: 25
        :param min_size: (experimental) The minimum number of instances that App Runner provisions for a service. The service always has at least minSize provisioned instances. Must be between 1 and 25. Default: 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef06c2e17ff3e572a7af9478d4e09b649f3f54aeb6c08cf6f77d83c2006982af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AutoScalingConfigurationProps(
            auto_scaling_configuration_name=auto_scaling_configuration_name,
            max_concurrency=max_concurrency,
            max_size=max_size,
            min_size=min_size,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        auto_scaling_configuration_arn: builtins.str,
    ) -> "IAutoScalingConfiguration":
        '''(experimental) Imports an App Runner Auto Scaling Configuration from its ARN.

        :param scope: -
        :param id: -
        :param auto_scaling_configuration_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13142842dfceb79198f01381a50a3e5d75bfaa10402849b027a9bf039ef7122b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument auto_scaling_configuration_arn", value=auto_scaling_configuration_arn, expected_type=type_hints["auto_scaling_configuration_arn"])
        return typing.cast("IAutoScalingConfiguration", jsii.sinvoke(cls, "fromArn", [scope, id, auto_scaling_configuration_arn]))

    @jsii.member(jsii_name="fromAutoScalingConfigurationAttributes")
    @builtins.classmethod
    def from_auto_scaling_configuration_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        auto_scaling_configuration_name: builtins.str,
        auto_scaling_configuration_revision: jsii.Number,
    ) -> "IAutoScalingConfiguration":
        '''(experimental) Imports an App Runner Auto Scaling Configuration from attributes.

        :param scope: -
        :param id: -
        :param auto_scaling_configuration_name: (experimental) The name of the Auto Scaling Configuration.
        :param auto_scaling_configuration_revision: (experimental) The revision of the Auto Scaling Configuration.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ba14de71b26aa8d2d8dacabb37288b217fab1af135a958edf55844f3f09bdb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AutoScalingConfigurationAttributes(
            auto_scaling_configuration_name=auto_scaling_configuration_name,
            auto_scaling_configuration_revision=auto_scaling_configuration_revision,
        )

        return typing.cast("IAutoScalingConfiguration", jsii.sinvoke(cls, "fromAutoScalingConfigurationAttributes", [scope, id, attrs]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationArn")
    def auto_scaling_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "autoScalingConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationName")
    def auto_scaling_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "autoScalingConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingConfigurationRevision")
    def auto_scaling_configuration_revision(self) -> jsii.Number:
        '''(experimental) The revision of the Auto Scaling Configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "autoScalingConfigurationRevision"))


class EcrPublicSource(
    Source,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.EcrPublicSource",
):
    '''(experimental) Represents the service source from ECR Public.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner_alpha as apprunner_alpha
        
        # secret: apprunner_alpha.Secret
        
        ecr_public_source = apprunner_alpha.EcrPublicSource(
            image_identifier="imageIdentifier",
        
            # the properties below are optional
            image_configuration=apprunner_alpha.ImageConfiguration(
                environment={
                    "environment_key": "environment"
                },
                environment_secrets={
                    "environment_secrets_key": secret
                },
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                port=123,
                start_command="startCommand"
            )
        )
    '''

    def __init__(
        self,
        *,
        image_identifier: builtins.str,
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_identifier: (experimental) The ECR Public image URI.
        :param image_configuration: (experimental) The image configuration for the image from ECR Public. Default: - no image configuration will be passed. The default ``port`` will be 8080.

        :stability: experimental
        '''
        props = EcrPublicProps(
            image_identifier=image_identifier, image_configuration=image_configuration
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: "_constructs_77d1e7e8.Construct") -> "SourceConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25ff2d831ac9b326ad13669ae9451f6d2db76f9975bc6afd9937cdff1c2e1c9)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast("SourceConfig", jsii.invoke(self, "bind", [_scope]))


class EcrSource(
    Source,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.EcrSource",
):
    '''(experimental) Represents the service source from ECR.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner_alpha as apprunner_alpha
        from aws_cdk import aws_ecr as ecr
        
        # repository: ecr.Repository
        # secret: apprunner_alpha.Secret
        
        ecr_source = apprunner_alpha.EcrSource(
            repository=repository,
        
            # the properties below are optional
            image_configuration=apprunner_alpha.ImageConfiguration(
                environment={
                    "environment_key": "environment"
                },
                environment_secrets={
                    "environment_secrets_key": secret
                },
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                port=123,
                start_command="startCommand"
            ),
            tag="tag",
            tag_or_digest="tagOrDigest"
        )
    '''

    def __init__(
        self,
        *,
        repository: "_aws_cdk_aws_ecr_ceddda9d.IRepository",
        image_configuration: typing.Optional[typing.Union["ImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[builtins.str] = None,
        tag_or_digest: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: (experimental) Represents the ECR repository.
        :param image_configuration: (experimental) The image configuration for the image from ECR. Default: - no image configuration will be passed. The default ``port`` will be 8080.
        :param tag: (deprecated) Image tag. Default: - 'latest'
        :param tag_or_digest: (experimental) Image tag or digest (digests must start with ``sha256:``). Default: - 'latest'

        :stability: experimental
        '''
        props = EcrProps(
            repository=repository,
            image_configuration=image_configuration,
            tag=tag,
            tag_or_digest=tag_or_digest,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: "_constructs_77d1e7e8.Construct") -> "SourceConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd17a6fe4667274b7ce2eab975f27b690350fdd5950e60470cc0c6574a115c1)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast("SourceConfig", jsii.invoke(self, "bind", [_scope]))


class GithubSource(
    Source,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apprunner-alpha.GithubSource",
):
    '''(experimental) Represents the service source from a Github repository.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apprunner_alpha as apprunner_alpha
        
        # git_hub_connection: apprunner_alpha.GitHubConnection
        # runtime: apprunner_alpha.Runtime
        # secret: apprunner_alpha.Secret
        
        github_source = apprunner_alpha.GithubSource(
            configuration_source=apprunner_alpha.ConfigurationSourceType.REPOSITORY,
            connection=git_hub_connection,
            repository_url="repositoryUrl",
        
            # the properties below are optional
            branch="branch",
            code_configuration_values=apprunner_alpha.CodeConfigurationValues(
                runtime=runtime,
        
                # the properties below are optional
                build_command="buildCommand",
                environment={
                    "environment_key": "environment"
                },
                environment_secrets={
                    "environment_secrets_key": secret
                },
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                port="port",
                start_command="startCommand"
            )
        )
    '''

    def __init__(
        self,
        *,
        configuration_source: "ConfigurationSourceType",
        connection: "GitHubConnection",
        repository_url: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        code_configuration_values: typing.Optional[typing.Union["CodeConfigurationValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configuration_source: (experimental) The source of the App Runner configuration.
        :param connection: (experimental) ARN of the connection to Github. Only required for Github source.
        :param repository_url: (experimental) The location of the repository that contains the source code.
        :param branch: (experimental) The branch name that represents a specific version for the repository. Default: main
        :param code_configuration_values: (experimental) The code configuration values. Will be ignored if configurationSource is ``REPOSITORY``. Default: - no values will be passed. The ``apprunner.yaml`` from the github reopsitory will be used instead.

        :stability: experimental
        '''
        props = GithubRepositoryProps(
            configuration_source=configuration_source,
            connection=connection,
            repository_url=repository_url,
            branch=branch,
            code_configuration_values=code_configuration_values,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: "_constructs_77d1e7e8.Construct") -> "SourceConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8890dbdfbf2cbe4c8cbd67ceb346d6e7ced18852992bc4d4bbc40af88916d4b0)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast("SourceConfig", jsii.invoke(self, "bind", [_scope]))


__all__ = [
    "AssetProps",
    "AssetSource",
    "AutoScalingConfiguration",
    "AutoScalingConfigurationAttributes",
    "AutoScalingConfigurationProps",
    "CodeConfiguration",
    "CodeConfigurationValues",
    "CodeRepositoryProps",
    "ConfigurationSourceType",
    "Cpu",
    "EcrProps",
    "EcrPublicProps",
    "EcrPublicSource",
    "EcrSource",
    "GitHubConnection",
    "GithubRepositoryProps",
    "GithubSource",
    "HealthCheck",
    "HealthCheckProtocolType",
    "HttpHealthCheckOptions",
    "IAutoScalingConfiguration",
    "IObservabilityConfiguration",
    "IService",
    "IVpcConnector",
    "IVpcIngressConnection",
    "ImageConfiguration",
    "ImageRepository",
    "ImageRepositoryType",
    "IpAddressType",
    "Memory",
    "ObservabilityConfiguration",
    "ObservabilityConfigurationAttributes",
    "ObservabilityConfigurationProps",
    "Runtime",
    "Secret",
    "SecretVersionInfo",
    "Service",
    "ServiceAttributes",
    "ServiceProps",
    "Source",
    "SourceCodeVersion",
    "SourceConfig",
    "TcpHealthCheckOptions",
    "TraceConfigurationVendor",
    "VpcConnector",
    "VpcConnectorAttributes",
    "VpcConnectorProps",
    "VpcIngressConnection",
    "VpcIngressConnectionAttributes",
    "VpcIngressConnectionProps",
]

publication.publish()

def _typecheckingstub__e08a8fbd7cfe007fa7ce008c1d8a55a2e2ebe4d254c9dd541108007ec6a8e6e5(
    *,
    asset: _aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset,
    image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f04f1b647655a9262a279fbe04c1b04be071f7dcc95c2b4faec882a230929f6(
    *,
    auto_scaling_configuration_name: builtins.str,
    auto_scaling_configuration_revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d409b1d530a639b5498bf567d8dcb90e3d933f850862a29f70518344ec6b1623(
    *,
    auto_scaling_configuration_name: typing.Optional[builtins.str] = None,
    max_concurrency: typing.Optional[jsii.Number] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae937db922ae6dad5990a7f5c386f8b91b134eb32d1e222b6397b08cd185df6(
    *,
    configuration_source: ConfigurationSourceType,
    configuration_values: typing.Optional[typing.Union[CodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfca01cbfa9c6291b2ceb7b79d2e8973e68667f4752762fc65620ae5c1d16bec(
    *,
    runtime: Runtime,
    build_command: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    port: typing.Optional[builtins.str] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8f6208c6ccadbd7f2f6a081b0c3ce8ee7e55504225e9ba72fd0d33a99d04d6(
    *,
    code_configuration: typing.Union[CodeConfiguration, typing.Dict[builtins.str, typing.Any]],
    connection: GitHubConnection,
    repository_url: builtins.str,
    source_code_version: typing.Union[SourceCodeVersion, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb36987110835c7df289907b6abce68377a8816dcc626b59e4634b110b68502a(
    unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d314b79b8d81f041cdd01718f3ef34ccc715997cf7fd3d81583ef7cdd22d75a(
    *,
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tag: typing.Optional[builtins.str] = None,
    tag_or_digest: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c946837bfdb36bdd4b295396580cb8fb7d16dbdf8cd7e7d26f40af21c98350(
    *,
    image_identifier: builtins.str,
    image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa88c7a5842afea11022e7d7cb6979e91cfb24043dd76ce07670f71189675f3f(
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f2a8dc46245c67294c19ebb6e56670f52e1c8498f08a6f3cc64085d586c648(
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d401724ed1ffda098b7c914516349006ef7826c8ceec08ba31a7c624efd3db14(
    *,
    configuration_source: ConfigurationSourceType,
    connection: GitHubConnection,
    repository_url: builtins.str,
    branch: typing.Optional[builtins.str] = None,
    code_configuration_values: typing.Optional[typing.Union[CodeConfigurationValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29cfd6afd364301a292f444ae0cb2af3e2fbd32a8e5c375cbc091c6d48b6083(
    *,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    path: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada5ceaac12328ac3e20c585b8447f90f84c0d2bf9b8461f994b196a6f5ca778(
    *,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    port: typing.Optional[jsii.Number] = None,
    start_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5739f9e0d186c5ae07f20de42ed39073fd22f6a1e220dd2c9b94782477260351(
    *,
    image_identifier: builtins.str,
    image_repository_type: ImageRepositoryType,
    image_configuration: typing.Optional[typing.Union[ImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aef99b08abb67e03d37b29a11f144ec6ca20853863c7f628ad9b0aa4181206e(
    unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421591e7b88a9ca05adf379a20784325b1be3eedc888d670052b856051ee10aa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    trace_configuration_vendor: TraceConfigurationVendor,
    observability_configuration_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b8985e0f2351adfd5874d7295c72db8512a2ddf22cc04e25d61e3a0649da91(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    observability_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9c656cd02cc4dd8667796a9860a8e89b2774a2728bd9d9bdee1fe1c8222387(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    observability_configuration_name: builtins.str,
    observability_configuration_revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996b375337e44a1fc2e0188aa768043611d92db57b51134bfc70c46cd87178f3(
    *,
    observability_configuration_name: builtins.str,
    observability_configuration_revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b324b5f514dc536d9d0d42556461942a8bb167ffa704ba3b757ee33b93849384(
    *,
    trace_configuration_vendor: TraceConfigurationVendor,
    observability_configuration_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb5ee8b6854f81974bb8bee14dcd006f98f0b3c2cf8d852ea034c6fe09f2e35(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f059432ff1a488be31a6b1d8f1a5752dafa5774b88cec265c7bc1c9f73a4e5(
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b639ee831f5eec1269609ed8aaace2c8c854af8a0a99896bf57f1ec44feec01d(
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    version_info: typing.Union[SecretVersionInfo, typing.Dict[builtins.str, typing.Any]],
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cf075f1b7a42d19d2404c921c8ea9deeb7507e3c967f80806510dd249b0e77(
    parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd282bba973b7a15360293a7363341363c526b874ed3ef1f9c1b62187cd9f09(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb5825ef7d4a37f927b0ae1f338a89941dd65787b02e3e4604e036461d23cc0(
    *,
    version_id: typing.Optional[builtins.str] = None,
    version_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d7d688c20ccfdaf4ead5ff12fa6ddcb24fd014e98a55a23b275e5f19aba35f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source: Source,
    access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    auto_deployments_enabled: typing.Optional[builtins.bool] = None,
    auto_scaling_configuration: typing.Optional[IAutoScalingConfiguration] = None,
    cpu: typing.Optional[Cpu] = None,
    health_check: typing.Optional[HealthCheck] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ip_address_type: typing.Optional[IpAddressType] = None,
    is_publicly_accessible: typing.Optional[builtins.bool] = None,
    kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    memory: typing.Optional[Memory] = None,
    observability_configuration: typing.Optional[IObservabilityConfiguration] = None,
    service_name: typing.Optional[builtins.str] = None,
    vpc_connector: typing.Optional[IVpcConnector] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8409d8e0abf02901118bc4d7766649b9864e2eeb9bf9cb3aac48e20660a74c7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service_arn: builtins.str,
    service_name: builtins.str,
    service_status: builtins.str,
    service_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150c152e2ac6267c6d21bd0cbf987659618d73bdd8ab39737c8f485109edb498(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f84babe1afe98a87221e6e76763e715d187e385c835bebec2fa7128a092bd4(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc967eafc1f0b4b004e18edc573b5becb1d10a6ea57ccc980fa0b326fd15f4b1(
    name: builtins.str,
    secret: Secret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5351c83ee7c098c1c4aac40f6a190c1c06bbd214351029437128b80b6a431a49(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c46766384c012b61899cf246f3108c023b5f905a313bafaeafc7f4429fa6fb6(
    *,
    service_arn: builtins.str,
    service_name: builtins.str,
    service_status: builtins.str,
    service_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbb5d2c5a8f10a3d012f0035d55423352f4a7eff0eb19c057f0e1898a751cb6(
    *,
    source: Source,
    access_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    auto_deployments_enabled: typing.Optional[builtins.bool] = None,
    auto_scaling_configuration: typing.Optional[IAutoScalingConfiguration] = None,
    cpu: typing.Optional[Cpu] = None,
    health_check: typing.Optional[HealthCheck] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ip_address_type: typing.Optional[IpAddressType] = None,
    is_publicly_accessible: typing.Optional[builtins.bool] = None,
    kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    memory: typing.Optional[Memory] = None,
    observability_configuration: typing.Optional[IObservabilityConfiguration] = None,
    service_name: typing.Optional[builtins.str] = None,
    vpc_connector: typing.Optional[IVpcConnector] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d725d56b2be3dba3a270f32f351b1b275b1b9c11bbcb6a012cc4a5f897ca1f(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949d9e931cb062829d4a475b7bd2b7486cdb86b88c3d21205da596876e5e1894(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8ae249276fa295c9d7707d2b3ac313afc8daaaabc6dd3c9700bece30447312(
    *,
    code_repository: typing.Optional[typing.Union[CodeRepositoryProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
    image_repository: typing.Optional[typing.Union[ImageRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac3cebf8ddb2593557fb2d26011f693f14d4099c4a43de1369aa1e30d559f03(
    *,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c2727e7b20522fb91a3f09b12d7ff62896b2b6d9d43a47521aac4b5a1f95b2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    vpc_connector_name: typing.Optional[builtins.str] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7694a840b363f1de81784418c84e977ddf3407154c0520684431271bfa580005(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
    vpc_connector_arn: builtins.str,
    vpc_connector_name: builtins.str,
    vpc_connector_revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558ce3e1e73be190b0f0325aa59459ce6505f908a7ee62c96a492894ec1d92ff(
    *,
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
    vpc_connector_arn: builtins.str,
    vpc_connector_name: builtins.str,
    vpc_connector_revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71fa89821720bc591fe5e6fb3e6314cb7258e32cc0a905888155847181cce9c0(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    vpc_connector_name: typing.Optional[builtins.str] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2444dea5f1a77b286d4e07ad1d439ff2d134a07a51e48680c7bd7e52bc6f4fd9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    interface_vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
    service: IService,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be112ae1759d62dac20b14d707319781c955b5b9f7a881738d6dc6a5cdb0d90a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    vpc_ingress_connection_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f765077463a26c42e05e524008ca4c66c0c4a74dd9f8b30786b632d2b00990f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain_name: builtins.str,
    status: builtins.str,
    vpc_ingress_connection_arn: builtins.str,
    vpc_ingress_connection_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147d6424d71cd2ebc7ba8c76443f7075084f8f726817a40aae39979dcf9eab5d(
    *,
    domain_name: builtins.str,
    status: builtins.str,
    vpc_ingress_connection_arn: builtins.str,
    vpc_ingress_connection_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2228ce28d31ba34a5673b0601bb2704194861b2eb9da3c03a7d3933a1018f9b2(
    *,
    interface_vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
    service: IService,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_ingress_connection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816e091a385df2e47be65a182df3765591f8f56e636bfd16e69e0cdbe27ca53a(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef06c2e17ff3e572a7af9478d4e09b649f3f54aeb6c08cf6f77d83c2006982af(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    auto_scaling_configuration_name: typing.Optional[builtins.str] = None,
    max_concurrency: typing.Optional[jsii.Number] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13142842dfceb79198f01381a50a3e5d75bfaa10402849b027a9bf039ef7122b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    auto_scaling_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ba14de71b26aa8d2d8dacabb37288b217fab1af135a958edf55844f3f09bdb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    auto_scaling_configuration_name: builtins.str,
    auto_scaling_configuration_revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25ff2d831ac9b326ad13669ae9451f6d2db76f9975bc6afd9937cdff1c2e1c9(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd17a6fe4667274b7ce2eab975f27b690350fdd5950e60470cc0c6574a115c1(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8890dbdfbf2cbe4c8cbd67ceb346d6e7ced18852992bc4d4bbc40af88916d4b0(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IAutoScalingConfiguration, IObservabilityConfiguration, IService, IVpcConnector, IVpcIngressConnection]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
