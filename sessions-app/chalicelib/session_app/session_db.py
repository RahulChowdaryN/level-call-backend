from boto3.dynamodb.conditions import Attr
import logging

log = logging.getLogger('sessions-app')


class DynamoDBSession:
    """ DB Class to handle all the session related queries. """

    def __init__(self, table_resource):
        log.info('connected to session db')
        self._table = table_resource

    def list_all_items(self):
        """
        lists all items from session table
        :param -
        :returns list of all items

        """
        log.info('listing all items from sessions table')
        response = self._table.scan()
        return response['Items']

    def list_items_by_course_id(self, course_id):
        """
        lists of all items matching course_id
        :param - course_id (int)
        :returns list of all items

        """
        log.info("in session db, listing items by course id")
        response = self._table.scan(
            FilterExpression=Attr('courseId').eq(course_id),
            ProjectionExpression='courseId,scheduledTime,#dur,sessionId,#nm,description,students,tutor,#st',
            ExpressionAttributeNames={'#dur': 'duration', '#st': 'status', '#nm': 'name'}
        )
        return response['Items']

    def add_item(self, session_record):
        """
        adds a session to user table
        :param session_record (dict)
        :returns session_id (string)

        """
        log.info('in sessions db, adding session item to table')
        print(session_record)
        self._table.put_item(
            Item=session_record

        )
        return session_record['sessionId']

    def list_items_mail(self, session_id_list):

        """
        retrieves sessions matching the email
        :param email (string)
        :returns list of matching items

        """
        log.info('in sessions db, listing all the sessions by email')

        response = self._table.scan(

            FilterExpression=Attr('sessionId').is_in(session_id_list),
            # & Attr('start_time').gte(str(datetime.utcnow())),
            ProjectionExpression='courseId,#dr,#nm,description,scheduledTime,students,tutor,#st',
            ExpressionAttributeNames={'#dr': 'duration', '#st': 'status', '#nm': 'name'}
        )
        return response['Items']

    def list_items_course(self, session_id_list, course_id):
        """
        retrieves sessions matching the course id and session ids
        :param session_id_list (list), course_id (int)
        :returns list of matching items

        """

        log.info('in sessions db, listing all the sessions by course')
        response = self._table.scan(
            FilterExpression=Attr('sessionId').is_in(session_id_list) & Attr('courseId').eq(course_id),
            # & Attr('start_time').gte(str(datetime.utcnow())),
            ProjectionExpression='courseId,#dr,#nm,description,scheduledTime,students,tutor,#st',
            ExpressionAttributeNames={'#dr': 'duration', '#st': 'status', '#nm': 'name'}
        )
        return response['Items']

    def validate_token(self, token):
        """
        retrieves items matching the token
        :param token (string)
        :returns list of matching items

        """
        log.info('in sessions db, validating the token from table')
        response = self._table.scan(
            FilterExpression=Attr('token').eq(token),
            ProjectionExpression='sessionId'
        )

        return response

    def get_item(self, session_id):
        """
        retrieves single item matching the session_id
        :param session_id (string)
        :returns list of matching items

        """
        log.info('in sessions db, getting the session based on session_Id')
        response = self._table.get_item(
            Key={
                'sessionId': session_id,
            },
            ProjectionExpression='sessionId,courseId,description,scheduledTime,#dur,#nm,#st,students,tutor',
            ExpressionAttributeNames={'#dur': 'duration', '#st': 'status', '#nm': 'name'}
        )

        if response.get('Item', False):
            return response['Item']
        return {}

    def get_session_details(self, session_id):
        """
        retrieves single item matching the session_id
        :param session_id (string)
        :returns list of matching items

        """
        log.info('in sessions db, getting the session details based on session_Id')
        response = self._table.get_item(
            Key={
                'sessionId': session_id,
            },
            ProjectionExpression='sessionId,courseId,description,scheduledTime,#dur,#nm,#st',
            ExpressionAttributeNames={'#dur': 'duration', '#st': 'status', '#nm': 'name'}
        )

        if response.get('Item', False):
            return response['Item']
        return {}

    def get_user_details(self, session_id,user_type):
        """
        retrieves single item matching the session_id
        :param session_id (string)
        :returns list of matching items

        """
        log.info('in sessions db, getting the session based on session_Id')
        if user_type == "tutor":
            projection_expression = "tutor.email,tutor.phoneNumber,tutor.firstName"
        else:
            projection_expression = "students"

        response = self._table.get_item(
            Key={
                'sessionId': session_id,
            },
            ProjectionExpression=projection_expression
        )

        if response.get('Item', False):
            return response['Item']
        return {}

    def get_item_details(self, session_id):
        """
        retrieves single item matching the session_id
        :param session_id (string)
        :returns list of matching items

        """
        log.info('in sessions db, getting the session based on session_Id')
        response = self._table.get_item(
            Key={
                'sessionId': session_id,
            },
            ProjectionExpression='courseId,scheduledTime,description,#dur,#nm,#st,students,tutor,profilePicUrl',
            ExpressionAttributeNames={'#dur': 'duration', '#st': 'status', '#nm': 'name'}

        )

        if response.get('Item', False):
            return response['Item']
        return {}

    def delete_item(self, session_id):
        """
        not using as of now
        :param session_id:
        :return:
        """
        self._table.delete_item(
            Key={
                'sessionId': session_id
            }
        )

        return

    def update_item(self,body):
        """
        not using as of now
        :param body:
        :return:
        """
        response = self._table.update_item(
            Key={
                'sessionId': body['sessionId']
            },
            UpdateExpression="set #st=:r",
            ExpressionAttributeValues={
                ':r': body['status']
            },
           ExpressionAttributeNames={
           "#st": "status"
           },
            ReturnValues="UPDATED_NEW"
        )
        return response['Attributes']

    def update_duration(self,body):
        """
        not using as of now
        :param body:
        :return:
        """
        response = self._table.update_item(
            Key={
                'sessionId': body['sessionId']
            },
            UpdateExpression="set #dr= #dr + :val",
            ExpressionAttributeValues={
                ':val': body['duration']
            },
           ExpressionAttributeNames={
           "#dr": "duration"
           },
            ReturnValues="UPDATED_NEW"
        )
        return response['Attributes']

