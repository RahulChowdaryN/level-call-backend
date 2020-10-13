import datetime
from uuid import uuid4
import jwt
import logging
from chalice import Blueprint, AuthResponse, Response, UnauthorizedError
log = logging.getLogger('sessions-app')
_SECRET = b'\xf7\xb6k\xabP\xce\xc1\xaf\xad\x86\xcf\x84\x02\x80\xa0\xe0'
auth_app = Blueprint(__name__)


def get_jwt_token(session_details):
    log.info('in auth, generating jwt token {}'.format(session_details))
    now = datetime.datetime.utcnow()
    unique_id = str(uuid4())
    payload = {
        'sessionId': session_details['sessionId'],
        'email': session_details['email'],
        'firstName': session_details['firstName'],
        'lastName': session_details['lastName'],
        'token':session_details['token'],
        'role':session_details['role'],
        'iat': now,
        'nbf': now,
        'jti': unique_id,
        'userId':session_details['userId']
        # NOTE: We can also add 'exp' if we want tokens to expire.
    }
    return jwt.encode(payload, _SECRET, algorithm='HS256').decode('utf-8')


def decode_jwt_token(token):
    log.info("in auth, decoding token")
    try:
        decoded_token = jwt.decode(token, _SECRET, algorithms=['HS256'])
        log.info("in auth, token decoded {}".format(decoded_token))
        return decoded_token
    except:
        # return Response(body={"message":f"unable to decode token.{e.args[0]}"},status_code = 400)
        log.info("unauthorized raising error")
        raise UnauthorizedError


@auth_app.authorizer()
def jwt_auth(auth_request):
    """
    handles authentication using jwt token
    :param auth_request:
    :return: aws policy statement
    """

    print("request info",auth_request.token)

    token = auth_request.token
    log.info("decoding auth token")
    try:
        decoded = decode_jwt_token(token)
        if not decoded:
            print("returning error as unauthorized")
            return Response(body={"message":"unable to decode token"},status_code=401)



        log.info(f'decoded the token {decoded}')

        return AuthResponse(routes=["*"], principal_id=decoded["email"],
                        context={"sessionId": decoded["sessionId"], "email": decoded["email"],"role":decoded["role"], "userId": decoded["userId"],
                                 "firstName": decoded["firstName"],"lastName": decoded["lastName"]
                            , "token": decoded["token"], })
    except Exception as e:
        return {"message": f"unable to decode token.{e.args[0]}"}



