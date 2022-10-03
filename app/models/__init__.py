from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import AppConfig
config = AppConfig()

db = SQLAlchemy()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False, future=True)