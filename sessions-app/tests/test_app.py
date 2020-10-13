from chalice.config import Config
import os
import json

chalice_config = '.chalice/config-test.json'
import random
from datetime import datetime

chalice_stage = "test"


def load_environ(chalice_stage, extra_environ=dict):
    with open(chalice_config, 'r') as config_json:
        stage_variables = Config(
            chalice_stage=chalice_stage,
            config_from_disk=json.loads(config_json.read())).environment_variables
        for k, v in stage_variables.items():
            print(k,v)
            os.environ[k] = v
    return os.environ


load_environ(chalice_stage)


from app import app
from chalice.test import Client

headers = {'Content-Type': 'application/json',
           'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uSWQiOiI3OWViZGFhZS1mMGMxLTQ3ZWEtYjc3Ni05MmY5NmY2MDI1NjQiLCJlbWFpbCI6InVkYXkucmVkZHlAc3R1ZGVudC5jb20iLCJmaXJzdE5hbWUiOiJVZGF5IiwibGFzdE5hbWUiOiJSZWRkeSIsInRva2VuIjoiNjQwNjAzOGEtZDMxNC00YmY5LWE2NTEtZmFiOGU1NGZhYTk4Iiwicm9sZSI6InN0dWRlbnQiLCJpYXQiOjE1OTc2MTQ4ODAsIm5iZiI6MTU5NzYxNDg4MCwianRpIjoiOGFkODk1NjgtNGQ3Ny00ODc4LWI3ZTMtMDM2ZTJhM2YyYThlIiwidXNlcklkIjoiMDE5ZWIzMWEtZDM5My00MDBlLTgzMjgtNWU4ZGZhM2M3OTYwIn0.G7kHC6bx0a2WX4zSYrPyyJCWnTRYKgozP_IEvisf6oc'}

headers_no_auth = {'Content-Type': 'application/json'}
def test_index():
    with Client(app) as client:
        response = client.http.get('/')
        assert response.json_body == {'hello': 'world'}


def test_session_controller():
    with Client(app) as client:
        response = client.http.get('/api/session_controller')
        assert response.json_body == {'session': 'controller'}


def test_session_join():
    with Client(app) as client:
        response = client.http.post('/api/session/join',
                                    body=json.dumps({"token": "6406038a-d314-4bf9-a651-fab8e54faa98"}), headers = headers_no_auth)
        assert response.status_code == 200

        response = client.http.post('/api/session/join',
                                    body=json.dumps({"tokn": "388f7b5d-754a-4586-943a-fcbb1cd3c58c"}), headers = headers_no_auth)
        assert response.status_code == 422

        response = client.http.post('/api/session/join', body=json.dumps({"token": "388f7b5d-754a-4586-943a-fcbbd3c5"}),headers=headers_no_auth)
        assert response.status_code == 400


# def test_session_schedule():
#     payload = dict(courseId=random.randint(1, 999), tutor={
#         "firstName": "Suchitra",
#         "lastName": "Reddy",
#         "phoneNumber": "9876543210",
#         "profilePicUrl": "https://s3url.com",
#         "email": "suchitra.reddy@tutor.com"
#     }, duration=random.choice([60, 90, 45, 120]), name="Meditation", description="science",
#                    scheduledTime=str(datetime.utcnow()), students=[
#             {
#                 "firstName": "Rahul",
#                 "lastName": "Nama",
#                 "phoneNumber": "9876543210",
#                 "profilePicUrl": "https://s3url.com",
#                 "email": "rahul.nama@student.com"
#             },
#             {
#                 "firstName": "Uday",
#                 "lastName": "Reddy",
#                 "phoneNumber": "9876543204",
#                 "profilePicUrl": "https://3url.com",
#                 "email": "uday.reddy@student.com"
#             }
#         ])
#     with Client(app) as client:
#         response = client.http.post('/api/session/schedule', body=json.dumps(payload), headers=headers)
#         assert response.status_code == 200
#         del payload["courseId"]
#         response = client.http.post('/api/session/schedule', body=json.dumps(payload), headers=headers)
#         assert response.status_code == 422
#         response = client.http.post('/api/session/schedule', body=json.dumps({}), headers=headers)
#         assert response.status_code == 422

