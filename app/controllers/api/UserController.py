import json
from flask import request
from models.User import User
from models import db
from utils.auth_handler import AuthHandler

auth = AuthHandler()

@auth.auth_wrapper
def index():
    users = db.session.query(User).all()
    
    result = {
        "success" : True,
        "error"   : None,
        "message" : "User All",
        "data"    : [ dict(user.list()) for user in users ]
    }
    return json.dumps(result)


def show(userId):
    return 'success'

def update(userId):
    return 'success'


def destroy(userId):
    return 'success'