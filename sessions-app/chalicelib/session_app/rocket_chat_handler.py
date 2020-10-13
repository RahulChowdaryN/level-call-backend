# import requests
# import json
# from chalice import Response
# from chalice import Blueprint
# from chalicelib import global_auth, auth
# import os
# import logging
#
#
# log = logging.getLogger("sessions-app")
#
# ROCKETCHAT_URL = os.environ['ROCKETCHAT_URL']
#
# rocket_chat = Blueprint(__name__)
#
# login_end_point = "/api/v1/login"
# user_valid_end_point = "/api/v1/users.info"
# create_user_end_point = "/api/v1/users.create"
# headers = {
#     'X-Auth-Token': os.environ['ROCKETCHAT_X_Auth_Token'],
#     'X-User-Id': os.environ['ROCKETCHAT_X_User_Id'],
#     'Content-Type': 'application/json'
# }
#
#
# def rocket_chat_account(firstname, email, password):
#     username = email[:email.find('@')]
#     login_params = {'username': username}
#     print(ROCKETCHAT_URL + user_valid_end_point)
#     response = requests.request("GET", ROCKETCHAT_URL + user_valid_end_point, headers=headers, params=login_params)
#     log.info(response.json())
#     if not response.json()['success']:
#         log.info("creating user in")
#         try:
#             payload = {"name": firstname, "username": username, "email": email, "password": password, "verified": True}
#             response = requests.request("POST", ROCKETCHAT_URL + create_user_end_point, headers=headers,
#                                         data=json.dumps(payload))
#             log.info(response.json()['success'])
#             if not response.json()['success']:
#                 return {"status": False, "message": response.json()}
#         except Exception as e:
#             print(e.args)
#             return json.dumps({"message": e.args[0], "status": False})
#     log.debug("logging in")
#     user_payload = {"user": email, "password": password}
#     try:
#         response = requests.request("POST", ROCKETCHAT_URL + login_end_point, headers=headers,
#                                     data=json.dumps(user_payload)).json()
#         log.info(response)
#         if response["status"] != "success":
#             return {"status": False, "message": response}
#         response = {"rocketChatAuthToken": response["data"]["authToken"],
#                     "rocketChatUserId": response["data"]["userId"], "status": True}
#         return response
#     except Exception as e:
#         log.info("exception while handling rocket chat")
#         return {"status": False, "message": e.args[0]}
#
# @rocket_chat.route('/api/session/iframe', methods=['GET'], cors=global_auth.cors_config)
# def rocket_chat_iframe():
#     try:
#         print("request body",rocket_chat.current_request)
#         auth_cookie = rocket_chat.current_request.headers['Cookie']
#         chatToken = auth_cookie[auth_cookie.find("=") + 1:]
#         return Response(body = "<script>window.parent.postMessage({event:'login-with-token',loginToken: '%s'},"
#                                "'%s'); </script>"%(chatToken,ROCKETCHAT_URL),status_code=200,
#                         headers={'Content-Type':'text/html'})
#     except Exception as e:
#         log.info("exception while generating rocket iframe")
#         return Response(body={"message":f"unable to fetch token from {e.args[0]}"},status_code=400)
#
#
# @rocket_chat.route('/api/session/auth', methods=['GET'], cors=global_auth.cors_config)
# def rocket_chat_auth():
#     print("request body",rocket_chat.current_request.headers)
#     try:
#         auth_cookie = rocket_chat.current_request.headers['Cookie']
#         chatToken = auth_cookie[auth_cookie.find("=")+1:]
#         return Response(body={"loginToken":chatToken},status_code=200)
#
#     except Exception as e:
#         return Response(body={"message":f"unable to fetch token from {e.args[0]}"},status_code=400)
#
#
#
