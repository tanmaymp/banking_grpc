from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BankRequest(_message.Message):
    __slots__ = ["id", "eventid", "type", "interface", "money", "balance", "logclock", "event_tracker"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    LOGCLOCK_FIELD_NUMBER: _ClassVar[int]
    EVENT_TRACKER_FIELD_NUMBER: _ClassVar[int]
    id: int
    eventid: int
    type: str
    interface: str
    money: int
    balance: int
    logclock: int
    event_tracker: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., eventid: _Optional[int] = ..., type: _Optional[str] = ..., interface: _Optional[str] = ..., money: _Optional[int] = ..., balance: _Optional[int] = ..., logclock: _Optional[int] = ..., event_tracker: _Optional[_Iterable[int]] = ...) -> None: ...

class BankResponse(_message.Message):
    __slots__ = ["interface", "result", "balance", "logclock", "branch_id"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    LOGCLOCK_FIELD_NUMBER: _ClassVar[int]
    BRANCH_ID_FIELD_NUMBER: _ClassVar[int]
    interface: str
    result: str
    balance: int
    logclock: int
    branch_id: int
    def __init__(self, interface: _Optional[str] = ..., result: _Optional[str] = ..., balance: _Optional[int] = ..., logclock: _Optional[int] = ..., branch_id: _Optional[int] = ...) -> None: ...
