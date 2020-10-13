from chalice import CustomAuthorizer,CORSConfig
import logging
from boto3 import client
import os
log = logging.getLogger("audit-feedback")

invokeLambda = client("lambda", region_name=f"{os.environ['CURRENT_REGION']}")

cors_config = CORSConfig(
    allow_origin='*',
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=False
)

authorizer = CustomAuthorizer(
    'MyCustomAuth', header='Authorization',
    authorizer_uri=(f"arn:aws:apigateway:{os.environ['CURRENT_REGION']}:lambda:path/2015-03-31"
                    "/functions/arn:aws:lambda:us-east-2:886064876783:function:sessions-app-dev-jwt_auth/invocations"))


def get_authorized_session_id(current_request):
    log.info("current request session_id", current_request.context)
    return current_request.context['authorizer']['sessionId']


def get_authorized_email(current_request):
    log.info("current request email", current_request.context)
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
                 'userId':current_request.context['authorizer']['userId'],
                 'role':current_request.context['authorizer']['role'],
                 'email':current_request.context['authorizer']['principalId']}
    return user_data