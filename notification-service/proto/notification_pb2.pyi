from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmailType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMAIL_TYPE_UNSPECIFIED: _ClassVar[EmailType]
    EMAIL_TYPE_WELCOME: _ClassVar[EmailType]
    EMAIL_TYPE_PASSWORD_RESET: _ClassVar[EmailType]
    EMAIL_TYPE_VERIFY: _ClassVar[EmailType]
    EMAIL_TYPE_NOTIFICATION: _ClassVar[EmailType]
EMAIL_TYPE_UNSPECIFIED: EmailType
EMAIL_TYPE_WELCOME: EmailType
EMAIL_TYPE_PASSWORD_RESET: EmailType
EMAIL_TYPE_VERIFY: EmailType
EMAIL_TYPE_NOTIFICATION: EmailType

class SendEmailRequest(_message.Message):
    __slots__ = ("to", "type", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    to: str
    type: EmailType
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, to: _Optional[str] = ..., type: _Optional[_Union[EmailType, str]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SendEmailResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    def __init__(self, success: bool = ..., error: _Optional[str] = ...) -> None: ...