#
# def test_get_session():
#     with Client(app) as client:
#         response = client.http.post('/api/session', body=json.dumps({
#             "sessionId": "d4687e48-285d-43c5-ae6b-09ef12e3a70"
#         }), headers=headers)
#         assert response.status_code == 200
#         assert response.json_body == {}
#
#         response = client.http.post('/api/session', body=json.dumps({
#             "sessionId": "4d18e52a-6fd3-4833-8c48-97f24efef41b"
#         }), headers=headers)
#         assert response.status_code == 200
#         response = client.http.post('/api/session', body=json.dumps({}), headers=headers)
#         assert response.status_code == 422
#         response = client.http.post('/api/session', body=json.dumps({"email": "random@gmail"}), headers=headers)
#         assert response.status_code == 200
#         assert response.json_body == []
#         response = client.http.post('/api/session', body=json.dumps({"email": "suchitra.reddy@tutor.com"}),
#                                     headers=headers)
#         assert response.status_code == 200
#         assert len(response.json_body) >= 1
#
#         response = client.http.post('/api/session', body=json.dumps({"courseId": 131}), headers=headers)
#         assert response.status_code == 200
#
#         response = client.http.post('/api/session', body=json.dumps({"courseId": 1000}), headers=headers)
#         assert response.status_code == 200
#         assert response.json_body == []
#
#
# def test_end_session():
#     with Client(app) as client:
#         response = client.http.get('/api/session/end')
#         assert response.status_code == 401
#
#         response = client.http.get('/api/session/end', headers=headers)
#         assert response.status_code == 200
#
#         # response = client.http.post('api/session',body = json.dumps("")headers = headers)
#
#
# def test_openvidu():
#     with Client(app) as client:
#         response = client.http.post('/api/session/openvidu', headers=headers)
#         assert response.status_code == 400
#         payload = {
#             "name": "Test",
#             "email": "Test",
#             "isMobile": True,
#             "screenShare": True
#         }
#         response = client.http.post('/api/session/openvidu', body=json.dumps(payload),headers=headers)
#         assert response.status_code == 200
#         assert "id" in response.json_body.keys()
#
#
# def test_update_status():
#     with Client(app) as client:
#         response = client.http.post('/api/status/update', headers=headers)
#         assert response.status_code == 400
#         body = {
#             "name": "Test",
#             "email": "Test",
#             "isMobile": True,
#             "screenShare": True
#         }
#         response = client.http.post('/api/status/update', body=json.dumps(body), headers=headers)
#         assert response.status_code == 422
#         body = {'status': 'completed'}
#         response = client.http.post('/api/status/update', body=json.dumps(body), headers=headers)
#         assert response.status_code == 200
#
#
# def test_session_extend():
#     with Client(app) as client:
#         response = client.http.post('/api/session/extend', headers=headers)
#         assert response.status_code == 400
#         body = {
#             "name": "Test",
#             "email": "Test",
#             "isMobile": True,
#             "screenShare": True
#         }
#         response = client.http.post('/api/session/extend', body=json.dumps(body), headers=headers)
#         assert response.status_code == 422
#         body = {'duration': 40}
#         response = client.http.post('/api/session/extend', body=json.dumps(body), headers=headers)
#         assert response.status_code == 200
#         assert "duration" in response.json_body.keys()
#
#
# def test_session_jwt():
#     with Client(app) as client:
#         response = client.http.get('/api/testjwt')
#         assert response.status_code == 401
#
#         response = client.http.get('/api/testjwt', headers=headers)
#         assert response.status_code == 200
#
#
# def test_session_notify():
#     with Client(app) as client:
#         response = client.http.get('/api/notify')
#         assert response.status_code == 401
#
#         response = client.http.get('/api/notify', headers=headers)
#         assert response.status_code == 202
#
#
# def test_user_controller():
#     with Client(app) as client:
#         response = client.http.get('/api/user_controller')
#         assert response.json_body == {'user':'controller'}
#
#
# def test_roles_controller():
#     with Client(app) as client:
#         response = client.http.get('/api/roles_controller')
#         assert response.json_body == {'roles':'controller'}
#
#
#         response = client.http.get('/api/session/types')
#         assert response.status_code == 200
#         assert len(response.json_body) >= 7
#
#
#         response = client.http.get('/api/user/roles')
#         assert response.status_code == 200
#         assert len(response.json_body) >= 3
#
#
#
#
#
#
#
#



# def test_app_controller(monkeypatch):
#     monkeypatch.setattr(app, "index", {"session": "controller"})
#     assert app.index == {"session": "controller"}
#
#
# def test_app_auth(monkeypatch):
#     monkeypatch.setattr(app, "needs_auth", True)
#     assert app.needs_auth == True
#
#
# def test_session_controller(monkeypatch):
#     # apply the monkeypatch for requests.get to mock_get
#     monkeypatch.setattr(session_controller,"index", {"session": "controller"})
#
#     assert session_controller.index == {"session": "controller"}
