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


################# TESTS #################

    # test all key
    def test_get_all_keys_empty(self):

        _EXPECTED_GET_ALL_KEYS_EMPTY_RESPONSE = {
            "body": {
                "keys": {}
            },
            "status_code": SUCCESS_RESPONSE_STATUS_CODE,
            "success": True
        }
        response = self.app.get('/get', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_ALL_KEYS_EMPTY_RESPONSE)
    
    # test get key value
    def test_get_sepcific_key_empty(self):
        _key_id = "nokeyid"
        _EXPECTED_GET_SPECIFIC_KEYS_EMPTY_RESPONSE = {
            "body": KEY_NOT_FOUND_MESSAGE.format(_key_id),
            "status_code": KEY_NOT_FOUND_STATUS_CODE,
            "success": False
        }
        response = self.app.get(f'/get/{_key_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SPECIFIC_KEYS_EMPTY_RESPONSE)

    # test perfix search key
    def test_get_search_prefix_keys_empty(self):

        _EXPECTED_GET_SEARCH_PREFIX_KEYS_EMPTY_RESPONSE = {
            "body": SEARCH_KEY_NOT_FOUND_MESSAGE,
            "status_code": SEARCH_KEY_NOT_FOUND_STATUS_CODE,
            "success": False
        }
        response = self.app.get('/search?prefix=nokey', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SEARCH_PREFIX_KEYS_EMPTY_RESPONSE)

    # test suffix search key
    def test_get_search_suffix_keys_empty(self):

        _EXPECTED_GET_SEARCH_SUFFIX_KEYS_EMPTY_RESPONSE = {
            "body": SEARCH_KEY_NOT_FOUND_MESSAGE,
            "status_code": SEARCH_KEY_NOT_FOUND_STATUS_CODE,
            "success": False
        }
        response = self.app.get('/search?suffix=nokey', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SEARCH_SUFFIX_KEYS_EMPTY_RESPONSE)
