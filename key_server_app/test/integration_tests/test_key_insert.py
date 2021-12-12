import os
import json
import unittest
import pytest

from run_server import app, wipe_keys
from constants import *


@pytest.mark.integrationtest
class EmptyKeysTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)
        wipe_keys()

    def tearDown(self):
      pass

    @classmethod
    def tearDownClass(cls):
      del cls
################# TESTS #################
    def test_put_key(self):
        key_name = "testkeyname"
        key_value = "testvalue"
        _EXPECTED_GET_ALL_KEYS_EMPTY_RESPONSE = {
            "body": SUCCESS_KEY_INSERT_RESPONSE_MESSAGE.format(key_name),
            "status_code": SUCCESS_KEY_INSERT_RESPONSE_STATUS_CODE,
            "success": True
        }
        response = self.app.post('/set', data=json.dumps({
            "key_name": key_name,
            "key_value": key_value
        }), follow_redirects=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_ALL_KEYS_EMPTY_RESPONSE)
