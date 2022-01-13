
from typing import Generic, TypeVar, cast, overload

T = TypeVar("T")
class Collection(Generic[T], dict[str, T]):
    @overload
    def __init__(self, dict: dict[str, T]):
        ...

    @overload
    def __init__(self):
        ...

    def __init__(self, dict: dict[str, T] = {}):
        self.update(__collection__=cast(T, True))
        self.update(dict)