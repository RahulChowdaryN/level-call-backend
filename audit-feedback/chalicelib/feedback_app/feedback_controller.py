from chalice import Blueprint, Response
from chalicelib import global_db_handler,global_auth
from uuid import uuid4
import logging
from datetime import datetime

log = logging.getLogger("audit-feedback")

feedback_app = Blueprint(__name__)


@feedback_app.route('/feedbackcontroller')
def index():
    return {"feedback": "controller"}


@feedback_app.route('/api/feedback', methods=['POST'], cors=global_auth.cors_config  , authorizer=global_auth.authorizer)
def update_feedback():
    body = feedback_app.current_request.json_body
    if not body:
        return Response(body = {"message":"no required details"},status_code=422)
    if not body.get("rating",False) or not body.get("note",False):
        return Response(body={"message":"rating and note fields are mandatory"}, status_code=422)
    log.info(feedback_app.current_request.context)
    body['uid'] = str(uuid4())
    body['sessionId'] = global_auth.get_authorized_session_id(feedback_app.current_request)
    current_user_data = global_auth.get_authorized_user_data(feedback_app.current_request)
    body['email'] = current_user_data['email']
    body['role'] = current_user_data['role']
    body['userId'] = current_user_data['userId']
    body['timestamp'] = str(datetime.utcnow())

    response = global_db_handler.get_feedback_db().add_item(body)
    return Response(body = {"message": "updated"},status_code = 200)


@feedback_app.route('/api/feedback/{session_id}', methods=['GET'], cors=global_auth.cors_config ,authorizer=global_auth.authorizer)
def get_feedback(session_id):

    response = global_db_handler.get_feedback_db().get_item(session_id)

    if len(response) ==0:
        return Response(body={"message":"unable to find session id"},status_code=400)

    response = global_db_handler.replace_decimals(response)
    return Response(body=response,status_code=200)