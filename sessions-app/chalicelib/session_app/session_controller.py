import os
from uuid import uuid4
from chalicelib import auth, global_auth
from chalicelib.validationslib import session_validation
from chalicelib import global_db_handler
from requests.auth import HTTPBasicAuth
from chalicelib.audit_app import audit_controller
from datetime import datetime
from chalice import Blueprint, Response
import json
import logging
import requests

session_app = Blueprint(__name__)

log = logging.getLogger('sessions-app')

OPENVIDU_URL = os.environ['OPENVIDU_URL']
ROCKETCHAT_URL = os.environ['ROCKETCHAT_URL']


@session_app.route('/api/session_controller', cors=global_auth.cors_config)
def index():
    return Response(body={"session": "controller"}, status_code=200)


@session_app.route('/api/session/join', methods=['POST'], cors=global_auth.cors_config)
def login():
    """"
    function to join session and generate jwt.
    :returns jwt token and session data (dict)
    """
    body = session_app.current_request.json_body
    if not body or not body.get('token'):
        return Response(body={'message': 'token is required'}, status_code=422)
    log.info(f"received session join request with {body['token']}")
    response = global_db_handler.get_user_db().validate_token(body['token'])
    log.info(f"response from db call for token  {body['token']} ")
    if len(response) <= 0:
        log.info("no session found with token")
        return Response(body={'message': 'no session found', 'code': 'session_not_found'}, status_code=400)
    current_session_details = global_db_handler.get_session_db().get_item(response['sessionId'])
    if len(current_session_details) == 0:
        return Response(body={'message': 'no session found', 'code': 'session_not_found'}, status_code=400)
    log.info(f'current session details for the token{current_session_details}')
    body['sessionDetails'] = {'email': response['email'], 'firstName': response['firstName'],
                              'lastName': response['lastName'], 'token': body['token'],
                              'role': response['role'],
                              'userId': response['uid'], 'sessionId': response['sessionId']}
    log.info('generating authentication token using jwt')
    jwt_token = auth.get_jwt_token(body['sessionDetails'])
    log.info('token generated, returning response ')
    session_audit_payload = {"sessionId": response['sessionId'], "statusId": 3, "status": "IN_PROGRESS",
                             "timestamp": str(datetime.utcnow())}
    user_audit_payload = {"userId": response['uid'], "roleId": 3, "status": "JOINED",
                          "timestamp": str(datetime.utcnow()), 'email': response['email']}
    session_status_payload = {"sessionId": response['sessionId'], "status": "IN_PROGRESS"}
    audit_controller.update_audit("session", session_audit_payload)
    audit_controller.update_audit("user", user_audit_payload)
    update_session_status(session_status_payload)
    current_session_details = global_db_handler.replace_decimals(current_session_details)
    return Response(body={'token': jwt_token, 'sessionDetails': current_session_details,
                          'user': {'firstName': response['firstName'],
                                   'lastName': response['lastName'],
                                   'email': response['email'],
                                   'phoneNumber': response['phoneNumber'],
                                   'profilePicUrl': response['profilePicUrl']}}, status_code=200)
    #            headers={"Set-Cookie": f"rocketChatAuthToken={response['Items'][0]['rocketChatAuthToken']};secure;",


@session_app.route('/api/session/schedule', methods=['POST'], cors=global_auth.cors_config, authorizer=auth.jwt_auth)
def schedule_session():
    """
    schedules session
    :param  "body data" (dict)
    :return: session_id (dict)
    """
    body = session_app.current_request.json_body
    if not body:
        return Response(body={'message': 'empty body, missing required details'}, status_code=422)
    log.info("scheduling new session")
    # print("scheduling new session with body", body)
    is_valid = session_validation.validate_session(body)
    if is_valid != True:
        return Response(body=is_valid, status_code=422)
    log.info("Validation done. creating a session record")
    session_id = str(uuid4())
    session_record = {'sessionId': session_id, 'scheduledTime': body['scheduledTime'], 'courseId': body['courseId'],
                      'name': body['name'], 'duration': body['duration'],
                      'status': 'REGISTERED', 'description': body['description'], 'recordingUrl': ''}

    log.info(f"creating user record for session id {{session_id}}")
    user_list = []
    session_only_users = []
    for student in body['students']:
        student_token = str(uuid4())
        session_only_record = {'email': student['email'], 'firstName': student['firstName'],
                               'lastName': student['lastName'], 'token': student_token,
                               'profilePicUrl': student['profilePicUrl'],
                               'phoneNumber': student['phoneNumber']}
        user_record = {'roleId': 1, 'role': "student",
                       'sessionId': session_id, 'uid': str(uuid4())}
        user_record.update(session_only_record)
        session_only_users.append(session_only_record)
        user_list.append(user_record)
    session_record['students'] = session_only_users
    tutor_token = str(uuid4())
    session_record['tutor'] = {'firstName': body['tutor']['firstName'], 'lastName': body['tutor']['lastName'],
                               'email': body['tutor']['email'], 'token': tutor_token,
                               'profilePicUrl': body['tutor']['profilePicUrl'],
                               'phoneNumber': body['tutor']['phoneNumber']}
    tutor_record = {'roleId': 2, 'role': "tutor",
                    'sessionId': session_id, 'uid': str(uuid4())}
    tutor_record.update(session_record['tutor'])
    user_list.append(tutor_record)
    global_db_handler.get_session_db().add_item(session_record)
    global_db_handler.get_user_db().add_item(user_list)
    session_audit_payload = {"sessionId": session_id, "statusId": 1, "status": "REGISTERED",
                             "timestamp": str(datetime.utcnow())}
    # user_audit_payload = {"userId": user_id, "roleId": 3, "status": "LEFT",
    #                      "timestamp": str(datetime.utcnow())}
    audit_controller.update_audit("session", session_audit_payload)
    # audit_controller.update_audit("user", user_audit_payload)
    return Response(body={"sessionId": session_id}, status_code=200)


