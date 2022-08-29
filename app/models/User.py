from datetime import datetime as dt
from models import db

class User(db.Model):
    __tablename__ = 'users'

    id 			= db.Column('id', db.Integer, primary_key=True)
    name		= db.Column('name', db.String)
    email		= db.Column('email', db.String, unique=True)
    password	= db.Column('password', db.String)
    token       = db.Column('token', db.String)
    created_at 	= db.Column('created_at', db.DateTime, default=db.func.NOW())
    updated_at 	= db.Column('updated_at', db.DateTime, default=db.func.NOW(), onupdate=db.func.NOW())

    dt_format = '%H:%M %d-%m-%Y'

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)

    def list(self):
        return {
            'name'    : self.name,
            'email'   : self.email,
            'created' : dt.strftime(self.created_at, self.dt_format),
        }

    def profile(self):
        return {
            'name'  : self.name,
            'email' : self.email,
            'token' : self.token,
            'created' : dt.strftime(self.created_at, self.dt_format),   
        }
    
    @property
    def serialize(self):
        return {
            'id'         : self.id,
            'name'       : self.name,
            'email'      : self.email,
            'password'   : self.password,
            'token'      : self.token,            
            'created_at' : self.created_at,            
            'updated_at' : self.updated_at,            
        }