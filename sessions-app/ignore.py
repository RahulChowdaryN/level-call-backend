# client  = boto3.client('dynamodb')
#
#
# response = client.scan(
#
#     ExpressionAttributeValues={
#         ':a': {
#             'S': "9db2cf78-5b68-4264-9e28-e3619df4ab84",
#         },
#     },
#     FilterExpression='session_id = :a',
#   #  ProjectionExpression='#id',
#     TableName="users"
# )
#
# print(response)
#
#
# import boto3
# from boto3.dynamodb.conditions import Attr

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('session')
#

# print(response)
# user_data = response['Items']
# #
# session_data = {}
# session_data['users'] = [{user_data[0]['type']+'s': {'name': user_data[0]['name'], 'email': user_data[0]['email']}},
#                          {user_data[1]['type']: {'name': user_data[1]['name'], 'email': user_data[1]['email']}}]

# print(session_data)
# table = dynamodb.Table('session')
# # response = table.scan(
# #            # Key = { 'students.email':'test@co'}
# #            FilterExpression=Attr('students[0].email').eq('test@co')
# #
# #         )
# session_id_list = ['98f4421e-386c-4e57-8577-68ddd0559f5f', 'dee86e52-4a36-4b0f-bd86-eddb1683acce',
#                    'f754124d-a38d-4f22-a466-8d68d1c66a82', 'f754124d-a38d-4f22-a466-8d68d1c66a82',
#                    'dee86e52-4a36-4b0f-bd86-eddb1683acce', '98f4421e-386c-4e57-8577-68ddd0559f5f']
# response1 = table.scan(
#
#     FilterExpression=Attr('session_id').is_in(session_id_list)
# )
#
# print(response1)

# response = table.scan(
#  FilterExpression=Attr('tutor.name').eq("tutor1")
# )
#
# print(response)










#
# @app.route('/api/session/{session_id}', methods=['GET'], authorizer=jwt_auth)
# def get_session_by_id(session_id):
#     session_data = get_session_db().get_item(session_id)
#     if len(session_data) > 1:
#         return session_data
#     return {"message": "session details not found"}
#
#
# @app.route('/api/session', methods=['GET'], authorizer=jwt_auth)
# def get_session():
#     session_id = get_authorized_session_id(app.current_request)
#     print(session_id)
#     session_data = get_session_db().get_item(session_id)
#
#     if len(session_data) > 1:
#         return {"message": session_data}
#     return {"message": "session details not found"}
#
#
# @app.route('/api/session/upcoming', methods=['GET'], authorizer=jwt_auth)
# def get_upcoming_sessions():
#     body = app.current_request.json_body
#     user_email = get_authorized_email(app.current_request)
#     # if not body and not body.get('email', False):
#     #     return {'message': 'email is missing'}
#
#    # user_email = body['email']
#
#     user_session_data = get_user_db().list_items_by_mail(user_email)
#     print(user_session_data)
#     if len(user_session_data) <= 0:
#         return {"message": "no upcoming sessions"}
#     session_id_list = []
#     for each_session in user_session_data:
#         session_id_list.append(each_session['session_id'])
#
#     print(session_id_list)
#     session_details = get_session_db().list_items_mail(session_id_list)
#     print("session details", session_details)
#     return {"message": session_details}
#
#
# @app.route('/api/session/{session_id}', methods=['PUT'], authorizer=jwt_auth)
# def update_session(session_id):
#     body = app.current_request.json_body
#     body['session_id'] = session_id
#     body['status'] = "rescheduled"
#     get_session_db().update_item(body)
#
#     return {"message": "session updated successfully"}
#
#
# @app.route('/api/session/{session_id}', methods=['DELETE'], authorizer=jwt_auth)
# def delete_session(session_id):
#     get_user_db().delete_item(session_id)
#     get_session_db().delete_item(session_id)
#     return {"message": "session deleted successfully"}
#
#
# @app.route('/api/session/course', methods=['POST'], authorizer=jwt_auth)
# def get_sessions_course():
#     body = app.current_request.json_body
#     email = get_authorized_email(app.current_request)
#     if not body or not body.get('course_id', False):
#         return {"message": "course_id is required"}
#     #  get_user_db().delete_item(session_id)
#     user_session_data = get_user_db().list_items_by_mail(email)
#
#     print(user_session_data)
#     if len(user_session_data) <= 0:
#         return {"message": "no upcoming sessions"}
#     session_id_list = []
#     for each_session in user_session_data:
#         session_id_list.append(each_session['session_id'])
#
#     print(session_id_list)
#     session_details = get_session_db().list_items_course(session_id_list, body['course_id'])
#     # for session in session_details:
#     #     session['Name'] = session['session_name']
#     #     del session['session_name']
#     print("session details", session_details)
#     return {"message": session_details}
#
# def rocket_chat_account(username,password,email):
#     import requests
#     import json
#     ROCKETCHAT_URL ="https://rocketchat.mylevelapp.com"
#
#     login_end_point = "/api/v1/login"
#     user_valid_end_point = "/api/v1/users.info"
#     create_user_end_point = "/api/v1/users.create"
#
#     headers = {
#      'X-Auth-Token': 'aovXdUpWM-7bLVeFw0yQHow50O29scOqIMTlive3ljO',
#      'X-User-Id': 'fBiE4qkjgsx9c4fo5',
#      'Content-Type': 'application/json'
#     }
#     login_params = {'username': 'rahul3'}
#     print(ROCKETCHAT_URL + user_valid_end_point)
#     response = requests.request("GET", ROCKETCHAT_URL + user_valid_end_point, headers=headers,params=login_params)
#     print(response.json())
#     if not response.json()['success']:
#        print("creating user in")
#        try:
#            payload = {"name": "rahul3", "username": "rahul3", "email": "rnama3@umbc.edu", "password": "rahul3","verified": True}
#            response = requests.request("POST", ROCKETCHAT_URL+create_user_end_point, headers=headers, data=json.dumps(payload))
#            print(response.json()['success'])
#            if not response.json()['success']:
#                return {"status":False,"message":response.json()}
#        except Exception as e:
#            print(e.args)
#            return json.dumps({"message":e.args[0],"status":False})
#     print("logging in")
#     user_payload = {"user":"rnama3@umbc.edu","password":"rahul3"}
#     response = requests.request("POST", ROCKETCHAT_URL+login_end_point, headers=headers, data=json.dumps(user_payload)).json()
#     print(response)
#     if response["status"] != "success":
#         return {"status":False,"message":response}
#     response = {"authToken":response["data"]["authToken"],"userId":response["data"]["userId"],"status":True}
#     return response
#
#
# print(rocket_chat_account("rnama","rnama","rnama"))

