import json, jwt
from functools import wraps
from flask import request, make_response
from passlib.context import CryptContext
from datetime import datetime, timedelta
from models import db


from models.User import User

from config import Settings


class AuthHandler():
    pwd_context     = CryptContext(schemes=["bcrypt"], deprecated="auto")
    JWT_SECRET      = Settings.JWT_SECRET
    JWT_ALGORITHM   = Settings.JWT_ALGORITHM  

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def token_encode(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.JWT_SECRET,
            self.JWT_ALGORITHM
        )

    def token_decode(self, token):
        try:
            payload = jwt.decode(token, self.JWT_SECRET, self.JWT_ALGORITHM)
            return payload['sub']

        except jwt.ExpiredSignatureError as e:
            return False

        except jwt.InvalidTokenError as e:
            return False

    def auth_wrapper(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'x-token-access' in request.headers:
                token = request.headers['x-token-access']
            
            if not token:
                return json.dumps({'message' : str(request.headers)})

            try:
                data = self.token_decode(token=token)
                user = db.session.query(User).filter(User.token==data).first()
                if user is None:
                    return json.dumps({
                        'message' : 'Token is invalid !!',
                        'error'   : str(e)
                })
            except Exception as e:
                return json.dumps({
                    'message' : 'Token is invalid !!',
                    'error'   : str(e)
                })
            # returns the current logged in users contex to the routes
            return  f(*args, **kwargs)

        return decorated


