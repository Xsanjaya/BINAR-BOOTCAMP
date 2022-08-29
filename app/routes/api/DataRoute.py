from flask import Blueprint
from controllers.api.DataController import text, file

data_route = Blueprint('data_route', __name__)

data_route.route('/text', methods=['POST'])(text)
data_route.route('/file', methods=['POST'])(file)