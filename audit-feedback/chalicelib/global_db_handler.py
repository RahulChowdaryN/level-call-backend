from chalicelib.audit_app import audit_db
from chalicelib.feedback_app import feedback_db
from chalicelib.roles import roles_db
from boto3 import resource
import os
import logging
log = logging.getLogger("audit-feedback")


_USER_AUDIT_DB = None
_SESSION_AUDIT_DB = None
_FEEDBACK_DB = None
_USER_ROLES_DB = None
_SESSION_ROLES_DB = None
_USER_ROLES = None
_SESSION_ROLES = None


def get_feedback_db():
    global _FEEDBACK_DB
    if _FEEDBACK_DB is None:
        _FEEDBACK_DB = feedback_db.DynamoDBFeedback(
            resource('dynamodb').Table(
                os.environ['FEEDBACK_TABLE_NAME'])
        )
    return _FEEDBACK_DB


def get_session_audit_db():
    global _SESSION_AUDIT_DB
    if _SESSION_AUDIT_DB is None:
        _SESSION_AUDIT_DB = audit_db.DynamoDBAudit(
            resource('dynamodb').Table(
                os.environ['SESSION_AUDIT_TABLE_NAME'])
        )
    return _SESSION_AUDIT_DB


def get_user_audit_db():
    global _USER_AUDIT_DB
    if _USER_AUDIT_DB is None:
        _USER_AUDIT_DB = audit_db.DynamoDBAudit(
            resource('dynamodb').Table(
                os.environ['USER_AUDIT_TABLE_NAME'])
        )
    return _USER_AUDIT_DB


def get_session_roles_db():
    """
    connects to session roles table. global variable
    :return: connection

    """
    log.info('connecting to session-roles table')
    global _SESSION_ROLES_DB
    if _SESSION_ROLES_DB is None:
        _SESSION_ROLES_DB = roles_db.DynamoDBRoles(
            resource('dynamodb').Table(
                os.environ['SESSION_ROLES_TABLE_NAME'])
        )
    log.info('connected to session-roles table')
    return _SESSION_ROLES_DB


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