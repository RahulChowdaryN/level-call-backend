from boto3.dynamodb.conditions import Attr
import logging
log = logging.getLogger("audit-feedback")



class DynamoDBAudit:
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def list_items_by_mail(self, email):

        response = self._table.scan(
            FilterExpression=Attr('email').eq(email),
            ProjectionExpression='email,#nm,#tp,session_id',
            ExpressionAttributeNames={'#nm': 'name', '#tp': 'type'}
        )
        return response['Items']

    def add_item(self, audit_event):

        self._table.put_item(Item=audit_event)

        return True

    def get_session_item(self, session_id):

        response = self._table.scan(
            FilterExpression=Attr('sessionId').eq(session_id),
            ProjectionExpression = 'sessionId,#ts,#st,statusId',
            ExpressionAttributeNames = {'#ts': 'timestamp', '#st': 'status'}
        )

        if response['Count'] < 1:
            return {}
        return response['Items']

    def get_user_item(self, user_id):

        response = self._table.scan(
            FilterExpression=Attr('userId').eq(user_id),
            ProjectionExpression = 'userId,#ts,#tp,roleId',
            ExpressionAttributeNames = {'#ts': 'timestamp', '#tp': 'type'}
        )
        log.info(response,"response")
        if response['Count'] < 1:
            return {}
        return response['Items']

    def delete_item(self, session_id):
        response = self._table.scan(
            FilterExpression=Attr('session_id').eq(session_id)
        )
        if response['Count'] < 1:
            return {}

        student_uid = response['Items'][0]['uid']
        tutor_uid = response['Items'][1]['uid']

        self._table.delete_item(
            Key={
                'uid': tutor_uid
            }
        )
        self._table.delete_item(
            Key={
                'uid': student_uid
            }
        )

        return

    def update_item(self, body):
        # We could also use update_item() with an UpdateExpression.
        response = self._table.scan(
            FilterExpression=Attr('session_id').eq(body['session_id'])
        )

        student_record = {'uid': response['Items'][0]['uid'], 'name': body['users']['students'][0]['name'],
                          'email': body['users']['students'][0]['email'], 'session_id': body['session_id'],
                          'type': "student"}

        tutor_record = {'uid': response['Items'][1]['uid'], 'name': body['users']['tutor']['name'],
                        'email': body['users']['tutor']['email'], 'type': "tutor", 'session_id': body['session_id']}
        self._table.put_item(
            Item=student_record
        )

        self._table.put_item(
            Item=tutor_record
        )
        return student_record['uid']



