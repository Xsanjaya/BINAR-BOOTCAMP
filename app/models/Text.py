from datetime import datetime as dt
from models import db

class Text(db.Model):
    __tablename__ = 'texts'

    id 			= db.Column('id', db.Integer, primary_key=True)
    original   = db.Column('original', db.String)
    result		= db.Column('result', db.String)
   #  created_at 	= db.Column('created_at', db.DateTime, default=db.func.NOW())
   #  updated_at 	= db.Column('updated_at', db.DateTime, default=db.func.NOW(), onupdate=db.func.NOW())