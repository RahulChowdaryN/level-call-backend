from boto3.dynamodb.conditions import Attr


class DynamoDBRoles:
    def __init__(self, table_resource):

        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def add_item(self, roles_list):
        with self._table.batch_writer() as batch:
            for each_role in roles_list:
                batch.put_item(
                    Item=(each_role)
                )
        return True

    def get_item(self, session_id):

        response = self._table.scan(
            FilterExpression=Attr('session_id').eq(session_id)
        )

        if response['Count'] < 1:
            return {}
        return response['Items']