@session_app.route('/api/session', methods=['POST'], authorizer=auth.jwt_auth, cors=global_auth.cors_config)
def get_sessions():
    """
    handles session retrievals based on email,session_id and course_id
    :return: session details
    """

    body = session_app.current_request.json_body
    if not body:
        return Response({'message': 'empty body, missing required details'}, status_code=422)

    log.info('retrieving session details')
    if body.get('sessionId', False) and body['sessionId'] is not None:
        log.info('connecting to session db with session id')
        current_session = global_db_handler.get_session_db().get_item_details(body['sessionId'])
        current_session = global_db_handler.replace_decimals(current_session)
        return Response(body=current_session, status_code=200)
    if body.get('courseId', False):
        if not body.get('email'):
            body['email'] = global_auth.get_authorized_email(session_app.current_request)
        user_session_data = global_db_handler.get_user_db().list_items_by_mail(body['email'])
        log.info('current user data ')
        if len(user_session_data) <= 0:
            return Response(body=[], status_code=200)
        session_id_list = []
        for each_session in user_session_data:
            session_id_list.append(each_session['sessionId'])
        log.info('sessions found for current request')
        session_details = global_db_handler.get_session_db().list_items_course(session_id_list, body['courseId'])
        log.info("session details")
        session_details = global_db_handler.replace_decimals(session_details)
        return Response(body=session_details, status_code=200)
    if not body.get('email', False):
        log.info('no email found. decoding auth token')
        body['email'] = global_auth.get_authorized_email(session_app.current_request)
    log.info('getting session details by email')
    user_session_data = global_db_handler.get_user_db().list_items_by_mail(body['email'])
    log.info('response from user table')
    if len(user_session_data) <= 0:
        return Response(body=[], status_code=200)
    session_id_list = []
    for each_session in user_session_data:
        session_id_list.append(each_session['sessionId'])
    log.info('getting all sessions which match session ids')
    session_details = global_db_handler.get_session_db().list_items_mail(session_id_list)
    log.info(f"returning session details {session_details}")
    session_details = global_db_handler.replace_decimals(session_details)
    return Response(body=session_details, status_code=200)


@session_app.route('/api/session/end', methods=['GET'], authorizer=auth.jwt_auth, cors=global_auth.cors_config)
def end_session():
    #  print("session end request", session_app.current_request.headers)
    # new_cookie = session_app.current_request.headers['Cookie']
    # print("cookie information for session end request", new_cookie)
    user_id = global_auth.get_authorized_user_id(session_app.current_request)
    session_id = global_auth.get_authorized_session_id(session_app.current_request)
    email = global_auth.get_authorized_email(session_app.current_request)
    if not user_id or not session_id or not email:
        return Response(body={"message": "session not found"}, status_code=400)
    session_audit_payload = {"sessionId": session_id, "statusId": 3, "status": "COMPLETED",
                             "timestamp": str(datetime.utcnow())}
    user_audit_payload = {"userId": user_id, "roleId": 3, "status": "LEFT",
                          "timestamp": str(datetime.utcnow()), 'email': email}
    audit_controller.update_audit("session", session_audit_payload)
    audit_controller.update_audit("user", user_audit_payload)
    session_status_payload = {"sessionId": session_id, "status": "COMPLETED"}
    update_session_status(session_status_payload)

    return Response(body={"message": "success"}, status_code=200)


