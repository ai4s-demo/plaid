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


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_emrcontainers.IVirtualClusterRef"
)
class IVirtualClusterRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a VirtualCluster.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="virtualClusterRef")
    def virtual_cluster_ref(self) -> "VirtualClusterReference":
        '''(experimental) A reference to a VirtualCluster resource.

        :stability: experimental
        '''
        ...


class _IVirtualClusterRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a VirtualCluster.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_emrcontainers.IVirtualClusterRef"

    @builtins.property
    @jsii.member(jsii_name="virtualClusterRef")
    def virtual_cluster_ref(self) -> "VirtualClusterReference":
        '''(experimental) A reference to a VirtualCluster resource.

        :stability: experimental
        '''
        return typing.cast("VirtualClusterReference", jsii.get(self, "virtualClusterRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVirtualClusterRef).__jsii_proxy_class__ = lambda : _IVirtualClusterRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_emrcontainers.VirtualClusterReference",
    jsii_struct_bases=[],
    name_mapping={
        "virtual_cluster_arn": "virtualClusterArn",
        "virtual_cluster_id": "virtualClusterId",
    },
)
class VirtualClusterReference:
    def __init__(
        self,
        *,
        virtual_cluster_arn: builtins.str,
        virtual_cluster_id: builtins.str,
    ) -> None:
        '''A reference to a VirtualCluster resource.

        :param virtual_cluster_arn: The ARN of the VirtualCluster resource.
        :param virtual_cluster_id: The Id of the VirtualCluster resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_emrcontainers as interfaces_emrcontainers
            
            virtual_cluster_reference = interfaces_emrcontainers.VirtualClusterReference(
                virtual_cluster_arn="virtualClusterArn",
                virtual_cluster_id="virtualClusterId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b279f868e31527e514f6d252f42aa76ae779c333792720eb24ad65b2884b2923)
            check_type(argname="argument virtual_cluster_arn", value=virtual_cluster_arn, expected_type=type_hints["virtual_cluster_arn"])
            check_type(argname="argument virtual_cluster_id", value=virtual_cluster_id, expected_type=type_hints["virtual_cluster_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_cluster_arn": virtual_cluster_arn,
            "virtual_cluster_id": virtual_cluster_id,
        }

    @builtins.property
    def virtual_cluster_arn(self) -> builtins.str:
        '''The ARN of the VirtualCluster resource.'''
        result = self._values.get("virtual_cluster_arn")
        assert result is not None, "Required property 'virtual_cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_cluster_id(self) -> builtins.str:
        '''The Id of the VirtualCluster resource.'''
        result = self._values.get("virtual_cluster_id")
        assert result is not None, "Required property 'virtual_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualClusterReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IVirtualClusterRef",
    "VirtualClusterReference",
]

publication.publish()

def _typecheckingstub__b279f868e31527e514f6d252f42aa76ae779c333792720eb24ad65b2884b2923(
    *,
    virtual_cluster_arn: builtins.str,
    virtual_cluster_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IVirtualClusterRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
