from schema import Schema, Optional, SchemaError, SchemaMissingKeyError, SchemaUnexpectedTypeError
import json
import logging

log = logging.getLogger('sessions-app')


def validate_session(body):
    try:
        body = json.dumps(body)
        log.info("in session validation, validating session in validations")
        Schema({'name': str, 'description': str, 'courseId': int, 'scheduledTime': str, 'students': [
            {'email': str, 'firstName': str, 'lastName': str, Optional('phoneNumber'): str,
             Optional('profilePicUrl'): str}],
                'tutor': {'email': str, 'firstName': str, 'lastName': str, Optional('phoneNumber'): str,
                          Optional('profilePicUrl'): str}, 'duration': int}).validate(json.loads(body))
        log.info('in session validation, validation done')
        return True
    except SchemaMissingKeyError as e:
        log.info("in validate_session schema missing exception while validation {}".format(e.args))
        return json.dumps({"message": e.args[0]})
    except Exception as e:
        log.info("in validate_session exception while validation {}".format(e.args))
        return json.dumps({"message": e.args[0]})

#
# def validate_openvidu(body):
#     try:
#         body = json.dumps(body)
#         log.info(f"in session validation, validating openvidu body in validations {body}")
#         Schema({'name': str, 'email': str, 'isMobile': bool, 'screenShare': bool}).validate(json.loads(body))
#         log.info('in session validation, validation done')
#         return True
#     except Exception as e:
#         log.info("in validate_session exception while validation {}".format(e.args))
#         return json.dumps({"message": e.args[0]})
