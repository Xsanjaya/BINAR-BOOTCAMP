from flask import Blueprint
from controllers.api.UserController import index, show, update, destroy

user_route = Blueprint('user_route', __name__)

user_route.route('/', methods=['GET'])(index)
user_route.route('/<int:user_id>', methods=['GET'])(show)
user_route.route('/<int:user_id>/edit', methods=['POST'])(update)
user_route.route('/<int:user_id>', methods=['DELETE'])(destroy)