from boto3.dynamodb.conditions import Attr
import boto3

client = boto3.client('dynamodb')


# class DynamoDBAudit:
#     def __init__(self, table_resource):
#
#         self._table = table_resource
#
#     def list_all_items(self):
#         response = self._table.scan()
#         return response['Items']
#
#     def list_items_by_mail(self, email):
#
#         response = self._table.scan(
#             FilterExpression=Attr('email').eq(email),
#             ProjectionExpression='email,#nm,#tp,session_id',
#             ExpressionAttributeNames={'#nm': 'name', '#tp': 'type'}
#         )
#         return response['Items']
#
#     def add_item(self, user_list):
#
#         print(len(user_list), "length")
#         for user in user_list:
#             self._table.put_item(Item=user)
#
#         return user_list
#
#     def get_item(self, session_id):
#
#         response = self._table.scan(
#             FilterExpression=Attr('session_id').eq(session_id)
#         )
#
#         if response['Count'] < 1:
#             return {}
#         return response['Items']





