from boto3.dynamodb.conditions import Attr
import logging

log = logging.getLogger("audit-feedback")


class DynamoDBFeedback:
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']


    def add_item(self, feedback_item):
        self._table.put_item(
            Item=feedback_item

        )
        return feedback_item['uid']


    def get_item(self, session_id):
        response = self._table.scan(
            FilterExpression=Attr('sessionId').eq(session_id),
            ProjectionExpression = 'note,#em,#ts,rating',
            ExpressionAttributeNames = {'#em': 'email','#ts':'timestamp'}
        )

        log.info(f"response {response}")
        if response.get('Items', False):
            return response['Items']
        return {}

    def delete_item(self, session_id):
        self._table.delete_item(
            Key={
                'sessionId': session_id
            }
        )
        return

    def update_item(self, body):
        # We could also use update_item() with an UpdateExpression.

        # item = self.get_item(body['session_id'])
        #
        # if body.get('start_time', False):
        #     item['start_time'] = body['start_time']
        #
        # if body.get('course_id', False):
        #     item['course_id'] = body['course_id']
        #
        # if body.get('duration', False):
        #     item['duration'] = body['duration']
        #
        # if body.get('end_time', False):
        #     item['end_time'] = body['end_time']

        self._table.put_item(Item=body)




