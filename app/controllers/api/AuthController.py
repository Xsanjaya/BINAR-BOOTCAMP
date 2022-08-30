import json, uuid
from flask import request, redirect
from models.User import User
from models import db
from utils.auth_handler import AuthHandler

auth_handler = AuthHandler()

def register():
    req = request.json
    name     = req['name']
    email    = req['email']
    password = auth_handler.hash_password( req['password'] )
    token    = str(uuid.uuid4())

    try:
        user = User(name=name, email=email, password=password, token=token)
        
        db.session.add(user)
        db.session.commit()

        result = {
            "success" : True,
            "error"   : None,
            "message" : "Create User",
            "data"    : [user.profile()]
        }

    except Exception as err:
        result = {
            "success" : False,
            "error"   : str(err),
            "message" : "Create User Error",
            "data"    : []
        }

    return json.dumps(result)


def login():
    req = request.json
    email    = req['email']
    password = req['password']

    user =  db.session.query(User).filter(User.email == email).first()

    if (user is None) or (not auth_handler.verify_password(password, user.password)):
        result = {
            "success" : False,
            "error"   : None,
            "message" : "Email is Taken",
            "data"    : []
        }
        return json.dumps(result)

    token = auth_handler.token_encode(user.token)

    result = {
            "success" : True,
            "error"   : None,
            "message" : "Login Success",
            "data"    : {
                'profile' : user.list(), 
                'token'   : token}
        }
    return json.dumps(result)


def logout():
    pass