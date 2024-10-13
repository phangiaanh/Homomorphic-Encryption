from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EncryptedData(_message.Message):
    __slots__ = ("polynomials0", "polynomials1")
    POLYNOMIALS0_FIELD_NUMBER: _ClassVar[int]
    POLYNOMIALS1_FIELD_NUMBER: _ClassVar[int]
    polynomials0: _containers.RepeatedScalarFieldContainer[int]
    polynomials1: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, polynomials0: _Optional[_Iterable[int]] = ..., polynomials1: _Optional[_Iterable[int]] = ...) -> None: ...

class ComputationRequest(_message.Message):
    __slots__ = ("data_array", "operation", "relinearization0", "relinearization1")
    DATA_ARRAY_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    RELINEARIZATION0_FIELD_NUMBER: _ClassVar[int]
    RELINEARIZATION1_FIELD_NUMBER: _ClassVar[int]
    data_array: _containers.RepeatedCompositeFieldContainer[EncryptedData]
    operation: str
    relinearization0: _containers.RepeatedCompositeFieldContainer[ItemArray]
    relinearization1: _containers.RepeatedCompositeFieldContainer[ItemArray]
    def __init__(self, data_array: _Optional[_Iterable[_Union[EncryptedData, _Mapping]]] = ..., operation: _Optional[str] = ..., relinearization0: _Optional[_Iterable[_Union[ItemArray, _Mapping]]] = ..., relinearization1: _Optional[_Iterable[_Union[ItemArray, _Mapping]]] = ...) -> None: ...

class ItemArray(_message.Message):
    __slots__ = ("item",)
    ITEM_FIELD_NUMBER: _ClassVar[int]
    item: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, item: _Optional[_Iterable[int]] = ...) -> None: ...

class ComputationResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EncryptedData
    def __init__(self, result: _Optional[_Union[EncryptedData, _Mapping]] = ...) -> None: ...
