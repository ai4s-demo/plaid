r'''
# AWS::DevOpsAgent Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_devopsagent as devopsagent
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DevOpsAgent construct libraries](https://constructs.dev/search?q=devopsagent)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DevOpsAgent resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DevOpsAgent.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DevOpsAgent](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DevOpsAgent.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_9df397a6,
    IInspectable as _IInspectable_c2943556,
    IResolvable as _IResolvable_da3f097b,
    TreeInspector as _TreeInspector_488e0dd5,
)
from ..interfaces.aws_devopsagent import (
    AgentSpaceReference as _AgentSpaceReference_4cf55ea9,
    AssociationReference as _AssociationReference_249ec236,
    IAgentSpaceRef as _IAgentSpaceRef_2ffb48ed,
    IAssociationRef as _IAssociationRef_ac0997e3,
)


@jsii.implements(_IInspectable_c2943556, _IAgentSpaceRef_2ffb48ed)
class CfnAgentSpace(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_devopsagent.CfnAgentSpace",
):
    '''The ``AWS::DevOpsAgent::AgentSpace`` resource specifies an Agent Space for the AWS DevOps Agent Service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-agentspace.html
    :cloudformationResource: AWS::DevOpsAgent::AgentSpace
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_devopsagent as devopsagent
        
        cfn_agent_space = devopsagent.CfnAgentSpace(self, "MyCfnAgentSpace",
            name="name",
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::DevOpsAgent::AgentSpace``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the Agent Space.
        :param description: The description of the Agent Space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3897cdc52c2bc2a74bdd32702e32905947b3c0fc36798edcdac7875cc9939456)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAgentSpaceProps(name=name, description=description)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForAgentSpace")
    @builtins.classmethod
    def arn_for_agent_space(cls, resource: "_IAgentSpaceRef_2ffb48ed") -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fd19a72161f0ef8cc6732b6e9205e1c9f41b50d57a659a84461dcdde223423)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForAgentSpace", [resource]))

    @jsii.member(jsii_name="isCfnAgentSpace")
    @builtins.classmethod
    def is_cfn_agent_space(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnAgentSpace.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b6182298920242aa320928b58b0b5bc6ee7fe37ab398df5dd8f138f81638f6)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnAgentSpace", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c3714a879ff931c53d9540f49cb04b7551032f6754505380b7064cbcb7719f)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca7931f7e8a8dc031f895c3bf121e4253f0443d5d02865c48e259d41303518b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="agentSpaceRef")
    def agent_space_ref(self) -> "_AgentSpaceReference_4cf55ea9":
        '''A reference to a AgentSpace resource.'''
        return typing.cast("_AgentSpaceReference_4cf55ea9", jsii.get(self, "agentSpaceRef"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentSpaceId")
    def attr_agent_space_id(self) -> builtins.str:
        '''The unique identifier of the Agent Space.

        :cloudformationAttribute: AgentSpaceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentSpaceId"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Agent Space.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the resource was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the resource was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Agent Space.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e1593c483d80afbaaf07c646b5d5ede131e360f81f0dde9fa486f5c749e58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Agent Space.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7561d8cdcaf93c81d1cf0a9a4cc5790c03232e494d49db5171a93599b8f575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_devopsagent.CfnAgentSpaceProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description"},
)
class CfnAgentSpaceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAgentSpace``.

        :param name: The name of the Agent Space.
        :param description: The description of the Agent Space.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-agentspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_devopsagent as devopsagent
            
            cfn_agent_space_props = devopsagent.CfnAgentSpaceProps(
                name="name",
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea00a21cf40eafce14a4e6e1a4cd3e9f843a2f2e416299a20a2159ce8cdb6d5f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Agent Space.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-agentspace.html#cfn-devopsagent-agentspace-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Agent Space.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-agentspace.html#cfn-devopsagent-agentspace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgentSpaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556, _IAssociationRef_ac0997e3)
class CfnAssociation(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation",
):
    '''The ``AWS::DevOpsAgent::Association`` resource specifies an association between an Agent Space and a service, defining how the Agent Space interacts with external services like GitHub, Slack, AWS accounts, and others.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html
    :cloudformationResource: AWS::DevOpsAgent::Association
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_devopsagent as devopsagent
        
        # resource_metadata: Any
        
        cfn_association = devopsagent.CfnAssociation(self, "MyCfnAssociation",
            agent_space_id="agentSpaceId",
            configuration=devopsagent.CfnAssociation.ServiceConfigurationProperty(
                aws=devopsagent.CfnAssociation.AWSConfigurationProperty(
                    account_id="accountId",
                    account_type="accountType",
                    assumable_role_arn="assumableRoleArn",
        
                    # the properties below are optional
                    resources=[devopsagent.CfnAssociation.AWSResourceProperty(
                        resource_arn="resourceArn",
        
                        # the properties below are optional
                        resource_metadata=resource_metadata,
                        resource_type="resourceType"
                    )],
                    tags=[devopsagent.CfnAssociation.KeyValuePairProperty(
                        key="key",
                        value="value"
                    )]
                ),
                dynatrace=devopsagent.CfnAssociation.DynatraceConfigurationProperty(
                    env_id="envId",
        
                    # the properties below are optional
                    enable_webhook_updates=False,
                    resources=["resources"]
                ),
                event_channel=devopsagent.CfnAssociation.EventChannelConfigurationProperty(
                    enable_webhook_updates=False
                ),
                git_hub=devopsagent.CfnAssociation.GitHubConfigurationProperty(
                    owner="owner",
                    owner_type="ownerType",
                    repo_id="repoId",
                    repo_name="repoName"
                ),
                git_lab=devopsagent.CfnAssociation.GitLabConfigurationProperty(
                    project_id="projectId",
                    project_path="projectPath",
        
                    # the properties below are optional
                    enable_webhook_updates=False,
                    instance_identifier="instanceIdentifier"
                ),
                mcp_server=devopsagent.CfnAssociation.MCPServerConfigurationProperty(
                    endpoint="endpoint",
                    name="name",
                    tools=["tools"],
        
                    # the properties below are optional
                    description="description",
                    enable_webhook_updates=False
                ),
                mcp_server_datadog=devopsagent.CfnAssociation.MCPServerDatadogConfigurationProperty(
                    endpoint="endpoint",
                    name="name",
        
                    # the properties below are optional
                    description="description",
                    enable_webhook_updates=False
                ),
                mcp_server_new_relic=devopsagent.CfnAssociation.MCPServerNewRelicConfigurationProperty(
                    account_id="accountId",
                    endpoint="endpoint"
                ),
                mcp_server_splunk=devopsagent.CfnAssociation.MCPServerSplunkConfigurationProperty(
                    endpoint="endpoint",
                    name="name",
        
                    # the properties below are optional
                    description="description",
                    enable_webhook_updates=False
                ),
                service_now=devopsagent.CfnAssociation.ServiceNowConfigurationProperty(
                    enable_webhook_updates=False,
                    instance_id="instanceId"
                ),
                slack=devopsagent.CfnAssociation.SlackConfigurationProperty(
                    transmission_target=devopsagent.CfnAssociation.SlackTransmissionTargetProperty(
                        incident_response_target=devopsagent.CfnAssociation.SlackChannelProperty(
                            channel_id="channelId",
        
                            # the properties below are optional
                            channel_name="channelName"
                        )
                    ),
                    workspace_id="workspaceId",
                    workspace_name="workspaceName"
                ),
                source_aws=devopsagent.CfnAssociation.SourceAwsConfigurationProperty(
                    account_id="accountId",
                    account_type="accountType",
                    assumable_role_arn="assumableRoleArn",
        
                    # the properties below are optional
                    resources=[devopsagent.CfnAssociation.AWSResourceProperty(
                        resource_arn="resourceArn",
        
                        # the properties below are optional
                        resource_metadata=resource_metadata,
                        resource_type="resourceType"
                    )],
                    tags=[devopsagent.CfnAssociation.KeyValuePairProperty(
                        key="key",
                        value="value"
                    )]
                )
            ),
            service_id="serviceId",
        
            # the properties below are optional
            linked_association_ids=["linkedAssociationIds"]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        agent_space_id: builtins.str,
        configuration: typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.ServiceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        service_id: builtins.str,
        linked_association_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::DevOpsAgent::Association``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param agent_space_id: The unique identifier of the Agent Space.
        :param configuration: The configuration that directs how the Agent Space interacts with the given service. You can specify only one configuration type per association. *Allowed Values* : ``SourceAws`` | ``Aws`` | ``GitHub`` | ``GitLab`` | ``Slack`` | ``Dynatrace`` | ``ServiceNow`` | ``MCPServer`` | ``MCPServerNewRelic`` | ``MCPServerDatadog`` | ``MCPServerSplunk`` | ``EventChannel``
        :param service_id: The identifier for the associated service. For ``SourceAws`` and ``Aws`` configurations, this must be ``aws`` . For all other service types, this is a UUID generated from the RegisterService command.
        :param linked_association_ids: Set of linked association IDs for parent-child relationships.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9507e77277cf05febf82ccf8829d008e3d5bca6bfbb5c229a629346a34d445ff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssociationProps(
            agent_space_id=agent_space_id,
            configuration=configuration,
            service_id=service_id,
            linked_association_ids=linked_association_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnAssociation")
    @builtins.classmethod
    def is_cfn_association(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnAssociation.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89cae44481f5807f4bcf3fcf5d08b660423111da523b22ba60bcaacf43a50aa9)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnAssociation", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd21b036854f8ed65af7b88356ee2787b8f2fb60324e8b7f39b6edf4992ce967)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0d4a7651eb08ad3bc11db7886a5718c26e72c5b665acd6183227b87adf00e4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="associationRef")
    def association_ref(self) -> "_AssociationReference_249ec236":
        '''A reference to a Association resource.'''
        return typing.cast("_AssociationReference_249ec236", jsii.get(self, "associationRef"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationId")
    def attr_association_id(self) -> builtins.str:
        '''The unique identifier of the association.

        :cloudformationAttribute: AssociationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the association was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the association was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="agentSpaceId")
    def agent_space_id(self) -> builtins.str:
        '''The unique identifier of the Agent Space.'''
        return typing.cast(builtins.str, jsii.get(self, "agentSpaceId"))

    @agent_space_id.setter
    def agent_space_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac4f12f5965b47ff3162eacbbbebb04e5d1595483e00e0e29ace1cd733b8156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentSpaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Union["_IResolvable_da3f097b", "CfnAssociation.ServiceConfigurationProperty"]:
        '''The configuration that directs how the Agent Space interacts with the given service.'''
        return typing.cast(typing.Union["_IResolvable_da3f097b", "CfnAssociation.ServiceConfigurationProperty"], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Union["_IResolvable_da3f097b", "CfnAssociation.ServiceConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b224d34e655755660b3f83f1ef3ad78de31336ef41e61cf24dfb47a3d5e00b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''The identifier for the associated service.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @service_id.setter
    def service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d88d472b1933bfd27859b1b634111a6667c50bedacee3234cfc98a8a05797a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkedAssociationIds")
    def linked_association_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of linked association IDs for parent-child relationships.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "linkedAssociationIds"))

    @linked_association_ids.setter
    def linked_association_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a926a8cb577bf81233b764232f042b444bc6a9e989283355f36b9faf248fe46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedAssociationIds", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.AWSConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "account_type": "accountType",
            "assumable_role_arn": "assumableRoleArn",
            "resources": "resources",
            "tags": "tags",
        },
    )
    class AWSConfigurationProperty:
        def __init__(
            self,
            *,
            account_id: builtins.str,
            account_type: builtins.str,
            assumable_role_arn: builtins.str,
            resources: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.AWSResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tags: typing.Optional[typing.Sequence[typing.Union["CfnAssociation.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for AWS monitor account integration.

            Specifies the account ID, assumable role ARN, and resources to be monitored in the primary monitoring account.

            :param account_id: Account ID corresponding to the provided resources.
            :param account_type: Account Type 'monitor' for AWS DevOps Agent monitoring.
            :param assumable_role_arn: Role ARN used by AWS DevOps Agent to access resources in the primary account.
            :param resources: List of resources to monitor.
            :param tags: List of tags as key-value pairs, used to identify resources for topology crawl.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                # resource_metadata: Any
                
                a_wSConfiguration_property = devopsagent.CfnAssociation.AWSConfigurationProperty(
                    account_id="accountId",
                    account_type="accountType",
                    assumable_role_arn="assumableRoleArn",
                
                    # the properties below are optional
                    resources=[devopsagent.CfnAssociation.AWSResourceProperty(
                        resource_arn="resourceArn",
                
                        # the properties below are optional
                        resource_metadata=resource_metadata,
                        resource_type="resourceType"
                    )],
                    tags=[devopsagent.CfnAssociation.KeyValuePairProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f1d632ade69849147b75fe20e7412c90e54c9e84dafe76046f35e5fa880436f)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
                check_type(argname="argument assumable_role_arn", value=assumable_role_arn, expected_type=type_hints["assumable_role_arn"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "account_id": account_id,
                "account_type": account_type,
                "assumable_role_arn": assumable_role_arn,
            }
            if resources is not None:
                self._values["resources"] = resources
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def account_id(self) -> builtins.str:
            '''Account ID corresponding to the provided resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-accountid
            '''
            result = self._values.get("account_id")
            assert result is not None, "Required property 'account_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def account_type(self) -> builtins.str:
            '''Account Type 'monitor' for AWS DevOps Agent monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-accounttype
            '''
            result = self._values.get("account_type")
            assert result is not None, "Required property 'account_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def assumable_role_arn(self) -> builtins.str:
            '''Role ARN used by AWS DevOps Agent to access resources in the primary account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-assumablerolearn
            '''
            result = self._values.get("assumable_role_arn")
            assert result is not None, "Required property 'assumable_role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def resources(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnAssociation.AWSResourceProperty"]]]]:
            '''List of resources to monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnAssociation.AWSResourceProperty"]]]], result)

        @builtins.property
        def tags(
            self,
        ) -> typing.Optional[typing.List["CfnAssociation.KeyValuePairProperty"]]:
            '''List of tags as key-value pairs, used to identify resources for topology crawl.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsconfiguration.html#cfn-devopsagent-association-awsconfiguration-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List["CfnAssociation.KeyValuePairProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.AWSResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_arn": "resourceArn",
            "resource_metadata": "resourceMetadata",
            "resource_type": "resourceType",
        },
    )
    class AWSResourceProperty:
        def __init__(
            self,
            *,
            resource_arn: builtins.str,
            resource_metadata: typing.Any = None,
            resource_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an AWS resource to be monitored, including its type, ARN, and optional metadata.

            :param resource_arn: The Amazon Resource Name (ARN) of the resource.
            :param resource_metadata: Additional metadata specific to the resource. This is an optional JSON object that can include resource-specific information to provide additional context for monitoring and management.
            :param resource_type: Resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                # resource_metadata: Any
                
                a_wSResource_property = devopsagent.CfnAssociation.AWSResourceProperty(
                    resource_arn="resourceArn",
                
                    # the properties below are optional
                    resource_metadata=resource_metadata,
                    resource_type="resourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c83865c7f5f4d4caa82576ab7efaac17f6225904d0ac52970333a1906f6ed0cb)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument resource_metadata", value=resource_metadata, expected_type=type_hints["resource_metadata"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resource_arn": resource_arn,
            }
            if resource_metadata is not None:
                self._values["resource_metadata"] = resource_metadata
            if resource_type is not None:
                self._values["resource_type"] = resource_type

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsresource.html#cfn-devopsagent-association-awsresource-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def resource_metadata(self) -> typing.Any:
            '''Additional metadata specific to the resource.

            This is an optional JSON object that can include resource-specific information to provide additional context for monitoring and management.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsresource.html#cfn-devopsagent-association-awsresource-resourcemetadata
            '''
            result = self._values.get("resource_metadata")
            return typing.cast(typing.Any, result)

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''Resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-awsresource.html#cfn-devopsagent-association-awsresource-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.DynatraceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "env_id": "envId",
            "enable_webhook_updates": "enableWebhookUpdates",
            "resources": "resources",
        },
    )
    class DynatraceConfigurationProperty:
        def __init__(
            self,
            *,
            env_id: builtins.str,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]] = None,
            resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration for Dynatrace monitoring integration.

            Defines the Dynatrace environment ID, list of resources to monitor, and webhook update settings required for the Agent Space to access metrics, traces, and logs from Dynatrace.

            :param env_id: Dynatrace environment id.
            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param resources: List of Dynatrace resources to monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-dynatraceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                dynatrace_configuration_property = devopsagent.CfnAssociation.DynatraceConfigurationProperty(
                    env_id="envId",
                
                    # the properties below are optional
                    enable_webhook_updates=False,
                    resources=["resources"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af533dc830c7a5f8fd17b5170cecf1e7dd483fe076400d57927aca27831a0ca8)
                check_type(argname="argument env_id", value=env_id, expected_type=type_hints["env_id"])
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "env_id": env_id,
            }
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if resources is not None:
                self._values["resources"] = resources

        @builtins.property
        def env_id(self) -> builtins.str:
            '''Dynatrace environment id.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-dynatraceconfiguration.html#cfn-devopsagent-association-dynatraceconfiguration-envid
            '''
            result = self._values.get("env_id")
            assert result is not None, "Required property 'env_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-dynatraceconfiguration.html#cfn-devopsagent-association-dynatraceconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]], result)

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of Dynatrace resources to monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-dynatraceconfiguration.html#cfn-devopsagent-association-dynatraceconfiguration-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.EventChannelConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enable_webhook_updates": "enableWebhookUpdates"},
    )
    class EventChannelConfigurationProperty:
        def __init__(
            self,
            *,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]] = None,
        ) -> None:
            '''Configuration for Event Channel integration.

            Defines webhook update settings to enable the Agent Space to receive real-time event notifications from event channel integrations.

            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-eventchannelconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                event_channel_configuration_property = devopsagent.CfnAssociation.EventChannelConfigurationProperty(
                    enable_webhook_updates=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5d900735d86a3a2a681d9eba7f3ce7754e8cdfbc47df16370253e165583cd41)
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-eventchannelconfiguration.html#cfn-devopsagent-association-eventchannelconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventChannelConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.GitHubConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "owner": "owner",
            "owner_type": "ownerType",
            "repo_id": "repoId",
            "repo_name": "repoName",
        },
    )
    class GitHubConfigurationProperty:
        def __init__(
            self,
            *,
            owner: builtins.str,
            owner_type: builtins.str,
            repo_id: builtins.str,
            repo_name: builtins.str,
        ) -> None:
            '''Configuration for GitHub repository integration.

            Defines the repository name, numeric repository ID, owner name, and owner type (user or organization) required for the Agent Space to access and interact with the GitHub repository.

            :param owner: Repository owner.
            :param owner_type: Type of repository owner.
            :param repo_id: Associated Github repo ID.
            :param repo_name: Associated Github repo name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                git_hub_configuration_property = devopsagent.CfnAssociation.GitHubConfigurationProperty(
                    owner="owner",
                    owner_type="ownerType",
                    repo_id="repoId",
                    repo_name="repoName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f52e2bfd74e3e041299304fca2e11acf7c77935cb3d81768bd90034e89f0c1f3)
                check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
                check_type(argname="argument owner_type", value=owner_type, expected_type=type_hints["owner_type"])
                check_type(argname="argument repo_id", value=repo_id, expected_type=type_hints["repo_id"])
                check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "owner": owner,
                "owner_type": owner_type,
                "repo_id": repo_id,
                "repo_name": repo_name,
            }

        @builtins.property
        def owner(self) -> builtins.str:
            '''Repository owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html#cfn-devopsagent-association-githubconfiguration-owner
            '''
            result = self._values.get("owner")
            assert result is not None, "Required property 'owner' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def owner_type(self) -> builtins.str:
            '''Type of repository owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html#cfn-devopsagent-association-githubconfiguration-ownertype
            '''
            result = self._values.get("owner_type")
            assert result is not None, "Required property 'owner_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def repo_id(self) -> builtins.str:
            '''Associated Github repo ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html#cfn-devopsagent-association-githubconfiguration-repoid
            '''
            result = self._values.get("repo_id")
            assert result is not None, "Required property 'repo_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def repo_name(self) -> builtins.str:
            '''Associated Github repo name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-githubconfiguration.html#cfn-devopsagent-association-githubconfiguration-reponame
            '''
            result = self._values.get("repo_name")
            assert result is not None, "Required property 'repo_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitHubConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.GitLabConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "project_id": "projectId",
            "project_path": "projectPath",
            "enable_webhook_updates": "enableWebhookUpdates",
            "instance_identifier": "instanceIdentifier",
        },
    )
    class GitLabConfigurationProperty:
        def __init__(
            self,
            *,
            project_id: builtins.str,
            project_path: builtins.str,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]] = None,
            instance_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for GitLab project integration.

            Defines the numeric project ID, full project path (namespace/project-name), GitLab instance identifier, and webhook update settings required for the Agent Space to access and interact with the GitLab project.

            :param project_id: GitLab numeric project ID.
            :param project_path: Full GitLab project path (e.g., namespace/project-name).
            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param instance_identifier: GitLab instance identifier (e.g., gitlab.com).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                git_lab_configuration_property = devopsagent.CfnAssociation.GitLabConfigurationProperty(
                    project_id="projectId",
                    project_path="projectPath",
                
                    # the properties below are optional
                    enable_webhook_updates=False,
                    instance_identifier="instanceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d0bf76d18d2da5c1a7b65fd908fdd6aa4ca798335d0ef9f07ec4c064ccb5241)
                check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
                check_type(argname="argument project_path", value=project_path, expected_type=type_hints["project_path"])
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument instance_identifier", value=instance_identifier, expected_type=type_hints["instance_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "project_id": project_id,
                "project_path": project_path,
            }
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if instance_identifier is not None:
                self._values["instance_identifier"] = instance_identifier

        @builtins.property
        def project_id(self) -> builtins.str:
            '''GitLab numeric project ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html#cfn-devopsagent-association-gitlabconfiguration-projectid
            '''
            result = self._values.get("project_id")
            assert result is not None, "Required property 'project_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def project_path(self) -> builtins.str:
            '''Full GitLab project path (e.g., namespace/project-name).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html#cfn-devopsagent-association-gitlabconfiguration-projectpath
            '''
            result = self._values.get("project_path")
            assert result is not None, "Required property 'project_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html#cfn-devopsagent-association-gitlabconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]], result)

        @builtins.property
        def instance_identifier(self) -> typing.Optional[builtins.str]:
            '''GitLab instance identifier (e.g., gitlab.com).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-gitlabconfiguration.html#cfn-devopsagent-association-gitlabconfiguration-instanceidentifier
            '''
            result = self._values.get("instance_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitLabConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.KeyValuePairProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class KeyValuePairProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''A key-value pair for tags.

            :param key: The key name of the tag.
            :param value: The value for the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-keyvaluepair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                key_value_pair_property = devopsagent.CfnAssociation.KeyValuePairProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ded74f7f3af261fdfeb1ca20f0589b46cd28465b569b567f86c794c6d2010df2)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The key name of the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-keyvaluepair.html#cfn-devopsagent-association-keyvaluepair-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value for the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-keyvaluepair.html#cfn-devopsagent-association-keyvaluepair-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyValuePairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.MCPServerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint": "endpoint",
            "name": "name",
            "tools": "tools",
            "description": "description",
            "enable_webhook_updates": "enableWebhookUpdates",
        },
    )
    class MCPServerConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint: builtins.str,
            name: builtins.str,
            tools: typing.Sequence[builtins.str],
            description: typing.Optional[builtins.str] = None,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]] = None,
        ) -> None:
            '''Configuration for MCP (Model Context Protocol) server integration.

            Defines the server name, endpoint URL, available tools, optional description, and webhook update settings for custom MCP servers.

            :param endpoint: MCP server endpoint URL.
            :param name: The name of the MCP server.
            :param tools: List of MCP tools that can be used with the association.
            :param description: The description of the MCP server.
            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                m_cPServer_configuration_property = devopsagent.CfnAssociation.MCPServerConfigurationProperty(
                    endpoint="endpoint",
                    name="name",
                    tools=["tools"],
                
                    # the properties below are optional
                    description="description",
                    enable_webhook_updates=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97d8de94964f9d444ce60e60c71a8386873d9d717628a8b450e0463922b08600)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tools", value=tools, expected_type=type_hints["tools"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "endpoint": endpoint,
                "name": name,
                "tools": tools,
            }
            if description is not None:
                self._values["description"] = description
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates

        @builtins.property
        def endpoint(self) -> builtins.str:
            '''MCP server endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def tools(self) -> typing.List[builtins.str]:
            '''List of MCP tools that can be used with the association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-tools
            '''
            result = self._values.get("tools")
            assert result is not None, "Required property 'tools' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverconfiguration.html#cfn-devopsagent-association-mcpserverconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPServerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.MCPServerDatadogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint": "endpoint",
            "name": "name",
            "description": "description",
            "enable_webhook_updates": "enableWebhookUpdates",
        },
    )
    class MCPServerDatadogConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint: builtins.str,
            name: builtins.str,
            description: typing.Optional[builtins.str] = None,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]] = None,
        ) -> None:
            '''Configuration for Datadog MCP server integration.

            Defines the server name, endpoint URL, optional description, and webhook update settings.

            :param endpoint: MCP server endpoint URL.
            :param name: The name of the MCP server.
            :param description: The description of the MCP server.
            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                m_cPServer_datadog_configuration_property = devopsagent.CfnAssociation.MCPServerDatadogConfigurationProperty(
                    endpoint="endpoint",
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    enable_webhook_updates=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94bdd66d2ae6508b6fa75de77b1b7bd044d6bf7b9e0c60cb573f57ca7faa1817)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "endpoint": endpoint,
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates

        @builtins.property
        def endpoint(self) -> builtins.str:
            '''MCP server endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html#cfn-devopsagent-association-mcpserverdatadogconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html#cfn-devopsagent-association-mcpserverdatadogconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html#cfn-devopsagent-association-mcpserverdatadogconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserverdatadogconfiguration.html#cfn-devopsagent-association-mcpserverdatadogconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPServerDatadogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.MCPServerNewRelicConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"account_id": "accountId", "endpoint": "endpoint"},
    )
    class MCPServerNewRelicConfigurationProperty:
        def __init__(self, *, account_id: builtins.str, endpoint: builtins.str) -> None:
            '''Configuration for New Relic MCP server integration.

            Defines the New Relic account ID and MCP server endpoint URL required for the Agent Space to authenticate and query observability data from New Relic.

            :param account_id: New Relic Account ID.
            :param endpoint: MCP server endpoint URL (e.g., https://mcp.newrelic.com/mcp/).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpservernewrelicconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                m_cPServer_new_relic_configuration_property = devopsagent.CfnAssociation.MCPServerNewRelicConfigurationProperty(
                    account_id="accountId",
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d60c2241968bd47959618d5fef16076f92aa6b8c2e1932e3d7d5e3983c4108a8)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "account_id": account_id,
                "endpoint": endpoint,
            }

        @builtins.property
        def account_id(self) -> builtins.str:
            '''New Relic Account ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpservernewrelicconfiguration.html#cfn-devopsagent-association-mcpservernewrelicconfiguration-accountid
            '''
            result = self._values.get("account_id")
            assert result is not None, "Required property 'account_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def endpoint(self) -> builtins.str:
            '''MCP server endpoint URL (e.g., https://mcp.newrelic.com/mcp/).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpservernewrelicconfiguration.html#cfn-devopsagent-association-mcpservernewrelicconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPServerNewRelicConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.MCPServerSplunkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint": "endpoint",
            "name": "name",
            "description": "description",
            "enable_webhook_updates": "enableWebhookUpdates",
        },
    )
    class MCPServerSplunkConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint: builtins.str,
            name: builtins.str,
            description: typing.Optional[builtins.str] = None,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]] = None,
        ) -> None:
            '''Configuration for Splunk MCP server integration.

            Defines the server name, endpoint URL, optional description, and webhook update settings.

            :param endpoint: MCP server endpoint URL.
            :param name: The name of the MCP server.
            :param description: The description of the MCP server.
            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                m_cPServer_splunk_configuration_property = devopsagent.CfnAssociation.MCPServerSplunkConfigurationProperty(
                    endpoint="endpoint",
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    enable_webhook_updates=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5251bb56068759277d9b99b06c4d20b0e0434473774eeb3d825f9ed5301ba970)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "endpoint": endpoint,
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates

        @builtins.property
        def endpoint(self) -> builtins.str:
            '''MCP server endpoint URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html#cfn-devopsagent-association-mcpserversplunkconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html#cfn-devopsagent-association-mcpserversplunkconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the MCP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html#cfn-devopsagent-association-mcpserversplunkconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-mcpserversplunkconfiguration.html#cfn-devopsagent-association-mcpserversplunkconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MCPServerSplunkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.ServiceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws": "aws",
            "dynatrace": "dynatrace",
            "event_channel": "eventChannel",
            "git_hub": "gitHub",
            "git_lab": "gitLab",
            "mcp_server": "mcpServer",
            "mcp_server_datadog": "mcpServerDatadog",
            "mcp_server_new_relic": "mcpServerNewRelic",
            "mcp_server_splunk": "mcpServerSplunk",
            "service_now": "serviceNow",
            "slack": "slack",
            "source_aws": "sourceAws",
        },
    )
    class ServiceConfigurationProperty:
        def __init__(
            self,
            *,
            aws: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.AWSConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynatrace: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.DynatraceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            event_channel: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.EventChannelConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            git_hub: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.GitHubConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            git_lab: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.GitLabConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.MCPServerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server_datadog: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.MCPServerDatadogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server_new_relic: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.MCPServerNewRelicConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mcp_server_splunk: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.MCPServerSplunkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.ServiceNowConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            slack: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.SlackConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_aws: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.SourceAwsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration that directs how Agent Space interacts with the given service.

            You can specify only one configuration type per association.

            :param aws: Configuration for AWS monitor account integration. Specifies the account ID, assumable role ARN, and resources to be monitored in the primary monitoring account.
            :param dynatrace: Configuration for Dynatrace monitoring integration. Specifies the environment ID, resources to monitor, and webhook settings to enable the Agent Space to access Dynatrace metrics, traces, and logs.
            :param event_channel: Configuration for Event Channel integration. Specifies webhook settings to enable the Agent Space to receive and process real-time events from external systems.
            :param git_hub: Configuration for GitHub repository integration. Specifies the repository name, repository ID, owner, and owner type to enable the Agent Space to access code, pull requests, and issues.
            :param git_lab: Configuration for GitLab project integration. Specifies the project ID, project path, instance identifier, and webhook settings to enable the Agent Space to access code, merge requests, and issues.
            :param mcp_server: Configuration for custom MCP (Model Context Protocol) server integration. Specifies the server name, endpoint URL, available tools, description, and webhook settings to enable the Agent Space to interact with custom MCP servers.
            :param mcp_server_datadog: Configuration for Datadog MCP server integration. Specifies the server name, endpoint URL, optional description, and webhook settings to enable the Agent Space to query metrics, traces, and logs from Datadog.
            :param mcp_server_new_relic: Configuration for New Relic MCP server integration. Specifies the New Relic account ID and MCP endpoint URL to enable the Agent Space to query metrics, traces, and logs from New Relic.
            :param mcp_server_splunk: Configuration for Splunk MCP server integration. Specifies the server name, endpoint URL, optional description, and webhook settings to enable the Agent Space to query logs, metrics, and events from Splunk.
            :param service_now: Configuration for ServiceNow instance integration. Specifies the instance URL, instance ID, and webhook settings to enable the Agent Space to create, update, and manage ServiceNow incidents and change requests.
            :param slack: Configuration for Slack workspace integration. Specifies the workspace ID, workspace name, and transmission targets to enable the Agent Space to send notifications to designated Slack channels.
            :param source_aws: Configuration for AWS source account integration. Specifies the account ID, assumable role ARN, and resources to be monitored in the source account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                # resource_metadata: Any
                
                service_configuration_property = devopsagent.CfnAssociation.ServiceConfigurationProperty(
                    aws=devopsagent.CfnAssociation.AWSConfigurationProperty(
                        account_id="accountId",
                        account_type="accountType",
                        assumable_role_arn="assumableRoleArn",
                
                        # the properties below are optional
                        resources=[devopsagent.CfnAssociation.AWSResourceProperty(
                            resource_arn="resourceArn",
                
                            # the properties below are optional
                            resource_metadata=resource_metadata,
                            resource_type="resourceType"
                        )],
                        tags=[devopsagent.CfnAssociation.KeyValuePairProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    dynatrace=devopsagent.CfnAssociation.DynatraceConfigurationProperty(
                        env_id="envId",
                
                        # the properties below are optional
                        enable_webhook_updates=False,
                        resources=["resources"]
                    ),
                    event_channel=devopsagent.CfnAssociation.EventChannelConfigurationProperty(
                        enable_webhook_updates=False
                    ),
                    git_hub=devopsagent.CfnAssociation.GitHubConfigurationProperty(
                        owner="owner",
                        owner_type="ownerType",
                        repo_id="repoId",
                        repo_name="repoName"
                    ),
                    git_lab=devopsagent.CfnAssociation.GitLabConfigurationProperty(
                        project_id="projectId",
                        project_path="projectPath",
                
                        # the properties below are optional
                        enable_webhook_updates=False,
                        instance_identifier="instanceIdentifier"
                    ),
                    mcp_server=devopsagent.CfnAssociation.MCPServerConfigurationProperty(
                        endpoint="endpoint",
                        name="name",
                        tools=["tools"],
                
                        # the properties below are optional
                        description="description",
                        enable_webhook_updates=False
                    ),
                    mcp_server_datadog=devopsagent.CfnAssociation.MCPServerDatadogConfigurationProperty(
                        endpoint="endpoint",
                        name="name",
                
                        # the properties below are optional
                        description="description",
                        enable_webhook_updates=False
                    ),
                    mcp_server_new_relic=devopsagent.CfnAssociation.MCPServerNewRelicConfigurationProperty(
                        account_id="accountId",
                        endpoint="endpoint"
                    ),
                    mcp_server_splunk=devopsagent.CfnAssociation.MCPServerSplunkConfigurationProperty(
                        endpoint="endpoint",
                        name="name",
                
                        # the properties below are optional
                        description="description",
                        enable_webhook_updates=False
                    ),
                    service_now=devopsagent.CfnAssociation.ServiceNowConfigurationProperty(
                        enable_webhook_updates=False,
                        instance_id="instanceId"
                    ),
                    slack=devopsagent.CfnAssociation.SlackConfigurationProperty(
                        transmission_target=devopsagent.CfnAssociation.SlackTransmissionTargetProperty(
                            incident_response_target=devopsagent.CfnAssociation.SlackChannelProperty(
                                channel_id="channelId",
                
                                # the properties below are optional
                                channel_name="channelName"
                            )
                        ),
                        workspace_id="workspaceId",
                        workspace_name="workspaceName"
                    ),
                    source_aws=devopsagent.CfnAssociation.SourceAwsConfigurationProperty(
                        account_id="accountId",
                        account_type="accountType",
                        assumable_role_arn="assumableRoleArn",
                
                        # the properties below are optional
                        resources=[devopsagent.CfnAssociation.AWSResourceProperty(
                            resource_arn="resourceArn",
                
                            # the properties below are optional
                            resource_metadata=resource_metadata,
                            resource_type="resourceType"
                        )],
                        tags=[devopsagent.CfnAssociation.KeyValuePairProperty(
                            key="key",
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__534ff66bec4c3f764380e71fc8dbccb3b6b0319f301032fa7e975aa1842a74e1)
                check_type(argname="argument aws", value=aws, expected_type=type_hints["aws"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument event_channel", value=event_channel, expected_type=type_hints["event_channel"])
                check_type(argname="argument git_hub", value=git_hub, expected_type=type_hints["git_hub"])
                check_type(argname="argument git_lab", value=git_lab, expected_type=type_hints["git_lab"])
                check_type(argname="argument mcp_server", value=mcp_server, expected_type=type_hints["mcp_server"])
                check_type(argname="argument mcp_server_datadog", value=mcp_server_datadog, expected_type=type_hints["mcp_server_datadog"])
                check_type(argname="argument mcp_server_new_relic", value=mcp_server_new_relic, expected_type=type_hints["mcp_server_new_relic"])
                check_type(argname="argument mcp_server_splunk", value=mcp_server_splunk, expected_type=type_hints["mcp_server_splunk"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument source_aws", value=source_aws, expected_type=type_hints["source_aws"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws is not None:
                self._values["aws"] = aws
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if event_channel is not None:
                self._values["event_channel"] = event_channel
            if git_hub is not None:
                self._values["git_hub"] = git_hub
            if git_lab is not None:
                self._values["git_lab"] = git_lab
            if mcp_server is not None:
                self._values["mcp_server"] = mcp_server
            if mcp_server_datadog is not None:
                self._values["mcp_server_datadog"] = mcp_server_datadog
            if mcp_server_new_relic is not None:
                self._values["mcp_server_new_relic"] = mcp_server_new_relic
            if mcp_server_splunk is not None:
                self._values["mcp_server_splunk"] = mcp_server_splunk
            if service_now is not None:
                self._values["service_now"] = service_now
            if slack is not None:
                self._values["slack"] = slack
            if source_aws is not None:
                self._values["source_aws"] = source_aws

        @builtins.property
        def aws(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.AWSConfigurationProperty"]]:
            '''Configuration for AWS monitor account integration.

            Specifies the account ID, assumable role ARN, and resources to be monitored in the primary monitoring account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-aws
            '''
            result = self._values.get("aws")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.AWSConfigurationProperty"]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.DynatraceConfigurationProperty"]]:
            '''Configuration for Dynatrace monitoring integration.

            Specifies the environment ID, resources to monitor, and webhook settings to enable the Agent Space to access Dynatrace metrics, traces, and logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.DynatraceConfigurationProperty"]], result)

        @builtins.property
        def event_channel(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.EventChannelConfigurationProperty"]]:
            '''Configuration for Event Channel integration.

            Specifies webhook settings to enable the Agent Space to receive and process real-time events from external systems.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-eventchannel
            '''
            result = self._values.get("event_channel")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.EventChannelConfigurationProperty"]], result)

        @builtins.property
        def git_hub(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.GitHubConfigurationProperty"]]:
            '''Configuration for GitHub repository integration.

            Specifies the repository name, repository ID, owner, and owner type to enable the Agent Space to access code, pull requests, and issues.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-github
            '''
            result = self._values.get("git_hub")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.GitHubConfigurationProperty"]], result)

        @builtins.property
        def git_lab(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.GitLabConfigurationProperty"]]:
            '''Configuration for GitLab project integration.

            Specifies the project ID, project path, instance identifier, and webhook settings to enable the Agent Space to access code, merge requests, and issues.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-gitlab
            '''
            result = self._values.get("git_lab")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.GitLabConfigurationProperty"]], result)

        @builtins.property
        def mcp_server(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.MCPServerConfigurationProperty"]]:
            '''Configuration for custom MCP (Model Context Protocol) server integration.

            Specifies the server name, endpoint URL, available tools, description, and webhook settings to enable the Agent Space to interact with custom MCP servers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-mcpserver
            '''
            result = self._values.get("mcp_server")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.MCPServerConfigurationProperty"]], result)

        @builtins.property
        def mcp_server_datadog(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.MCPServerDatadogConfigurationProperty"]]:
            '''Configuration for Datadog MCP server integration.

            Specifies the server name, endpoint URL, optional description, and webhook settings to enable the Agent Space to query metrics, traces, and logs from Datadog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-mcpserverdatadog
            '''
            result = self._values.get("mcp_server_datadog")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.MCPServerDatadogConfigurationProperty"]], result)

        @builtins.property
        def mcp_server_new_relic(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.MCPServerNewRelicConfigurationProperty"]]:
            '''Configuration for New Relic MCP server integration.

            Specifies the New Relic account ID and MCP endpoint URL to enable the Agent Space to query metrics, traces, and logs from New Relic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-mcpservernewrelic
            '''
            result = self._values.get("mcp_server_new_relic")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.MCPServerNewRelicConfigurationProperty"]], result)

        @builtins.property
        def mcp_server_splunk(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.MCPServerSplunkConfigurationProperty"]]:
            '''Configuration for Splunk MCP server integration.

            Specifies the server name, endpoint URL, optional description, and webhook settings to enable the Agent Space to query logs, metrics, and events from Splunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-mcpserversplunk
            '''
            result = self._values.get("mcp_server_splunk")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.MCPServerSplunkConfigurationProperty"]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.ServiceNowConfigurationProperty"]]:
            '''Configuration for ServiceNow instance integration.

            Specifies the instance URL, instance ID, and webhook settings to enable the Agent Space to create, update, and manage ServiceNow incidents and change requests.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.ServiceNowConfigurationProperty"]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.SlackConfigurationProperty"]]:
            '''Configuration for Slack workspace integration.

            Specifies the workspace ID, workspace name, and transmission targets to enable the Agent Space to send notifications to designated Slack channels.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.SlackConfigurationProperty"]], result)

        @builtins.property
        def source_aws(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.SourceAwsConfigurationProperty"]]:
            '''Configuration for AWS source account integration.

            Specifies the account ID, assumable role ARN, and resources to be monitored in the source account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-serviceconfiguration.html#cfn-devopsagent-association-serviceconfiguration-sourceaws
            '''
            result = self._values.get("source_aws")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnAssociation.SourceAwsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.ServiceNowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_webhook_updates": "enableWebhookUpdates",
            "instance_id": "instanceId",
        },
    )
    class ServiceNowConfigurationProperty:
        def __init__(
            self,
            *,
            enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]] = None,
            instance_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for ServiceNow integration.

            Defines the ServiceNow instance URL, instance ID, and webhook update settings required for the Agent Space to create, update, and manage incidents and change requests.

            :param enable_webhook_updates: When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.
            :param instance_id: ServiceNow instance ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-servicenowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                service_now_configuration_property = devopsagent.CfnAssociation.ServiceNowConfigurationProperty(
                    enable_webhook_updates=False,
                    instance_id="instanceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9767ae84f8f9ac8fbffe3c19d1ac1dc61d581770deb87d97b058eb73cc671511)
                check_type(argname="argument enable_webhook_updates", value=enable_webhook_updates, expected_type=type_hints["enable_webhook_updates"])
                check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_webhook_updates is not None:
                self._values["enable_webhook_updates"] = enable_webhook_updates
            if instance_id is not None:
                self._values["instance_id"] = instance_id

        @builtins.property
        def enable_webhook_updates(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]]:
            '''When set to true, enables the Agent Space to create and update webhooks for receiving notifications and events from the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-servicenowconfiguration.html#cfn-devopsagent-association-servicenowconfiguration-enablewebhookupdates
            '''
            result = self._values.get("enable_webhook_updates")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_IResolvable_da3f097b"]], result)

        @builtins.property
        def instance_id(self) -> typing.Optional[builtins.str]:
            '''ServiceNow instance ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-servicenowconfiguration.html#cfn-devopsagent-association-servicenowconfiguration-instanceid
            '''
            result = self._values.get("instance_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.SlackChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_id": "channelId", "channel_name": "channelName"},
    )
    class SlackChannelProperty:
        def __init__(
            self,
            *,
            channel_id: builtins.str,
            channel_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a Slack channel with its unique identifier and optional display name.

            :param channel_id: Slack channel ID.
            :param channel_name: Slack channel name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackchannel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                slack_channel_property = devopsagent.CfnAssociation.SlackChannelProperty(
                    channel_id="channelId",
                
                    # the properties below are optional
                    channel_name="channelName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06cf6d0fee94466c60ffb3cbfb9f571fb9f69201085fc5de6cd2f0d6e4b8d633)
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
                check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "channel_id": channel_id,
            }
            if channel_name is not None:
                self._values["channel_name"] = channel_name

        @builtins.property
        def channel_id(self) -> builtins.str:
            '''Slack channel ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackchannel.html#cfn-devopsagent-association-slackchannel-channelid
            '''
            result = self._values.get("channel_id")
            assert result is not None, "Required property 'channel_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def channel_name(self) -> typing.Optional[builtins.str]:
            '''Slack channel name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackchannel.html#cfn-devopsagent-association-slackchannel-channelname
            '''
            result = self._values.get("channel_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.SlackConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "transmission_target": "transmissionTarget",
            "workspace_id": "workspaceId",
            "workspace_name": "workspaceName",
        },
    )
    class SlackConfigurationProperty:
        def __init__(
            self,
            *,
            transmission_target: typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.SlackTransmissionTargetProperty", typing.Dict[builtins.str, typing.Any]]],
            workspace_id: builtins.str,
            workspace_name: builtins.str,
        ) -> None:
            '''Configuration for Slack workspace integration.

            Defines the workspace ID, workspace name, and transmission targets that specify which Slack channels receive notifications.

            :param transmission_target: Transmission targets for agent notifications.
            :param workspace_id: Associated Slack workspace ID.
            :param workspace_name: Associated Slack workspace name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                slack_configuration_property = devopsagent.CfnAssociation.SlackConfigurationProperty(
                    transmission_target=devopsagent.CfnAssociation.SlackTransmissionTargetProperty(
                        incident_response_target=devopsagent.CfnAssociation.SlackChannelProperty(
                            channel_id="channelId",
                
                            # the properties below are optional
                            channel_name="channelName"
                        )
                    ),
                    workspace_id="workspaceId",
                    workspace_name="workspaceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28eb759dbeb853e46c5ba811aba401a06c7b87554a3bac255792e3d13c3f0c23)
                check_type(argname="argument transmission_target", value=transmission_target, expected_type=type_hints["transmission_target"])
                check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
                check_type(argname="argument workspace_name", value=workspace_name, expected_type=type_hints["workspace_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "transmission_target": transmission_target,
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
            }

        @builtins.property
        def transmission_target(
            self,
        ) -> typing.Union["_IResolvable_da3f097b", "CfnAssociation.SlackTransmissionTargetProperty"]:
            '''Transmission targets for agent notifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackconfiguration.html#cfn-devopsagent-association-slackconfiguration-transmissiontarget
            '''
            result = self._values.get("transmission_target")
            assert result is not None, "Required property 'transmission_target' is missing"
            return typing.cast(typing.Union["_IResolvable_da3f097b", "CfnAssociation.SlackTransmissionTargetProperty"], result)

        @builtins.property
        def workspace_id(self) -> builtins.str:
            '''Associated Slack workspace ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackconfiguration.html#cfn-devopsagent-association-slackconfiguration-workspaceid
            '''
            result = self._values.get("workspace_id")
            assert result is not None, "Required property 'workspace_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def workspace_name(self) -> builtins.str:
            '''Associated Slack workspace name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slackconfiguration.html#cfn-devopsagent-association-slackconfiguration-workspacename
            '''
            result = self._values.get("workspace_name")
            assert result is not None, "Required property 'workspace_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.SlackTransmissionTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"incident_response_target": "incidentResponseTarget"},
    )
    class SlackTransmissionTargetProperty:
        def __init__(
            self,
            *,
            incident_response_target: typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.SlackChannelProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Defines the Slack channels where different types of agent notifications will be sent.

            :param incident_response_target: Destination for AWS DevOps Agent Incident Response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slacktransmissiontarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                slack_transmission_target_property = devopsagent.CfnAssociation.SlackTransmissionTargetProperty(
                    incident_response_target=devopsagent.CfnAssociation.SlackChannelProperty(
                        channel_id="channelId",
                
                        # the properties below are optional
                        channel_name="channelName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4224928b94c6f3a7e8aeb21f4d921f668ae91ec705e4026d010b1813687b20c5)
                check_type(argname="argument incident_response_target", value=incident_response_target, expected_type=type_hints["incident_response_target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "incident_response_target": incident_response_target,
            }

        @builtins.property
        def incident_response_target(
            self,
        ) -> typing.Union["_IResolvable_da3f097b", "CfnAssociation.SlackChannelProperty"]:
            '''Destination for AWS DevOps Agent Incident Response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-slacktransmissiontarget.html#cfn-devopsagent-association-slacktransmissiontarget-incidentresponsetarget
            '''
            result = self._values.get("incident_response_target")
            assert result is not None, "Required property 'incident_response_target' is missing"
            return typing.cast(typing.Union["_IResolvable_da3f097b", "CfnAssociation.SlackChannelProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackTransmissionTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociation.SourceAwsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "account_type": "accountType",
            "assumable_role_arn": "assumableRoleArn",
            "resources": "resources",
            "tags": "tags",
        },
    )
    class SourceAwsConfigurationProperty:
        def __init__(
            self,
            *,
            account_id: builtins.str,
            account_type: builtins.str,
            assumable_role_arn: builtins.str,
            resources: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.AWSResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tags: typing.Optional[typing.Sequence[typing.Union["CfnAssociation.KeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for AWS source account integration.

            Specifies the account ID, assumable role ARN, and resources to be monitored in the source account.

            :param account_id: Account ID corresponding to the provided resources.
            :param account_type: Account Type 'source' for AWS DevOps Agent monitoring.
            :param assumable_role_arn: Role ARN to be assumed by AWS DevOps Agent to operate on behalf of customer.
            :param resources: List of resources to monitor.
            :param tags: List of tags as key-value pairs, used to identify resources for topology crawl.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_devopsagent as devopsagent
                
                # resource_metadata: Any
                
                source_aws_configuration_property = devopsagent.CfnAssociation.SourceAwsConfigurationProperty(
                    account_id="accountId",
                    account_type="accountType",
                    assumable_role_arn="assumableRoleArn",
                
                    # the properties below are optional
                    resources=[devopsagent.CfnAssociation.AWSResourceProperty(
                        resource_arn="resourceArn",
                
                        # the properties below are optional
                        resource_metadata=resource_metadata,
                        resource_type="resourceType"
                    )],
                    tags=[devopsagent.CfnAssociation.KeyValuePairProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7f309a9bf78a2704dbd1fd90dfdf8ff7ac7091cdb4572312fad3281cfcbd5ac)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
                check_type(argname="argument assumable_role_arn", value=assumable_role_arn, expected_type=type_hints["assumable_role_arn"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "account_id": account_id,
                "account_type": account_type,
                "assumable_role_arn": assumable_role_arn,
            }
            if resources is not None:
                self._values["resources"] = resources
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def account_id(self) -> builtins.str:
            '''Account ID corresponding to the provided resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-accountid
            '''
            result = self._values.get("account_id")
            assert result is not None, "Required property 'account_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def account_type(self) -> builtins.str:
            '''Account Type 'source' for AWS DevOps Agent monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-accounttype
            '''
            result = self._values.get("account_type")
            assert result is not None, "Required property 'account_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def assumable_role_arn(self) -> builtins.str:
            '''Role ARN to be assumed by AWS DevOps Agent to operate on behalf of customer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-assumablerolearn
            '''
            result = self._values.get("assumable_role_arn")
            assert result is not None, "Required property 'assumable_role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def resources(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnAssociation.AWSResourceProperty"]]]]:
            '''List of resources to monitor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnAssociation.AWSResourceProperty"]]]], result)

        @builtins.property
        def tags(
            self,
        ) -> typing.Optional[typing.List["CfnAssociation.KeyValuePairProperty"]]:
            '''List of tags as key-value pairs, used to identify resources for topology crawl.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsagent-association-sourceawsconfiguration.html#cfn-devopsagent-association-sourceawsconfiguration-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List["CfnAssociation.KeyValuePairProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceAwsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_devopsagent.CfnAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_space_id": "agentSpaceId",
        "configuration": "configuration",
        "service_id": "serviceId",
        "linked_association_ids": "linkedAssociationIds",
    },
)
class CfnAssociationProps:
    def __init__(
        self,
        *,
        agent_space_id: builtins.str,
        configuration: typing.Union["_IResolvable_da3f097b", typing.Union["CfnAssociation.ServiceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        service_id: builtins.str,
        linked_association_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAssociation``.

        :param agent_space_id: The unique identifier of the Agent Space.
        :param configuration: The configuration that directs how the Agent Space interacts with the given service. You can specify only one configuration type per association. *Allowed Values* : ``SourceAws`` | ``Aws`` | ``GitHub`` | ``GitLab`` | ``Slack`` | ``Dynatrace`` | ``ServiceNow`` | ``MCPServer`` | ``MCPServerNewRelic`` | ``MCPServerDatadog`` | ``MCPServerSplunk`` | ``EventChannel``
        :param service_id: The identifier for the associated service. For ``SourceAws`` and ``Aws`` configurations, this must be ``aws`` . For all other service types, this is a UUID generated from the RegisterService command.
        :param linked_association_ids: Set of linked association IDs for parent-child relationships.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_devopsagent as devopsagent
            
            # resource_metadata: Any
            
            cfn_association_props = devopsagent.CfnAssociationProps(
                agent_space_id="agentSpaceId",
                configuration=devopsagent.CfnAssociation.ServiceConfigurationProperty(
                    aws=devopsagent.CfnAssociation.AWSConfigurationProperty(
                        account_id="accountId",
                        account_type="accountType",
                        assumable_role_arn="assumableRoleArn",
            
                        # the properties below are optional
                        resources=[devopsagent.CfnAssociation.AWSResourceProperty(
                            resource_arn="resourceArn",
            
                            # the properties below are optional
                            resource_metadata=resource_metadata,
                            resource_type="resourceType"
                        )],
                        tags=[devopsagent.CfnAssociation.KeyValuePairProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    dynatrace=devopsagent.CfnAssociation.DynatraceConfigurationProperty(
                        env_id="envId",
            
                        # the properties below are optional
                        enable_webhook_updates=False,
                        resources=["resources"]
                    ),
                    event_channel=devopsagent.CfnAssociation.EventChannelConfigurationProperty(
                        enable_webhook_updates=False
                    ),
                    git_hub=devopsagent.CfnAssociation.GitHubConfigurationProperty(
                        owner="owner",
                        owner_type="ownerType",
                        repo_id="repoId",
                        repo_name="repoName"
                    ),
                    git_lab=devopsagent.CfnAssociation.GitLabConfigurationProperty(
                        project_id="projectId",
                        project_path="projectPath",
            
                        # the properties below are optional
                        enable_webhook_updates=False,
                        instance_identifier="instanceIdentifier"
                    ),
                    mcp_server=devopsagent.CfnAssociation.MCPServerConfigurationProperty(
                        endpoint="endpoint",
                        name="name",
                        tools=["tools"],
            
                        # the properties below are optional
                        description="description",
                        enable_webhook_updates=False
                    ),
                    mcp_server_datadog=devopsagent.CfnAssociation.MCPServerDatadogConfigurationProperty(
                        endpoint="endpoint",
                        name="name",
            
                        # the properties below are optional
                        description="description",
                        enable_webhook_updates=False
                    ),
                    mcp_server_new_relic=devopsagent.CfnAssociation.MCPServerNewRelicConfigurationProperty(
                        account_id="accountId",
                        endpoint="endpoint"
                    ),
                    mcp_server_splunk=devopsagent.CfnAssociation.MCPServerSplunkConfigurationProperty(
                        endpoint="endpoint",
                        name="name",
            
                        # the properties below are optional
                        description="description",
                        enable_webhook_updates=False
                    ),
                    service_now=devopsagent.CfnAssociation.ServiceNowConfigurationProperty(
                        enable_webhook_updates=False,
                        instance_id="instanceId"
                    ),
                    slack=devopsagent.CfnAssociation.SlackConfigurationProperty(
                        transmission_target=devopsagent.CfnAssociation.SlackTransmissionTargetProperty(
                            incident_response_target=devopsagent.CfnAssociation.SlackChannelProperty(
                                channel_id="channelId",
            
                                # the properties below are optional
                                channel_name="channelName"
                            )
                        ),
                        workspace_id="workspaceId",
                        workspace_name="workspaceName"
                    ),
                    source_aws=devopsagent.CfnAssociation.SourceAwsConfigurationProperty(
                        account_id="accountId",
                        account_type="accountType",
                        assumable_role_arn="assumableRoleArn",
            
                        # the properties below are optional
                        resources=[devopsagent.CfnAssociation.AWSResourceProperty(
                            resource_arn="resourceArn",
            
                            # the properties below are optional
                            resource_metadata=resource_metadata,
                            resource_type="resourceType"
                        )],
                        tags=[devopsagent.CfnAssociation.KeyValuePairProperty(
                            key="key",
                            value="value"
                        )]
                    )
                ),
                service_id="serviceId",
            
                # the properties below are optional
                linked_association_ids=["linkedAssociationIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9c7866e61a4a7267964c2e97d2c2f23071408ae1546eca41521d60b1273549)
            check_type(argname="argument agent_space_id", value=agent_space_id, expected_type=type_hints["agent_space_id"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument linked_association_ids", value=linked_association_ids, expected_type=type_hints["linked_association_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_space_id": agent_space_id,
            "configuration": configuration,
            "service_id": service_id,
        }
        if linked_association_ids is not None:
            self._values["linked_association_ids"] = linked_association_ids

    @builtins.property
    def agent_space_id(self) -> builtins.str:
        '''The unique identifier of the Agent Space.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html#cfn-devopsagent-association-agentspaceid
        '''
        result = self._values.get("agent_space_id")
        assert result is not None, "Required property 'agent_space_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Union["_IResolvable_da3f097b", "CfnAssociation.ServiceConfigurationProperty"]:
        '''The configuration that directs how the Agent Space interacts with the given service.

        You can specify only one configuration type per association.

        *Allowed Values* : ``SourceAws`` | ``Aws`` | ``GitHub`` | ``GitLab`` | ``Slack`` | ``Dynatrace`` | ``ServiceNow`` | ``MCPServer`` | ``MCPServerNewRelic`` | ``MCPServerDatadog`` | ``MCPServerSplunk`` | ``EventChannel``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html#cfn-devopsagent-association-configuration
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(typing.Union["_IResolvable_da3f097b", "CfnAssociation.ServiceConfigurationProperty"], result)

    @builtins.property
    def service_id(self) -> builtins.str:
        '''The identifier for the associated service.

        For ``SourceAws`` and ``Aws`` configurations, this must be ``aws`` . For all other service types, this is a UUID generated from the RegisterService command.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html#cfn-devopsagent-association-serviceid
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def linked_association_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of linked association IDs for parent-child relationships.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsagent-association.html#cfn-devopsagent-association-linkedassociationids
        '''
        result = self._values.get("linked_association_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAgentSpace",
    "CfnAgentSpaceProps",
    "CfnAssociation",
    "CfnAssociationProps",
]

publication.publish()

def _typecheckingstub__3897cdc52c2bc2a74bdd32702e32905947b3c0fc36798edcdac7875cc9939456(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fd19a72161f0ef8cc6732b6e9205e1c9f41b50d57a659a84461dcdde223423(
    resource: _IAgentSpaceRef_2ffb48ed,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b6182298920242aa320928b58b0b5bc6ee7fe37ab398df5dd8f138f81638f6(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c3714a879ff931c53d9540f49cb04b7551032f6754505380b7064cbcb7719f(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca7931f7e8a8dc031f895c3bf121e4253f0443d5d02865c48e259d41303518b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e1593c483d80afbaaf07c646b5d5ede131e360f81f0dde9fa486f5c749e58f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7561d8cdcaf93c81d1cf0a9a4cc5790c03232e494d49db5171a93599b8f575(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea00a21cf40eafce14a4e6e1a4cd3e9f843a2f2e416299a20a2159ce8cdb6d5f(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9507e77277cf05febf82ccf8829d008e3d5bca6bfbb5c229a629346a34d445ff(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent_space_id: builtins.str,
    configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.ServiceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    service_id: builtins.str,
    linked_association_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cae44481f5807f4bcf3fcf5d08b660423111da523b22ba60bcaacf43a50aa9(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd21b036854f8ed65af7b88356ee2787b8f2fb60324e8b7f39b6edf4992ce967(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0d4a7651eb08ad3bc11db7886a5718c26e72c5b665acd6183227b87adf00e4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac4f12f5965b47ff3162eacbbbebb04e5d1595483e00e0e29ace1cd733b8156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b224d34e655755660b3f83f1ef3ad78de31336ef41e61cf24dfb47a3d5e00b96(
    value: typing.Union[_IResolvable_da3f097b, CfnAssociation.ServiceConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d88d472b1933bfd27859b1b634111a6667c50bedacee3234cfc98a8a05797a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a926a8cb577bf81233b764232f042b444bc6a9e989283355f36b9faf248fe46(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1d632ade69849147b75fe20e7412c90e54c9e84dafe76046f35e5fa880436f(
    *,
    account_id: builtins.str,
    account_type: builtins.str,
    assumable_role_arn: builtins.str,
    resources: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.AWSResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnAssociation.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83865c7f5f4d4caa82576ab7efaac17f6225904d0ac52970333a1906f6ed0cb(
    *,
    resource_arn: builtins.str,
    resource_metadata: typing.Any = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af533dc830c7a5f8fd17b5170cecf1e7dd483fe076400d57927aca27831a0ca8(
    *,
    env_id: builtins.str,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d900735d86a3a2a681d9eba7f3ce7754e8cdfbc47df16370253e165583cd41(
    *,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52e2bfd74e3e041299304fca2e11acf7c77935cb3d81768bd90034e89f0c1f3(
    *,
    owner: builtins.str,
    owner_type: builtins.str,
    repo_id: builtins.str,
    repo_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0bf76d18d2da5c1a7b65fd908fdd6aa4ca798335d0ef9f07ec4c064ccb5241(
    *,
    project_id: builtins.str,
    project_path: builtins.str,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    instance_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded74f7f3af261fdfeb1ca20f0589b46cd28465b569b567f86c794c6d2010df2(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d8de94964f9d444ce60e60c71a8386873d9d717628a8b450e0463922b08600(
    *,
    endpoint: builtins.str,
    name: builtins.str,
    tools: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bdd66d2ae6508b6fa75de77b1b7bd044d6bf7b9e0c60cb573f57ca7faa1817(
    *,
    endpoint: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60c2241968bd47959618d5fef16076f92aa6b8c2e1932e3d7d5e3983c4108a8(
    *,
    account_id: builtins.str,
    endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5251bb56068759277d9b99b06c4d20b0e0434473774eeb3d825f9ed5301ba970(
    *,
    endpoint: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534ff66bec4c3f764380e71fc8dbccb3b6b0319f301032fa7e975aa1842a74e1(
    *,
    aws: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.AWSConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynatrace: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.DynatraceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_channel: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.EventChannelConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    git_hub: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.GitHubConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    git_lab: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.GitLabConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.MCPServerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server_datadog: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.MCPServerDatadogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server_new_relic: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.MCPServerNewRelicConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mcp_server_splunk: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.MCPServerSplunkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.ServiceNowConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slack: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.SlackConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_aws: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.SourceAwsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9767ae84f8f9ac8fbffe3c19d1ac1dc61d581770deb87d97b058eb73cc671511(
    *,
    enable_webhook_updates: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cf6d0fee94466c60ffb3cbfb9f571fb9f69201085fc5de6cd2f0d6e4b8d633(
    *,
    channel_id: builtins.str,
    channel_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28eb759dbeb853e46c5ba811aba401a06c7b87554a3bac255792e3d13c3f0c23(
    *,
    transmission_target: typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.SlackTransmissionTargetProperty, typing.Dict[builtins.str, typing.Any]]],
    workspace_id: builtins.str,
    workspace_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4224928b94c6f3a7e8aeb21f4d921f668ae91ec705e4026d010b1813687b20c5(
    *,
    incident_response_target: typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.SlackChannelProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f309a9bf78a2704dbd1fd90dfdf8ff7ac7091cdb4572312fad3281cfcbd5ac(
    *,
    account_id: builtins.str,
    account_type: builtins.str,
    assumable_role_arn: builtins.str,
    resources: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.AWSResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnAssociation.KeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9c7866e61a4a7267964c2e97d2c2f23071408ae1546eca41521d60b1273549(
    *,
    agent_space_id: builtins.str,
    configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnAssociation.ServiceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    service_id: builtins.str,
    linked_association_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
