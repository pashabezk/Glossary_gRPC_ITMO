from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Term(_message.Message):
    __slots__ = ("term", "definition")
    TERM_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    term: str
    definition: str
    def __init__(self, term: _Optional[str] = ..., definition: _Optional[str] = ...) -> None: ...

class TermRequest(_message.Message):
    __slots__ = ("term",)
    TERM_FIELD_NUMBER: _ClassVar[int]
    term: str
    def __init__(self, term: _Optional[str] = ...) -> None: ...

class AddTermRequest(_message.Message):
    __slots__ = ("term", "definition")
    TERM_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    term: str
    definition: str
    def __init__(self, term: _Optional[str] = ..., definition: _Optional[str] = ...) -> None: ...

class UpdateTermRequest(_message.Message):
    __slots__ = ("term", "new_definition")
    TERM_FIELD_NUMBER: _ClassVar[int]
    NEW_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    term: str
    new_definition: str
    def __init__(self, term: _Optional[str] = ..., new_definition: _Optional[str] = ...) -> None: ...

class TermList(_message.Message):
    __slots__ = ("terms",)
    TERMS_FIELD_NUMBER: _ClassVar[int]
    terms: _containers.RepeatedCompositeFieldContainer[Term]
    def __init__(self, terms: _Optional[_Iterable[_Union[Term, _Mapping]]] = ...) -> None: ...