# @session_app.route('/api/session/join', methods=['POST'], cors=global_auth.cors_config)
# def login():
#     """"
#     function to handle authentication. generates a jet token
#     :returns jwt token and session data (dict)
#     """
#     body = session_app.current_request.json_body
#     if not body:
#         return {'message': 'token is required'}
#     log.info(f"received session join request with {body['token']}")
#
#     if not body.get('token'):
#         return {'message': 'token is required'}
#     current_user = global_db_handler.get_user_db().validate_token(body['token'])
#     log.info(f"response from db call for token  {body['token']} ")
#     print("response",current_user)
#     if len(current_user['Items']) <= 0:
#         log.info("no session found with token")
#         return {'message': 'no session found', 'code': 'session_not_found'}
#
#     session_id = current_user['Items'][0]['sessionId']
#
#     session_users = global_db_handler.get_user_db().get_item_by_session_id(session_id)
#     print("session_users",session_users)
#
#     session_only_details = global_db_handler.get_session_db().get_session_details(session_id)
#
#     students = []
#     tutor = {}
#
#     for each_item in session_users:
#         if each_item["role"] == "student":
#             students.append(each_item)
#         else:
#             tutor = each_item
#
#     session_only_details["students"] = students
#     session_only_details["tutor"] = tutor
#     response = {"token": "token","sessionDetails":session_only_details,"user":current_user['Items'][0]}


#
# current_session_details = global_db_handler.get_session_db().get_item(response['Items'][0]['sessionId'])
#
# log.info(f'current session details for the token{current_session_details}')
# body['email'] = response['Items'][0]['email']
#
# body['sessionDetails'] = {'email': body['email'], 'firstName': response['Items'][0]['firstName'],'lastName':
# response['Items'][0]['lastName'], 'token': body['token'], 'role': response['Items'][0]['role'], 'userId': response[
# 'Items'][0]['uid'], 'sessionId': response['Items'][0]['sessionId']} # session_id = response['Items'][0][
# 'sessionId'] log.info('generating authentication token using jwt') jwt_token = auth.get_jwt_token(body[
# 'sessionDetails']) log.info('token generated, returning response ') # session_role_type = user_roles() # # role_id
# = None # # for each_role in session_role_type: # #     if each_role["name"] == "IN-PROGRESS": # #         role_id =
# each_role["roleId"] # #         break
#
# session_audit_payload = {"sessionId": response['Items'][0]['sessionId'], "statusId": 3, "status": "IN_PROGRESS",
# "timestamp": str(datetime.utcnow())} user_audit_payload = {"userId": response['Items'][0]['uid'], "roleId": 3,
# "status": "JOINED", "timestamp": str(datetime.utcnow()), 'email': body['email']} session_status_payload = {
# "sessionId": response['Items'][0]['sessionId'], "status": "IN_PROGRESS"} audit_controller.update_audit("session",
# session_audit_payload) audit_controller.update_audit("user", user_audit_payload) update_session_status(
# session_status_payload) return {'token': jwt_token, 'sessionDetails': current_session_details,
# 'user': {'firstName': response['Items'][0]['firstName'],'lastName': response['Items'][0]['lastName'],
# 'email': response['Items'][0]['email'], 'phoneNumber': response['Items'][0]['phoneNumber'], 'profilePicUrl':
# response['Items'][0]['profilePicUrl']}}

# return response