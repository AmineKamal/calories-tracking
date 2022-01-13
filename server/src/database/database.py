from typing import cast
from src.database.core import DatabaseNode, update_parent
from src.database.user import User
from src.schemas.collection import Collection
from src.schemas.database import IDatabase
import json
import os.path
import secrets

from src.schemas.user import IUser

default_database_dict: IDatabase = { 
    'users': Collection(),
    'total_user_count': 0,
    'secret': secrets.token_hex(32)
}

class Database(DatabaseNode[IDatabase]):
    def __init__(self, database: IDatabase = default_database_dict) -> None:
        super().__init__()
        self.initialize(database)
    
    def initialize(self, database: IDatabase):
        self.users: Collection[User] = Collection({ username: User.deserialize(user).link(self) if username != "__collection__" else cast(User, user) for username, user in database['users'].items() })
        self.total_user_count: int = database['total_user_count']
        self.secret: str = database['secret']

    @update_parent
    def add_user(self, user: User):
        user.id = self.total_user_count
        self.users[user.username] = user
        self.total_user_count += 1

    def update(self):
        self.save()

    def serialize(self) -> IDatabase:
        return {
            'users': Collection({ username: User.serialize(user) if username != "__collection__" else cast(IUser, user) for username, user in self.users.items() }),
            'total_user_count': self.total_user_count,
            'secret': self.secret
        }

    def save(self):
        with open('db.json', 'w') as json_file:
            json.dump(self.serialize(), json_file)

    @staticmethod
    def deserialize(dict: IDatabase) -> DatabaseNode[IDatabase]:
        return Database(dict)

    @staticmethod
    def load():
        if (os.path.isfile("db.json")):
            with open("db.json") as json_file:
                return Database(json.load(json_file))
        
        db = Database()
        db.save()
        return db