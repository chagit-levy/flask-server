import ast
import unittest

import flask
import requests

import flask_server
from flask_server import Application

from flask_server import Message
import json

from flask_server import app
from flask_server import myApp


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)
    # myApp = Application()
    length = 0
    lengthOf=0
    data = {
        'application_id': 3,
        'session_id': "aaaa",
        'message_id': "mmmm",
        'participants': ["father", "mother"],
        'content': "hi, how are you?"
    }
    data2 = {
        "application_id": 5,
        "session_id": "fff",
        "message_id": "rrr",
        "participants": ["uzi easy", "moshe cohen"],
        "content": "hi, how are you?"
    }

    def test_post_get(self):
        self.length = myApp.get_len()
        url = "http://127.0.0.1:5000/GetMessage/?application_id=3"
        ss = requests.get(url)
        json_data = json.loads(ss.text)
        self.lengthOf = len(json_data)

        with flask_server.app.test_client() as c:
            response = c.post('/AddMessage/', json=self.data)
            assert response.status_code == 200
            response = c.post('/AddMessage/', json=self.data2)
            string = str(response.data)
            res = string.split("'")[1]
            assert res == str(self.length+2)
        self.length += 2

        url = "http://127.0.0.1:5000/GetMessage/?application_id=3"
        ss = requests.get(url)
        json_data = json.loads(ss.text)
        assert len(json_data) == self.lengthOf+1

    def test_get(self):
        # with flask_server.app.test_request_context('/GetMessage/?application_id=1'):
        #     assert flask.request.path == '/GetMessage/'
        #     assert flask.request.args['application_id'] == '1'

        url = "http://127.0.0.1:5000/GetMessage/?application_id=3"
        ss = requests.get(url)
        json_data = json.loads(ss.text)
        assert self.data2 in json_data

    def test_delete(self):
        url = "http://127.0.0.1:5000/GetMessage/?message_id=mmmm"
        ss = requests.get(url)
        json_data = json.loads(ss.text)
        self.lengthOf = len(json_data)

        self.length = myApp.get_len()
        response = app.test_client().delete('/DeleteMessage/?message_id=mmmm')
        string = str(response.data)
        res = string.split("'")[1]
        assert res == str(self.length-self.lengthOf)

        # with app.test_request_context('/DeleteMessage/?message_id=mmmm'):
        #     assert flask.request.path == '/DeleteMessage/'
        #     assert flask.request.args['message_id'] == "mmmm"
        # assert myApp.get_len() == self.length-self.lengthOf


if __name__ == '__main__':
    unittest.main()

