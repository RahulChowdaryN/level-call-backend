from chalice.config import Config
import os
import json

chalice_config = '.chalice/config.json'
import random
from datetime import datetime

chalice_stage = 'test'


def load_environ(chalice_stage, extra_environ=dict):
    with open(chalice_config, 'r') as config_json:
        stage_variables = Config(
            chalice_stage=chalice_stage,
            config_from_disk=json.loads(config_json.read())).environment_variables
        for k, v in stage_variables.items():
            os.environ[k] = v
    return os.environ


load_environ(chalice_stage)

from app import app
from chalice.test import Client

headers = {'Content-Type': 'application/json',
           'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uSWQiOiI3OWViZGFhZS1mMGMxLTQ3ZWEtYjc3Ni05MmY5NmY2MDI1NjQiLCJlbWFpbCI6InVkYXkucmVkZHlAc3R1ZGVudC5jb20iLCJmaXJzdE5hbWUiOiJVZGF5IiwibGFzdE5hbWUiOiJSZWRkeSIsInRva2VuIjoiNjQwNjAzOGEtZDMxNC00YmY5LWE2NTEtZmFiOGU1NGZhYTk4Iiwicm9sZSI6InN0dWRlbnQiLCJpYXQiOjE1OTc3MjUyMTksIm5iZiI6MTU5NzcyNTIxOSwianRpIjoiODNjOGE3MDQtYWE0NC00MjcyLTk0MGMtZDY2NmM1Y2Y3OGNlIiwidXNlcklkIjoiMDE5ZWIzMWEtZDM5My00MDBlLTgzMjgtNWU4ZGZhM2M3OTYwIn0.-2yz7sKCzFZxU-Ye2BySiSbdJ3zM7Gfe91-6ZiYk1WI'}


def test_index():
    with Client(app) as client:
        response = client.http.get('/')
        assert response.json_body == {'hello': 'world'}


def test_auth():
    with Client(app) as client:
        response = client.http.get('/api/custom-auth')
        assert response.json_body == {"success": True}


def test_roles_controller():
    with Client(app) as client:
        response = client.http.get('/api/rolescontroller')
        assert response.json_body == {'roles': 'controller'}

        response = client.http.get('/api/session/types')
        assert response.status_code == 200
        assert len(response.json_body) >= 7

        response = client.http.get('/api/user/roles')
        assert response.status_code == 200
        assert len(response.json_body) >= 3


def test_audit_controller():
    with Client(app) as client:
        response = client.http.get('/auditcontroller')
        assert response.json_body == {'audit': 'controller'}

        response = client.http.get('/api/audit/user/randomid',headers=headers)
        assert response.status_code == 400

        response = client.http.get('/api/audit/session/randomid',headers=headers)
        assert response.status_code == 400

        response = client.http.post('/api/audit/session',body=json.dumps({}),headers=headers)
        assert response.status_code == 422

        # response = client.http.post('/api/audit/session', body=json.dumps({"status":"COMPLETED"}), headers=headers)
        # assert response.status_code == 200
        # assert response.json_body == {"message": "updated"}
        #
        response = client.http.post('/api/audit/user', body=json.dumps({}), headers=headers)
        assert response.status_code == 422


def test_feedback_controller():
    with Client(app) as client:
        response = client.http.get('/feedbackcontroller')
        assert response.json_body == {'feedback': 'controller'}

        response = client.http.post('/api/feedback')
        assert response.status_code == 422

        response = client.http.post('/api/feedback',body = json.dumps({}),headers=headers)
        assert response.status_code == 422

        response = client.http.get('/api/feedback/randomid',body=json.dumps({}),headers=headers)
        assert response.status_code == 400






