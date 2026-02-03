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

from ..._jsii import *

import constructs as _constructs_77d1e7e8
from .. import IEnvironmentAware as _IEnvironmentAware_f39049ee


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.BrowserCustomReference",
    jsii_struct_bases=[],
    name_mapping={"browser_arn": "browserArn", "browser_id": "browserId"},
)
class BrowserCustomReference:
    def __init__(self, *, browser_arn: builtins.str, browser_id: builtins.str) -> None:
        '''A reference to a BrowserCustom resource.

        :param browser_arn: The ARN of the BrowserCustom resource.
        :param browser_id: The BrowserId of the BrowserCustom resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_bedrockagentcore as interfaces_bedrockagentcore
            
            browser_custom_reference = interfaces_bedrockagentcore.BrowserCustomReference(
                browser_arn="browserArn",
                browser_id="browserId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d539b77517d652d5c6fba79e5a649664ea046fd158b0c2a9c0c103e93f28a2)
            check_type(argname="argument browser_arn", value=browser_arn, expected_type=type_hints["browser_arn"])
            check_type(argname="argument browser_id", value=browser_id, expected_type=type_hints["browser_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "browser_arn": browser_arn,
            "browser_id": browser_id,
        }

    @builtins.property
    def browser_arn(self) -> builtins.str:
        '''The ARN of the BrowserCustom resource.'''
        result = self._values.get("browser_arn")
        assert result is not None, "Required property 'browser_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def browser_id(self) -> builtins.str:
        '''The BrowserId of the BrowserCustom resource.'''
        result = self._values.get("browser_id")
        assert result is not None, "Required property 'browser_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BrowserCustomReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.CodeInterpreterCustomReference",
    jsii_struct_bases=[],
    name_mapping={
        "code_interpreter_arn": "codeInterpreterArn",
        "code_interpreter_id": "codeInterpreterId",
    },
)
class CodeInterpreterCustomReference:
    def __init__(
        self,
        *,
        code_interpreter_arn: builtins.str,
        code_interpreter_id: builtins.str,
    ) -> None:
        '''A reference to a CodeInterpreterCustom resource.

        :param code_interpreter_arn: The ARN of the CodeInterpreterCustom resource.
        :param code_interpreter_id: The CodeInterpreterId of the CodeInterpreterCustom resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_bedrockagentcore as interfaces_bedrockagentcore
            
            code_interpreter_custom_reference = interfaces_bedrockagentcore.CodeInterpreterCustomReference(
                code_interpreter_arn="codeInterpreterArn",
                code_interpreter_id="codeInterpreterId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31803efaee1e805b6555da7f5c0c2c409540346b67d7cb412b9f78fbe7b6198d)
            check_type(argname="argument code_interpreter_arn", value=code_interpreter_arn, expected_type=type_hints["code_interpreter_arn"])
            check_type(argname="argument code_interpreter_id", value=code_interpreter_id, expected_type=type_hints["code_interpreter_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code_interpreter_arn": code_interpreter_arn,
            "code_interpreter_id": code_interpreter_id,
        }

    @builtins.property
    def code_interpreter_arn(self) -> builtins.str:
        '''The ARN of the CodeInterpreterCustom resource.'''
        result = self._values.get("code_interpreter_arn")
        assert result is not None, "Required property 'code_interpreter_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code_interpreter_id(self) -> builtins.str:
        '''The CodeInterpreterId of the CodeInterpreterCustom resource.'''
        result = self._values.get("code_interpreter_id")
        assert result is not None, "Required property 'code_interpreter_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeInterpreterCustomReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.GatewayReference",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_arn": "gatewayArn",
        "gateway_identifier": "gatewayIdentifier",
    },
)
class GatewayReference:
    def __init__(
        self,
        *,
        gateway_arn: builtins.str,
        gateway_identifier: builtins.str,
    ) -> None:
        '''A reference to a Gateway resource.

        :param gateway_arn: The ARN of the Gateway resource.
        :param gateway_identifier: The GatewayIdentifier of the Gateway resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_bedrockagentcore as interfaces_bedrockagentcore
            
            gateway_reference = interfaces_bedrockagentcore.GatewayReference(
                gateway_arn="gatewayArn",
                gateway_identifier="gatewayIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d4b1089724a6b1cb8eaa1115a2c124f0d3516237c16f992947cb2b890de904)
            check_type(argname="argument gateway_arn", value=gateway_arn, expected_type=type_hints["gateway_arn"])
            check_type(argname="argument gateway_identifier", value=gateway_identifier, expected_type=type_hints["gateway_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_arn": gateway_arn,
            "gateway_identifier": gateway_identifier,
        }

    @builtins.property
    def gateway_arn(self) -> builtins.str:
        '''The ARN of the Gateway resource.'''
        result = self._values.get("gateway_arn")
        assert result is not None, "Required property 'gateway_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gateway_identifier(self) -> builtins.str:
        '''The GatewayIdentifier of the Gateway resource.'''
        result = self._values.get("gateway_identifier")
        assert result is not None, "Required property 'gateway_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GatewayReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.GatewayTargetReference",
    jsii_struct_bases=[],
    name_mapping={"gateway_identifier": "gatewayIdentifier", "target_id": "targetId"},
)
class GatewayTargetReference:
    def __init__(
        self,
        *,
        gateway_identifier: builtins.str,
        target_id: builtins.str,
    ) -> None:
        '''A reference to a GatewayTarget resource.

        :param gateway_identifier: The GatewayIdentifier of the GatewayTarget resource.
        :param target_id: The TargetId of the GatewayTarget resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_bedrockagentcore as interfaces_bedrockagentcore
            
            gateway_target_reference = interfaces_bedrockagentcore.GatewayTargetReference(
                gateway_identifier="gatewayIdentifier",
                target_id="targetId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c5b43c2a90eb380f924dad8dc36cab52c5988b4f78c98aa489c624cec4200d)
            check_type(argname="argument gateway_identifier", value=gateway_identifier, expected_type=type_hints["gateway_identifier"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_identifier": gateway_identifier,
            "target_id": target_id,
        }

    @builtins.property
    def gateway_identifier(self) -> builtins.str:
        '''The GatewayIdentifier of the GatewayTarget resource.'''
        result = self._values.get("gateway_identifier")
        assert result is not None, "Required property 'gateway_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_id(self) -> builtins.str:
        '''The TargetId of the GatewayTarget resource.'''
        result = self._values.get("target_id")
        assert result is not None, "Required property 'target_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GatewayTargetReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.IBrowserCustomRef"
)
class IBrowserCustomRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a BrowserCustom.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="browserCustomRef")
    def browser_custom_ref(self) -> "BrowserCustomReference":
        '''(experimental) A reference to a BrowserCustom resource.

        :stability: experimental
        '''
        ...


