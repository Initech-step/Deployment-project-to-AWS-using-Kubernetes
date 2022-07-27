'''
Tests for jwt flask app.
'''
import os
import json
import pytest

import main

#get env variables and set fallbacks
#this is so that in case the env variables arent set, it wont result in error

SECRET = os.environ.get('SECRET', 'fallbacksecret')
TOKEN = os.environ.get('TOKEN', 'fallbacktoken')
EMAIL = os.environ.get('EMAIL', 'fallbackemail@gmail.com')
PASSWORD = os.environ.get('PASSWORD', 'fallbackpassword')

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'
    assert False


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None
