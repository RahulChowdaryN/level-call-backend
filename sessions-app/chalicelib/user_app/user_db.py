from boto3.dynamodb.conditions import Attr
import boto3
import logging

log = logging.getLogger('sessions-app')
client = boto3.client('dynamodb')


class DynamoDBUser:
    """ DB Class to handle all the user related queries. """

    def __init__(self, table_resource):
        log.info('connected to user db')
        self._table = table_resource

    def list_all_items(self):
        """
        lists all items from user table
        :param -
        :returns list of all items

        """
        log.info('in userdb, listing all items from users table')
        response = self._table.scan()
        return response['Items']

    def list_items(self, session_id_list):
        """ retrieves items based on a list of ids
        :param session_id_list
        :returns list of matching items

        """
        log.info('in user db listing sessions matching sessions id,')
        response = self._table.scan(
            FilterExpression=Attr('sessionId').is_in(session_id_list),
            ProjectionExpression='email,#nm,#tp,sessionId',
            ExpressionAttributeNames={'#nm': 'name', '#tp': 'type'}
        )
        return response['Items']

    def validate_token(self, token):
        """
        retrieves items matching the token
        :param token (string)
        :returns list of matching items

        """
        log.info('in user db, validating token')
        response = self._table.scan(
            FilterExpression=Attr('token').eq(token),
            ProjectionExpression='sessionId,email,firstName,lastName,phoneNumber,uid,profilePicUrl,#rl,rocketChatPassword,rocketChatAuthToken',
            ExpressionAttributeNames={'#rl': 'role'}
        )
        log.info(f"user found for the token. here is the response {response} {self._table}")

        if len(response['Items']) == 0:
            return []

        return response['Items'][0]

    def list_items_by_mail(self, email):
        """
        retrieves items matching the email
        :param email (string)
        :returns list of matching items

        """
        log.info('in user db, listing all items by email')

        response = self._table.scan(
            FilterExpression=Attr('email').eq(email),
            ProjectionExpression='email,firstName,lastName,#tp,sessionId,rocketChatPassword',
            ExpressionAttributeNames={'#tp': 'type'}
        )
        return response['Items']

    def add_item(self, user_list):
        """ adds list of users to user table
        :param user_list (list)
        :returns list of users added to table

        """
        log.info('in user db, adding item to the user table')

        for user in user_list:
            self._table.put_item(Item=user)

        return user_list

    def get_item(self, session_id):
        """
        retrieves single item matching the session_id
        :param session_id (string)
        :returns list of matching items

        """

        log.info('in user db, retrieving item using session id')

        response = self._table.scan(
            FilterExpression=Attr('sessionId').eq(session_id)
        )

        if response['Count'] < 1:
            return {}
        return response['Items']

    def get_item_by_session_id(self, session_id):
        """
        retrieves single item matching the session_id
        :param session_id (string)
        :returns list of matching items

        """

        log.info('in user db, retrieving item using session id')

        response = self._table.scan(
            FilterExpression=Attr('sessionId').eq(session_id),
            ProjectionExpression='email,firstName,lastName,phoneNumber,#tk,profilePicUrl,#rl,rocketChatPassword',
            ExpressionAttributeNames={'#rl': 'role','#tk':'token'}
        )

        if response['Count'] < 1:
            return {}
        return response['Items']

    def get_user_details(self, user_id):
        """
        retrieves user phone number and email based on user id
        :param session_id (string)
        :returns list of matching items

        """

        log.info(f'in user db, retrieving mail and phone number using user id {user_id}')

        response = self._table.get_item(
            Key={
                'uid': user_id,
            },
            ProjectionExpression='email,phoneNumber'
        )
        print(response)

        if len(response['Item']) < 1:
            return {}
        return response['Item']

    # def delete_item(self, session_id):
    #     """ deletes items matching the sessionid
    #     not using as of now
    #     :param session_id (string)
    #     :returns custom message
    #
    #     """
    #     response = self._table.scan(
    #         FilterExpression=Attr('sessionId').eq(session_id)
    #     )
    #     if response['Count'] < 1:
    #         return {}
    #
    #     student_uid = response['Items'][0]['uid']
    #     tutor_uid = response['Items'][1]['uid']
    #
    #     self._table.delete_item(
    #         Key={
    #             'uid': tutor_uid
    #         }
    #     )
    #     self._table.delete_item(
    #         Key={
    #             'uid': student_uid
    #         }
    #     )
    #
    #     return

    # def update_item(self, body):
    #     """ updates items matching the sessionid
    #     not using as of now
    #     :param body (dict)
    #     :returns uid
    #
    #     """
    #
    #     response = self._table.scan(
    #         FilterExpression=Attr('sessionId').eq(body['sessionId'])
    #     )
    #
    #     student_record = {'uid': response['Items'][0]['uid'], 'firstName': body['users']['students'][0]['firstName'],
    #                       'lastName': body['users']['students'][0]['lastName'],
    #                       'email': body['users']['students'][0]['email'], 'sessionId': body['sessionId'],
    #                       'type': "student"}
    #
    #     tutor_record = {'uid': response['Items'][1]['uid'], 'firstName': body['users']['tutor']['firstName'],
    #                     'lastName': body['users']['tutor']['lastName'],
    #                     'email': body['users']['tutor']['email'], 'type': "tutor", 'sessionId': body['sessionId']}
    #     self._table.put_item(
    #         Item=student_record
    #     )
    #
    #     self._table.put_item(
    #         Item=tutor_record
    #     )
    #     return student_record['uid']
