from chalice import Blueprint
from chalicelib import global_auth

user_app = Blueprint(__name__)


@user_app.route('/api/user_controller', cors=global_auth.cors_config)
def index():
    return {"user": "controller"}