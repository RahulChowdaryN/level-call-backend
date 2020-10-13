import json
from chalicelib import global_auth
from chalice import Blueprint, Response
import logging
import os

log = logging.getLogger('sessions-app')
audit_app = Blueprint(__name__)



@audit_app.route('/api/audit_controller', cors=global_auth.cors_config)
def index():
    return Response(body = {"audit": "controller"}, status_code=200)


def update_audit(audit_type,payload):
    log.info(f"updating {audit_type} audit {payload}, invoking lambda function")

    if audit_type == "session":
        global_auth.invokeLambda.invoke(
        FunctionName=f"arn:aws:lambda:{os.environ['CURRENT_REGION']}:886064876783:function:audit-feedback-dev-SessionAuditFunction",
        InvocationType="Event", Payload=json.dumps(payload))

    if audit_type == "user":
        global_auth.invokeLambda.invoke(
        FunctionName=f"arn:aws:lambda:{os.environ['CURRENT_REGION']}:886064876783:function:audit-feedback-dev-UserAuditFunction",
        InvocationType="Event", Payload=json.dumps(payload))
    log.info("lambda function invoked")
    return None


