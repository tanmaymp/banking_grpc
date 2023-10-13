from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BankRequest(_message.Message):
    __slots__ = ["id", "type", "interface", "money", "balance"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: str
    interface: str
    money: int
    balance: int
    def __init__(self, id: _Optional[int] = ..., type: _Optional[str] = ..., interface: _Optional[str] = ..., money: _Optional[int] = ..., balance: _Optional[int] = ...) -> None: ...

class BankResponse(_message.Message):
    __slots__ = ["interface", "result", "balance"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    interface: str
    result: str
    balance: int
    def __init__(self, interface: _Optional[str] = ..., result: _Optional[str] = ..., balance: _Optional[int] = ...) -> None: ...