@session_app.route('/api/session/openvidu', methods=['POST'], authorizer=auth.jwt_auth, cors=global_auth.cors_config)
def generate_openvidu_token():
    """
    handles openvidu connections and token related stuff
    :return: openvidu url and token
    """
    try:

        body = session_app.current_request.json_body

        session_id = global_auth.get_authorized_session_id(session_app.current_request)
        data = {
            "mediaMode": "ROUTED",
            "recordingMode": "ALWAYS",
            "customSessionId": session_id
        }
        log.info("connecting to openvidu")
        headers = {'Content-type': 'application/json', 'Connection': 'keep-alive'}
        openvidu_session_response = requests.post(OPENVIDU_URL + 'sessions', headers=headers, json=data, verify=False,
                                                  auth=HTTPBasicAuth(os.environ['OPENVIDU_USERNAME'],
                                                                     os.environ['OPENVIDU_PASSWORD']))
        if openvidu_session_response.status_code == 409 or openvidu_session_response.status_code == 200:
            token_data = {"session": session_id, "data": json.dumps(body, separators=(',', ':'))}

            openvidu_token_response = requests.post(OPENVIDU_URL + 'tokens', headers=headers, json=token_data,
                                                    verify=False, auth=HTTPBasicAuth(os.environ['OPENVIDU_USERNAME'],
                                                                                     os.environ['OPENVIDU_PASSWORD']))
            json_response = openvidu_token_response.json()
            data = json.loads(json_response['data'])
            print(data, "data")
            openvidu_token_response.json()['data'] = data
            response = {'id': json_response['id'], 'sessionId': json_response['session'],
                        'role': json_response['role'], 'data': data,
                        'token': json_response['token']}

            log.info('{}'.format(openvidu_token_response.__dict__))
            return Response(body=response, status_code=200)

    except Exception as e:
        log.info('exception while calling openvidu {}'.format(e.args))
        return Response(body={"message": "unable to create session", "code": "open_vidu_issue"}, status_code=400)


@session_app.lambda_function(name='SessionStatusUpdateFunction')
def session_status_update_lambda_function(event, context):
    log.info(f"session status update {event} {context}")
    global_db_handler.get_session_db().update_item(event)
    return json.dumps({"message": "updated"})


def update_session_status(payload):
    log.info(f"updating session status, invoking a lambda from sessions-controller")
    global_auth.invokeLambda.invoke(
        FunctionName=f"arn:aws:lambda:{os.environ['CURRENT_REGION']}:886064876783:function:sessions-app-dev"
                     f"-SessionStatusUpdateFunction",
        InvocationType="Event", Payload=json.dumps(payload))
    return None


@session_app.route('/api/status/update', methods=['POST'], cors=global_auth.cors_config, authorizer=auth.jwt_auth)
def update_session_status_api():
    body = session_app.current_request.json_body
    log.info(f"session status update {body}")

    if not body or not body.get('status', False):
        return Response(body={'message': 'empty body, status field is required '}, status_code=422)
    if not body.get('sessionId', False):
        body['sessionId'] = global_auth.get_authorized_session_id(session_app.current_request)
    response = global_db_handler.get_session_db().update_item(body)
    return Response(body=response, status_code=200)


@session_app.route('/api/session/extend', methods=['POST'], cors=global_auth.cors_config, authorizer=auth.jwt_auth)
def update_session_duration():
    body = session_app.current_request.json_body
    log.info(f"session status update {body}")

    if not body or not body.get('duration', False):
        return Response(body={'message': 'empty body, duration field is required'}, status_code=422)

    if not isinstance(body['duration'], int):
        return Response(body={'message': 'duration field is int'}, status_code=422)

    if not body.get('sessionId', False):
        body['sessionId'] = global_auth.get_authorized_session_id(session_app.current_request)
    response = global_db_handler.get_session_db().update_duration(body)
    response = global_db_handler.replace_decimals(response)
    return Response(body=response, status_code=200)


@session_app.route('/api/testjwt', methods=['GET'], authorizer=auth.jwt_auth, cors=global_auth.cors_config)
def test_jwt_session():
    user_id = global_auth.get_authorized_user_id(session_app.current_request)
    session_id = global_auth.get_authorized_session_id(session_app.current_request)
    user_data = global_auth.get_authorized_user_data(session_app.current_request)
    email = global_auth.get_authorized_email(session_app.current_request)
    response = {"sessionId": session_id, "userId": user_id, "user_data": user_data, "email": email}
    response = global_db_handler.replace_decimals(response)
    return {"message": response}