class _IBrowserCustomRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a BrowserCustom.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_bedrockagentcore.IBrowserCustomRef"

    @builtins.property
    @jsii.member(jsii_name="browserCustomRef")
    def browser_custom_ref(self) -> "BrowserCustomReference":
        '''(experimental) A reference to a BrowserCustom resource.

        :stability: experimental
        '''
        return typing.cast("BrowserCustomReference", jsii.get(self, "browserCustomRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBrowserCustomRef).__jsii_proxy_class__ = lambda : _IBrowserCustomRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.ICodeInterpreterCustomRef"
)
class ICodeInterpreterCustomRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a CodeInterpreterCustom.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="codeInterpreterCustomRef")
    def code_interpreter_custom_ref(self) -> "CodeInterpreterCustomReference":
        '''(experimental) A reference to a CodeInterpreterCustom resource.

        :stability: experimental
        '''
        ...


class _ICodeInterpreterCustomRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a CodeInterpreterCustom.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_bedrockagentcore.ICodeInterpreterCustomRef"

    @builtins.property
    @jsii.member(jsii_name="codeInterpreterCustomRef")
    def code_interpreter_custom_ref(self) -> "CodeInterpreterCustomReference":
        '''(experimental) A reference to a CodeInterpreterCustom resource.

        :stability: experimental
        '''
        return typing.cast("CodeInterpreterCustomReference", jsii.get(self, "codeInterpreterCustomRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICodeInterpreterCustomRef).__jsii_proxy_class__ = lambda : _ICodeInterpreterCustomRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.IGatewayRef")
class IGatewayRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Gateway.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="gatewayRef")
    def gateway_ref(self) -> "GatewayReference":
        '''(experimental) A reference to a Gateway resource.

        :stability: experimental
        '''
        ...


