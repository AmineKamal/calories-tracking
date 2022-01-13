from typing import TypedDict
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt

class Password:
    @staticmethod
    def create(password: str):
        return generate_password_hash(password)

    @staticmethod
    def verify(hash: str, password: str):
        return check_password_hash(hash, password)

class ITokenPayload(TypedDict):
    exp: datetime.datetime
    iat: datetime.datetime
    sub: str

class Token:
    @staticmethod
    def create(username: str, secret: str) -> str:
        payload: ITokenPayload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }

        return jwt.encode(payload, secret, algorithm='HS256') # type:ignore
    
    @staticmethod
    def verify(token: str, secret: str) -> str:
        return jwt.decode(token, secret, algorithms=["HS256"])['sub'] # type:ignore
