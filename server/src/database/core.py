from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Optional, TypeVar, TypedDict, cast

NodeDict = TypeVar("NodeDict", bound=TypedDict)
class DatabaseNode(Generic[NodeDict], ABC):
    def __init__(self) -> None:
        self.__parent: Optional['DatabaseNode[Any]'] = None

    def link(self, parent: 'DatabaseNode[Any]'):
        self.__parent = parent
        return self

    def update(self):
        if (self.__parent):
            self.__parent.update()
    
    @abstractmethod
    def serialize(self) -> NodeDict:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(dict: NodeDict) -> 'DatabaseNode[NodeDict]':
        pass

DatabaseNodeMethod = TypeVar('DatabaseNodeMethod', bound=Callable[..., Any])
def update_parent(func: DatabaseNodeMethod) -> DatabaseNodeMethod:
    def wrapper(*args: Any, **kwargs: Any):
        res = func(*args, **kwargs)
        
        if hasattr(args[0], "update") and callable(getattr(args[0], "update")):
            args[0].update()

        return res

    return cast(DatabaseNodeMethod, wrapper)