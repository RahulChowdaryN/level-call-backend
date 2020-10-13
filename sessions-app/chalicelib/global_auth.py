import logging
from chalice import CORSConfig
from boto3 import client
import os
log = logging.getLogger("sessions-app")


cors_config = CORSConfig(
    allow_origin='*',
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=False
)

invokeLambda = client("lambda", region_name=f"{os.environ['CURRENT_REGION']}")


def get_authorized_session_id(current_request):
    """
     generates session id from auth token
    :params current_request body
    :return: sessionId (string)

    """
    log.info(f"generating current request session_id{current_request.context}")
    return current_request.context['authorizer']['sessionId']


def get_authorized_email(current_request):
    """
     generates email from auth token
    :params current_request body
    :return: email (string)
    """
    log.info(f"generating current request email{current_request.context}")
    return current_request.context['authorizer']['principalId']


def get_authorized_user_id(current_request):
    """
     generates user session data from auth token
    :params current_request body
    :return: email (string)

    """
    log.info(f"generating current request user data {current_request.context}")
    return current_request.context['authorizer']['userId']


def get_authorized_user_data(current_request):
    """
     generates user session data from auth token
    :params current_request body
    :return: email (string)

    """
    log.info(f"generating current request user data {current_request.context}")
    user_data = {'firstName':current_request.context['authorizer']['firstName'],
                 'lastName': current_request.context['authorizer']['lastName'],
                 'uid':current_request.context['authorizer']['userId'],
                 'role':current_request.context['authorizer']['role'],
                 'email':current_request.context['authorizer']['principalId']}
    return user_data


