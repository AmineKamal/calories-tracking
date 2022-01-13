from typing import cast
from flask import Flask
from src.api import Api, ApiException
from src.auth import Password, Token
from src.database.macros import IMacroCalculation, IMacros, Macros
from src.schemas.macros import IPartialMacros, MacroValidator
from src.schemas.meal import IMeal, IMealName, MealNameValidator, MealValidator
from src.schemas.user import CreateUserSchemaValidator, FollowUserValidator, IFollowUser, ILoginUser, IUsername, LoginUserSchemaValidator, UpdateUserSchemaValidator, UsernameValidator
from src.database.user import ICreateUser, IUpdateUser, User

api = Api(Flask(__name__))
db = api.db

@api.post("/users", {'body': True, 'validator': CreateUserSchemaValidator})
def create_user(body: ICreateUser):
    if (body.get('username') in db.users): raise ApiException(400, "User with the same username already Exists.")

    body['password'] = Password.create(body['password'])
    user = User(body).link(db)
    db.add_user(user)
    
    return user

@api.post("/user/login", {'body': True, 'validator': LoginUserSchemaValidator})
def login(body: ILoginUser):
    if (not body.get('username') in db.users): raise ApiException(404, "User not Found.")

    user = db.users[body.get('username')]
    if (not Password.verify(user.password, body.get('password'))): raise ApiException(401, "Password or username is not correct.")

    token = Token.create(user.username, db.secret)
    return {'user': user, 'token': token}

@api.get("/user", {'auth' : True})
def get_user(user: User):
    return user

@api.put("/user", {'auth' : True, 'body':True, 'validator': UpdateUserSchemaValidator })
def update_user(user: User, body: IUpdateUser):
    user.update_user(body)
    return user

@api.put("/user/evaluate/macros", {'auth' : True})
def evaluate_macros(user: User):
    macros = Macros.calculate_macros(cast(IMacroCalculation, user))
    user.target_macros.update_macros(macros)
    return user

@api.put('/user/add/macros', {'auth': True, 'body': True, 'validator': MacroValidator})
def add_macros(user: User, body: IPartialMacros):
    user.current_macros += Macros(body)
    return user

@api.put('/user/remove/macros', {'auth': True, 'body': True, 'validator': MacroValidator})
def remove_macros(user: User, body: IPartialMacros):
    user.current_macros -= Macros(body)
    return user

@api.post('/user/meals', {'auth': True, 'body': True, 'validator': MealValidator})
def create_meal(user: User, body: IMeal):
    user.add_meal(body)

    for username, options in user.followers.items():
        if not options['subscribe_to_meals']: continue
        db.users[username].add_meal(body)

    return user

@api.put('/user/add/meal', {'auth': True, 'body': True, 'validator': MealNameValidator})
def add_meal(user: User, body: IMealName):
    if not body['name'] in user.meals: raise ApiException(404, "Meal not found")
    user.current_macros += Macros(cast(IMacros, user.meals[body['name']]))
    return user

@api.put('/user/remove/meal', {'auth': True, 'body': True, 'validator': MealNameValidator})
def remove_meal(user: User, body: IMealName):
    if not body['name'] in user.meals: raise ApiException(404, "Meal not found")
    user.current_macros -= Macros(cast(IMacros, user.meals[body['name']]))
    return user

@api.put('/user/follow', {'auth': True, 'body': True, 'validator': FollowUserValidator})
def add_contact(user: User, body: IFollowUser):
    if not body['username'] in db.users: raise ApiException(404, "Username not found")
    user.follow(db.users[body['username']], body['options'])
    return user

@api.put('/user/unfollow', {'auth': True, 'body': True, 'validator': UsernameValidator})
def remove_contact(user: User, body: IUsername):
    if not body['username'] in db.users: raise ApiException(404, "Username not found")
    user.unfollow(db.users[body['username']])
    return user

@api.get('/user/remaining/macros', {'auth': True})
def get_remaining_macros(user: User):
    return user.target_macros - user.current_macros

api.run()