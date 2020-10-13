from chalicelib import global_db_handler,global_auth
from chalice import Blueprint, Response
import logging

log = logging.getLogger('sessions-app')
roles_app = Blueprint(__name__)

_USER_ROLES = None
_SESSION_ROLES = None


@roles_app.route('/api/roles_controller', cors=global_auth.cors_config)
def index():
    return Response(body = {"roles": "controller"}, status_code=200)


def user_roles():

    global _USER_ROLES
    if _USER_ROLES is None:
        log.info("cache miss for user roles, connecting to db")
        _USER_ROLES = global_db_handler.get_user_roles_db().list_all_items()
        _USER_ROLES = global_db_handler.replace_decimals(_USER_ROLES)
    return Response(body=_USER_ROLES, status_code=200)


def session_roles():
    global _SESSION_ROLES
    if _SESSION_ROLES is None:
        log.info("cache miss for session roles, connecting to db")
        _SESSION_ROLES = global_db_handler.get_session_roles_db().list_all_items()
        _SESSION_ROLES = global_db_handler.replace_decimals(_SESSION_ROLES)
    return Response(body=_SESSION_ROLES, status_code = 200)


@roles_app.route('/api/session/types', methods=['GET'], cors=global_auth.cors_config)
def get_session_types():
    roles_data = session_roles()

    return roles_data


@roles_app.route('/api/session/types', methods=['POST'], cors=global_auth.cors_config)
def update_session_types():
    body = roles_app.current_request.json_body

    if not body:
        return Response(body = {'message': 'empty body, missing required details'}, status_code=422)
    all_roles_list = []
    for each_role in body:
        all_roles_list.append(each_role)
    response = global_db_handler.get_session_roles_db().add_item(all_roles_list)

    return Response(body = {"message": response}, status_code = 200)


@roles_app.route('/api/user/roles', methods=['GET'], cors=global_auth.cors_config)
def get_user_roles():

    roles_data = user_roles()

    return roles_data


@roles_app.route('/api/user/roles', methods=['POST'], cors=global_auth.cors_config)
def update_user_roles():
    body = roles_app.current_request.json_body

    if not body:
        return Response(body={'message': 'empty body, missing required details'},status_code=422)
    all_roles_list = []
    for each_role in body:
        all_roles_list.append(each_role)
    response = global_db_handler.get_user_roles_db().add_item(all_roles_list)
    return Response(body = {"message": response}, status_code=200)