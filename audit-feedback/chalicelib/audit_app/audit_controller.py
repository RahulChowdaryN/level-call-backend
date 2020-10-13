from chalicelib import global_db_handler,global_auth
from uuid import uuid4
from chalice import Blueprint, Response
import logging
import json
log = logging.getLogger("audit-feedback")

audit_app = Blueprint(__name__)


@audit_app.route('/auditcontroller')
def index():
    return {'audit': 'controller'}


@audit_app.route('/api/audit/user/{user_id}', methods=['GET'], cors=global_auth.cors_config)
def get_user_audit(user_id):
    log.info(f"getting user audit event for userId {user_id}")
    response = global_db_handler.get_user_audit_db().get_user_item(str(user_id))

    if len(response) == 0:
        return Response(body={"message":"user not found"},status_code=400)
    response = global_db_handler.replace_decimals(response)
    return Response(body=response,status_code=200)


@audit_app.route('/api/audit/session/{session_id}', methods=['GET'], cors=global_auth.cors_config)
def get_session_audit(session_id):
    log.info(f"getting session audit event for sessionId {session_id}")
    response = global_db_handler.get_session_audit_db().get_session_item(session_id)
    if len(response) == 0:
        return Response(body={"message":"session not found"},status_code=400)
    response = global_db_handler.replace_decimals(response)
    return Response(body=response,status_code=200)

@audit_app.lambda_function(name='UserAuditFunction')
def user_audit_lambda_function(event, context):
    # Anything you want here.
    log.info(f"user audit entry {event} {context}")
    event['uid'] = str(uuid4())

    global_db_handler.get_user_audit_db().add_item(event)
    return json.dumps({"message": "updated"})


@audit_app.lambda_function(name='SessionAuditFunction')
def session_audit_lambda_function(event, context):
    log.info(f"session audit entry {event} {context}")
    # Anything you want here.
    event['uid'] = str(uuid4())
    global_db_handler.get_session_audit_db().add_item(event)
    return json.dumps({"message": "updated"})


@audit_app.route('/api/audit/session', methods=['POST'], cors=global_auth.cors_config,authorizer=global_auth.authorizer)
def update_session_audit():
    body = audit_app.current_request.json_body
    if not body:
        return Response(body={"message":"no required details"},status_code=422)
    if not body.get("status",False):
        return Response({"message":"status field is required"},status_code=422)
    body['uid'] = str(uuid4())
    body['sessionId'] = global_auth.get_authorized_session_id(audit_app.current_request)
    response = global_db_handler.get_session_audit_db().add_item(body)
    return Response(body = {"message": "updated"},status_code = 200)


@audit_app.route('/api/audit/user', methods=['POST'], cors=global_auth.cors_config,authorizer=global_auth.authorizer)
def update_user_audit():
    body = audit_app.current_request.json_body
    if not body:
        return Response(body={"message":"no required details"},status_code=422)
    if not body.get("status",False):
        return Response({"message":"status field is required"},status_code=422)
    body['uid'] = str(uuid4())
    body['userId'] = global_auth.get_authorized_user_id(audit_app.current_request)
    response = global_db_handler.get_user_audit_db().add_item(body)
    return Response(body = {"message": "updated"},status_code = 200)