from chalicelib.audit_app import audit_db
from chalicelib.roles import roles_db
from chalicelib.session_app import session_db
from chalicelib.user_app import user_db
import os
from boto3 import resource
import logging

log = logging.getLogger("sessions-app")

_DB = None
_USER_DB = None
_ROLES_DB = None
_USER_ROLES_DB = None
_USER_ROLES = None
_SESSION_ROLES= None


def get_user_db():
    """
    connects to user table. global variable
    :return: connection

    """
    log.info('connecting to user table')
    global _USER_DB
    if _USER_DB is None:
        _USER_DB = user_db.DynamoDBUser(
            resource('dynamodb').Table(
                os.environ['USERS_TABLE_NAME'])
        )
    log.info('connected to user table')
    return _USER_DB


def get_session_db():
    """
    connects to session table. global variable
    :return: connection

    """
    log.info('connecting to session table')
    global _DB
    if _DB is None:
        _DB = session_db.DynamoDBSession(
            resource('dynamodb').Table(
                os.environ['SESSION_TABLE_NAME'])
        )
    log.info('connected to session table')
    return _DB


def get_session_roles_db():
    """
    connects to session roles table. global variable
    :return: connection

    """
    log.info('connecting to session-roles table')
    global _ROLES_DB
    if _ROLES_DB is None:
        _ROLES_DB = roles_db.DynamoDBRoles(
            resource('dynamodb').Table(
                os.environ['SESSION_ROLES_TABLE_NAME'])
        )
    log.info('connected to session-roles table')
    return _ROLES_DB


def get_user_roles_db():
    """
    connects to session roles table. global variable
    :return: connection

    """
    log.info('connecting to user-roles table')
    global _USER_ROLES_DB
    if _USER_ROLES_DB is None:
        _USER_ROLES_DB = roles_db.DynamoDBRoles(
            resource('dynamodb').Table(
                os.environ['USER_ROLES_TABLE_NAME'])
        )
    log.info('connected to session-roles table')
    return _USER_ROLES_DB



def replace_decimals(obj):
    import decimal
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj:
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj