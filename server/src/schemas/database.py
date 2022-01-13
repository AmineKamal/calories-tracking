from typing import TypedDict
from src.schemas.collection import Collection
from src.schemas.user import IUser

class IDatabase(TypedDict):
    total_user_count: int
    users: Collection[IUser]
    secret: str