class _IGatewayRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Gateway.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_bedrockagentcore.IGatewayRef"

    @builtins.property
    @jsii.member(jsii_name="gatewayRef")
    def gateway_ref(self) -> "GatewayReference":
        '''(experimental) A reference to a Gateway resource.

        :stability: experimental
        '''
        return typing.cast("GatewayReference", jsii.get(self, "gatewayRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGatewayRef).__jsii_proxy_class__ = lambda : _IGatewayRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.IGatewayTargetRef"
)
class IGatewayTargetRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a GatewayTarget.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="gatewayTargetRef")
    def gateway_target_ref(self) -> "GatewayTargetReference":
        '''(experimental) A reference to a GatewayTarget resource.

        :stability: experimental
        '''
        ...


class _IGatewayTargetRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a GatewayTarget.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_bedrockagentcore.IGatewayTargetRef"

    @builtins.property
    @jsii.member(jsii_name="gatewayTargetRef")
    def gateway_target_ref(self) -> "GatewayTargetReference":
        '''(experimental) A reference to a GatewayTarget resource.

        :stability: experimental
        '''
        return typing.cast("GatewayTargetReference", jsii.get(self, "gatewayTargetRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGatewayTargetRef).__jsii_proxy_class__ = lambda : _IGatewayTargetRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.IMemoryRef")
class IMemoryRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Memory.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="memoryRef")
    def memory_ref(self) -> "MemoryReference":
        '''(experimental) A reference to a Memory resource.

        :stability: experimental
        '''
        ...


class _IMemoryRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Memory.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_bedrockagentcore.IMemoryRef"

    @builtins.property
    @jsii.member(jsii_name="memoryRef")
    def memory_ref(self) -> "MemoryReference":
        '''(experimental) A reference to a Memory resource.

        :stability: experimental
        '''
        return typing.cast("MemoryReference", jsii.get(self, "memoryRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMemoryRef).__jsii_proxy_class__ = lambda : _IMemoryRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.IRuntimeEndpointRef"
)
class IRuntimeEndpointRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a RuntimeEndpoint.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="runtimeEndpointRef")
    def runtime_endpoint_ref(self) -> "RuntimeEndpointReference":
        '''(experimental) A reference to a RuntimeEndpoint resource.

        :stability: experimental
        '''
        ...


class _IRuntimeEndpointRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a RuntimeEndpoint.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_bedrockagentcore.IRuntimeEndpointRef"

    @builtins.property
    @jsii.member(jsii_name="runtimeEndpointRef")
    def runtime_endpoint_ref(self) -> "RuntimeEndpointReference":
        '''(experimental) A reference to a RuntimeEndpoint resource.

        :stability: experimental
        '''
        return typing.cast("RuntimeEndpointReference", jsii.get(self, "runtimeEndpointRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuntimeEndpointRef).__jsii_proxy_class__ = lambda : _IRuntimeEndpointRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.IRuntimeRef")
class IRuntimeRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Runtime.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="runtimeRef")
    def runtime_ref(self) -> "RuntimeReference":
        '''(experimental) A reference to a Runtime resource.

        :stability: experimental
        '''
        ...


