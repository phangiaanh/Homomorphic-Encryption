from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ComputationRequest(_message.Message):
    __slots__ = ("data_array", "operation", "evaluation_key")
    DATA_ARRAY_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_KEY_FIELD_NUMBER: _ClassVar[int]
    data_array: _containers.RepeatedScalarFieldContainer[str]
    operation: str
    evaluation_key: str
    def __init__(self, data_array: _Optional[_Iterable[str]] = ..., operation: _Optional[str] = ..., evaluation_key: _Optional[str] = ...) -> None: ...

class ComputationResponse(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
