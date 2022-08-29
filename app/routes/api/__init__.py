import os
from flask import Blueprint

api_route = Blueprint('api_route', __name__)

@api_route.route('/')
def index():
    result = os.getenv('APP_NAME', 'API NAME')
    return result