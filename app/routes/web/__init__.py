import os
from flask import Blueprint

web_route = Blueprint('web_route', __name__)

@web_route.route('/')
def index():
    result = os.getenv('APP_NAME', 'WEB NAME')
    return result