class _IRuntimeRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Runtime.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_bedrockagentcore.IRuntimeRef"

    @builtins.property
    @jsii.member(jsii_name="runtimeRef")
    def runtime_ref(self) -> "RuntimeReference":
        '''(experimental) A reference to a Runtime resource.

        :stability: experimental
        '''
        return typing.cast("RuntimeReference", jsii.get(self, "runtimeRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuntimeRef).__jsii_proxy_class__ = lambda : _IRuntimeRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.IWorkloadIdentityRef"
)
class IWorkloadIdentityRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a WorkloadIdentity.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityRef")
    def workload_identity_ref(self) -> "WorkloadIdentityReference":
        '''(experimental) A reference to a WorkloadIdentity resource.

        :stability: experimental
        '''
        ...


class _IWorkloadIdentityRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a WorkloadIdentity.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_bedrockagentcore.IWorkloadIdentityRef"

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityRef")
    def workload_identity_ref(self) -> "WorkloadIdentityReference":
        '''(experimental) A reference to a WorkloadIdentity resource.

        :stability: experimental
        '''
        return typing.cast("WorkloadIdentityReference", jsii.get(self, "workloadIdentityRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IWorkloadIdentityRef).__jsii_proxy_class__ = lambda : _IWorkloadIdentityRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.MemoryReference",
    jsii_struct_bases=[],
    name_mapping={"memory_arn": "memoryArn"},
)
class MemoryReference:
    def __init__(self, *, memory_arn: builtins.str) -> None:
        '''A reference to a Memory resource.

        :param memory_arn: The MemoryArn of the Memory resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_bedrockagentcore as interfaces_bedrockagentcore
            
            memory_reference = interfaces_bedrockagentcore.MemoryReference(
                memory_arn="memoryArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87b5beb1d0be1ca0ef1075ebb74f73e86e27b1cb381596715a5727c06212f54)
            check_type(argname="argument memory_arn", value=memory_arn, expected_type=type_hints["memory_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "memory_arn": memory_arn,
        }

    @builtins.property
    def memory_arn(self) -> builtins.str:
        '''The MemoryArn of the Memory resource.'''
        result = self._values.get("memory_arn")
        assert result is not None, "Required property 'memory_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemoryReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.RuntimeEndpointReference",
    jsii_struct_bases=[],
    name_mapping={"agent_runtime_endpoint_arn": "agentRuntimeEndpointArn"},
)
class RuntimeEndpointReference:
    def __init__(self, *, agent_runtime_endpoint_arn: builtins.str) -> None:
        '''A reference to a RuntimeEndpoint resource.

        :param agent_runtime_endpoint_arn: The AgentRuntimeEndpointArn of the RuntimeEndpoint resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_bedrockagentcore as interfaces_bedrockagentcore
            
            runtime_endpoint_reference = interfaces_bedrockagentcore.RuntimeEndpointReference(
                agent_runtime_endpoint_arn="agentRuntimeEndpointArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f731eb99d3edd4594a77aea4dc91d39b42d1521809385fa10f06922fbc1c08)
            check_type(argname="argument agent_runtime_endpoint_arn", value=agent_runtime_endpoint_arn, expected_type=type_hints["agent_runtime_endpoint_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_runtime_endpoint_arn": agent_runtime_endpoint_arn,
        }

    @builtins.property
    def agent_runtime_endpoint_arn(self) -> builtins.str:
        '''The AgentRuntimeEndpointArn of the RuntimeEndpoint resource.'''
        result = self._values.get("agent_runtime_endpoint_arn")
        assert result is not None, "Required property 'agent_runtime_endpoint_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuntimeEndpointReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.RuntimeReference",
    jsii_struct_bases=[],
    name_mapping={
        "agent_runtime_arn": "agentRuntimeArn",
        "agent_runtime_id": "agentRuntimeId",
    },
)
class RuntimeReference:
    def __init__(
        self,
        *,
        agent_runtime_arn: builtins.str,
        agent_runtime_id: builtins.str,
    ) -> None:
        '''A reference to a Runtime resource.

        :param agent_runtime_arn: The ARN of the Runtime resource.
        :param agent_runtime_id: The AgentRuntimeId of the Runtime resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_bedrockagentcore as interfaces_bedrockagentcore
            
            runtime_reference = interfaces_bedrockagentcore.RuntimeReference(
                agent_runtime_arn="agentRuntimeArn",
                agent_runtime_id="agentRuntimeId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1435ab047fbb10ad1262aabe5dcc3598ed76fcfee17487287cbf9bfe742cb8a)
            check_type(argname="argument agent_runtime_arn", value=agent_runtime_arn, expected_type=type_hints["agent_runtime_arn"])
            check_type(argname="argument agent_runtime_id", value=agent_runtime_id, expected_type=type_hints["agent_runtime_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_runtime_arn": agent_runtime_arn,
            "agent_runtime_id": agent_runtime_id,
        }

    @builtins.property
    def agent_runtime_arn(self) -> builtins.str:
        '''The ARN of the Runtime resource.'''
        result = self._values.get("agent_runtime_arn")
        assert result is not None, "Required property 'agent_runtime_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_runtime_id(self) -> builtins.str:
        '''The AgentRuntimeId of the Runtime resource.'''
        result = self._values.get("agent_runtime_id")
        assert result is not None, "Required property 'agent_runtime_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuntimeReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_bedrockagentcore.WorkloadIdentityReference",
    jsii_struct_bases=[],
    name_mapping={
        "workload_identity_arn": "workloadIdentityArn",
        "workload_identity_name": "workloadIdentityName",
    },
)
class WorkloadIdentityReference:
    def __init__(
        self,
        *,
        workload_identity_arn: builtins.str,
        workload_identity_name: builtins.str,
    ) -> None:
        '''A reference to a WorkloadIdentity resource.

        :param workload_identity_arn: The ARN of the WorkloadIdentity resource.
        :param workload_identity_name: The Name of the WorkloadIdentity resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_bedrockagentcore as interfaces_bedrockagentcore
            
            workload_identity_reference = interfaces_bedrockagentcore.WorkloadIdentityReference(
                workload_identity_arn="workloadIdentityArn",
                workload_identity_name="workloadIdentityName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c87d0628ada636c999bb25ecf8067b788ff440bac34ff64b11d374db18dc71)
            check_type(argname="argument workload_identity_arn", value=workload_identity_arn, expected_type=type_hints["workload_identity_arn"])
            check_type(argname="argument workload_identity_name", value=workload_identity_name, expected_type=type_hints["workload_identity_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "workload_identity_arn": workload_identity_arn,
            "workload_identity_name": workload_identity_name,
        }

    @builtins.property
    def workload_identity_arn(self) -> builtins.str:
        '''The ARN of the WorkloadIdentity resource.'''
        result = self._values.get("workload_identity_arn")
        assert result is not None, "Required property 'workload_identity_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workload_identity_name(self) -> builtins.str:
        '''The Name of the WorkloadIdentity resource.'''
        result = self._values.get("workload_identity_name")
        assert result is not None, "Required property 'workload_identity_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadIdentityReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BrowserCustomReference",
    "CodeInterpreterCustomReference",
    "GatewayReference",
    "GatewayTargetReference",
    "IBrowserCustomRef",
    "ICodeInterpreterCustomRef",
    "IGatewayRef",
    "IGatewayTargetRef",
    "IMemoryRef",
    "IRuntimeEndpointRef",
    "IRuntimeRef",
    "IWorkloadIdentityRef",
    "MemoryReference",
    "RuntimeEndpointReference",
    "RuntimeReference",
    "WorkloadIdentityReference",
]

publication.publish()

def _typecheckingstub__30d539b77517d652d5c6fba79e5a649664ea046fd158b0c2a9c0c103e93f28a2(
    *,
    browser_arn: builtins.str,
    browser_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31803efaee1e805b6555da7f5c0c2c409540346b67d7cb412b9f78fbe7b6198d(
    *,
    code_interpreter_arn: builtins.str,
    code_interpreter_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d4b1089724a6b1cb8eaa1115a2c124f0d3516237c16f992947cb2b890de904(
    *,
    gateway_arn: builtins.str,
    gateway_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c5b43c2a90eb380f924dad8dc36cab52c5988b4f78c98aa489c624cec4200d(
    *,
    gateway_identifier: builtins.str,
    target_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87b5beb1d0be1ca0ef1075ebb74f73e86e27b1cb381596715a5727c06212f54(
    *,
    memory_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f731eb99d3edd4594a77aea4dc91d39b42d1521809385fa10f06922fbc1c08(
    *,
    agent_runtime_endpoint_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1435ab047fbb10ad1262aabe5dcc3598ed76fcfee17487287cbf9bfe742cb8a(
    *,
    agent_runtime_arn: builtins.str,
    agent_runtime_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c87d0628ada636c999bb25ecf8067b788ff440bac34ff64b11d374db18dc71(
    *,
    workload_identity_arn: builtins.str,
    workload_identity_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IBrowserCustomRef, ICodeInterpreterCustomRef, IGatewayRef, IGatewayTargetRef, IMemoryRef, IRuntimeEndpointRef, IRuntimeRef, IWorkloadIdentityRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