@session_app.lambda_function(name='SessionNotificationsPhone')
def session_notify_phone_function(event, context):
    import logging
    from boto3 import client
    from botocore.exceptions import ClientError
    log = logging.getLogger('sessions-app')
    log.info(f"session Phone notifications {event} {context}")
    sns = client('sns', region_name="ap-south-1")

    try:
        for each_item in event['phone_number_list']:
            print(f"sending message to {each_item['user_details']['phone_number']}")
            sns.publish(
                PhoneNumber=each_item['user_details']['phone_number'],
                Message=f"Hello {each_item['user_details']['first_name']}. Your session is about to start. This is "
                        f"just a reminder. Please login to https://dev.mylevelapp.com/  Thank you",
                Subject='LevelApp: Session Reminder',
                MessageAttributes={
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
        log.info(f'sending text messages"')
    except ClientError as e:
        print(e.response['Error']['Message'])
        return json.dumps({
            'statusCode': 400,
            'body': json.dumps(e.response['Error']['Message'])
        })
    else:
        return json.dumps({"message": "messages sent"})


@session_app.lambda_function(name='SessionNotificationsEmail')
def session_notify_email_function(event, context):
    import logging
    import json
    import boto3
    from botocore.exceptions import ClientError
    log = logging.getLogger('sessions-app')
    log.info(f"session Email notifications {event} {context}")
    print(event)
    aws_region = "ap-south-1"

    client = boto3.client('ses', region_name=aws_region)
    # Try to send the email.
    try:
        # Provide the contents of the email.
        for each_item in event['email_list']:
            log.info(json.dumps({"name": each_item['user_details']['first_name']}).replace('"', '/"'))

            client.send_templated_email(
                Source='noreply@mylevelapp.com',
                Destination={
                    'ToAddresses': [
                        each_item['user_details']['email']
                    ],
                },

                Template='Group_Invitation',
                TemplateData=json.dumps({"name": each_item['user_details']['first_name']})).replace('"', '/"')
            print(f"sending email to {each_item['user_details']['email']}")

    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
        return json.dumps({
            'statusCode': 400,
            'body': json.dumps(e.response['Error']['Message'])
        })
    else:
        log.info("Emails sent! Message ID:"),
        # print(response)
        return json.dumps({"message": "email sent"})


@session_app.route('/api/notify', methods=['GET'], authorizer=auth.jwt_auth, cors=global_auth.cors_config)
def session_notify_api():
    log.info("notification api")
    session_id = global_auth.get_authorized_session_id(session_app.current_request)
    user_data = global_auth.get_authorized_user_data(session_app.current_request)
    user_role = user_data['role']
    phone_number_list = []
    email_list = []
    log.info(f"user role {user_role}")
    if user_role == "student":
        user_details = global_db_handler.get_session_db().get_user_details(session_id, "tutor")
        log.info(f"tutor details to notify session {user_details}")
        phone_number_list = [{"user_details": {"first_name": user_details["tutor"]["firstName"],
                                               "phone_number": user_details["tutor"]["phoneNumber"]}}]
        email_list = [{"user_details": {"first_name": user_details["tutor"]["firstName"],
                                        "email": user_details["tutor"]["email"]}}]
    elif user_role == "tutor":
        user_details = global_db_handler.get_session_db().get_user_details(session_id, "student")
        log.info(f"student details to notify session {user_details}")
        for each_item in user_details['students']:
            log.debug(each_item)
            phone_number_list.append(
                {"user_details": {"phone_number": each_item["phoneNumber"], "first_name": each_item["firstName"]}})
            email_list.append({"user_details": {"email": each_item["email"], "first_name": each_item["firstName"]}})
    else:
        log.info(f"unknown user role. may be level admin ?. {user_role}")
        return Response(body={"message": "user role not identified"}, status_code=400)
    log.info(f'sending email to users with info {user_details}')
    response = {'email_list': email_list, 'phone_number_list': phone_number_list}
    phone_status = global_auth.invokeLambda.invoke(
        FunctionName=f"arn:aws:lambda:{os.environ['CURRENT_REGION']}:886064876783:function:sessions-app-dev"
                     f"-SessionNotificationsPhone",
        InvocationType="RequestResponse", Payload=json.dumps(response))
    log.info(f"text messages sent {phone_status}")
    email_status = global_auth.invokeLambda.invoke(
        FunctionName=f"arn:aws:lambda:{os.environ['CURRENT_REGION']}:886064876783:function:sessions-app-dev"
                     f"-SessionNotificationsEmail",
        InvocationType="RequestResponse", Payload=json.dumps(response))

    log.info(f"emails sent {email_status}")

    return Response(body={"phoneStatus": phone_status['ResponseMetadata']['HTTPStatusCode'],
                          "emailStatus": email_status['ResponseMetadata']['HTTPStatusCode']}, status_code=202)
