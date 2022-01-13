from typing import Any, Callable, Dict, Literal, Optional, TypeVar, TypedDict, cast, overload
from flask import Flask, request
from flask_cors import CORS
from src.auth import Token
from src.database.database import Database
from src.database.user import User
from src.validators.base import Validator
from src.utils.json import to_json
import jwt

Body = TypeVar("Body")
ApiCallback = TypeVar("ApiCallback", bound=Callable[..., Any])

class ApiValidatorOption(TypedDict, total=False):
    validator: Validator

class ApiBodyOption(ApiValidatorOption):
    body: Literal[True]

class ApiAuthOption(TypedDict):
    auth: Literal[True]

class ApiFullOptions(ApiAuthOption, ApiBodyOption):
    pass

ApiOptions = Optional[ApiBodyOption | ApiAuthOption | ApiFullOptions]

class Api:
    def __init__(self, app: Flask) -> None:
        self.__app: Flask = app
        CORS(app)
        self.db: Database = Database.load()

    def run(self):
        return self.__app.run()

    @overload
    def get(self, url: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
        ...
    @overload
    def get(self, url: str, options: ApiBodyOption) -> Callable[[Callable[[Body], Any]], Callable[[Body], Any]]:
        ...
    @overload
    def get(self, url: str, options: ApiAuthOption) -> Callable[[Callable[[User], Any]], Callable[[User], Any]]:
        ...
    @overload
    def get(self, url: str, options: ApiFullOptions) -> Callable[[Callable[[User, Body], Any]], Callable[[User, Body], Any]]: # type:ignore
        ...
    
    @overload
    def post(self, url: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
        ...
    @overload
    def post(self, url: str, options: ApiBodyOption) -> Callable[[Callable[[Body], Any]], Callable[[Body], Any]]:
        ...
    @overload
    def post(self, url: str, options: ApiAuthOption) -> Callable[[Callable[[User], Any]], Callable[[User], Any]]:
        ...
    @overload
    def post(self, url: str, options: ApiFullOptions) -> Callable[[Callable[[User, Body], Any]], Callable[[User, Body], Any]]: # type:ignore
        ...

    @overload
    def put(self, url: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
        ...
    @overload
    def put(self, url: str, options: ApiBodyOption) -> Callable[[Callable[[Body], Any]], Callable[[Body], Any]]:
        ...
    @overload
    def put(self, url: str, options: ApiAuthOption) -> Callable[[Callable[[User], Any]], Callable[[User], Any]]:
        ...
    @overload
    def put(self, url: str, options: ApiFullOptions) -> Callable[[Callable[[User, Body], Any]], Callable[[User, Body], Any]]: # type:ignore
        ...

    @overload
    def delete(self, url: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
        ...
    @overload
    def delete(self, url: str, options: ApiBodyOption) -> Callable[[Callable[[Body], Any]], Callable[[Body], Any]]:
        ...
    @overload
    def delete(self, url: str, options: ApiAuthOption) -> Callable[[Callable[[User], Any]], Callable[[User], Any]]:
        ...
    @overload
    def delete(self, url: str, options: ApiFullOptions) -> Callable[[Callable[[User, Body], Any]], Callable[[User, Body], Any]]: # type:ignore
        ...

    def get(self, url: str, options: ApiOptions = None) -> Callable[[ApiCallback], ApiCallback]:
        return lambda f: self.__app.get(url)(self.__get_wrapper(f, options)) # type:ignore

    def post(self, url: str, options: ApiOptions = None) -> Callable[[ApiCallback], ApiCallback]:
        return lambda f: self.__app.post(url)(self.__get_wrapper(f, options)) # type:ignore
    
    def put(self, url: str, options: ApiOptions = None) -> Callable[[ApiCallback], ApiCallback]:
        return lambda f: self.__app.put(url)(self.__get_wrapper(f, options)) # type:ignore
    
    def delete(self, url: str, options: ApiOptions = None) -> Callable[[ApiCallback], ApiCallback]:
        return lambda f: self.__app.delete(url)(self.__get_wrapper(f, options)) # type:ignore

    def __get_wrapper(self, f: ApiCallback, options: ApiOptions) -> ApiCallback:
        def wrapper() -> Any:
            try:
                if not options:
                    res = f()
                elif 'auth' in options and not 'body' in options:
                    user = self.__get_user()
                    res = f(user)
                elif 'body' in options and not 'auth' in options:
                    body = self.__get_body(options.get('validator', None))
                    res = f(body)
                elif 'body' in options and 'auth' in options:
                    user = self.__get_user()
                    body = self.__get_body(options.get('validator', None))
                    res = f(user, body)
                else:
                    res = f()

                res = res if res == None else to_json(res)
                return res
            except ApiException as e:
                return e.message, e.code

        wrapper.__name__ = f.__name__
        return cast(ApiCallback, wrapper)

    def __get_user(self):
        token = cast(Dict[str, str], request.headers).get('Authorization') # type:ignore

        if (not token): raise ApiException(401, "Invalid Token")
        token = token.split(" ")[1]

        try:
            username = Token.verify(token, self.db.secret)
            return self.db.users[username]
        except jwt.ExpiredSignatureError:
            raise ApiException(401, 'Signature expired.')
        except jwt.InvalidTokenError:
            raise ApiException(401, 'Invalid token.')
        
    def __get_body(self, validator: Optional[Validator]):
        body = request.get_json()

        if body == None: raise ApiException(400, "Request Body is missing.")
        if validator != None and not validator.validate(body): raise ApiException(400, 'Request Body is invalid')

        return body

class ApiException(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
