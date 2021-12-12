import os
import json
import unittest
import pytest
from random import randrange

from run_server import app, wipe_keys
from constants import *

@pytest.mark.integrationtest
class KeysPresentTests(unittest.TestCase):

    # NOTE: check the test cases before changing the value here
    STARTER_DATA = {
        "abc1": "value1",
        "abc2": "test1",
        "abc3": "test2",
        "xyz1": "newvalue1",
        "xyz2": "value2"
    }

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)
        wipe_keys()
        for each_key, each_value in self.STARTER_DATA.items():
            self.app.post('/set', data=json.dumps({
                "key_name": each_key,
                "key_value": each_value
            }), follow_redirects=True)


################# TESTS #################
    ##### Get All keys #####
    def test_get_all_keys_present(self):

        _EXPECTED_GET_ALL_KEYS_RESPONSE = {
            "body": {
                "keys": self.STARTER_DATA
            },
            "status_code": SUCCESS_RESPONSE_STATUS_CODE,
            "success": True
        }
        response = self.app.get('/get', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_ALL_KEYS_RESPONSE)

    ##### Get Specific Key Test #####
    def test_get_sepcific_key_present_not_found(self):
        _key_id = "nokeyid"
        _EXPECTED_GET_SPECIFIC_KEYS_NOT_FOUND_RESPONSE = {
            "body": KEY_NOT_FOUND_MESSAGE.format(_key_id),
            "status_code": KEY_NOT_FOUND_STATUS_CODE,
            "success": False
        }
        response = self.app.get(f'/get/{_key_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SPECIFIC_KEYS_NOT_FOUND_RESPONSE)

    def test_get_sepcific_key_present_found(self):
        _key_id = list(self.STARTER_DATA.keys())[
            randrange(len(self.STARTER_DATA))]
        _EXPECTED_GET_SPECIFIC_KEYS_FOUND_RESPONSE = {
            "body": {'value': self.STARTER_DATA[_key_id]},
            "status_code": SUCCESS_RESPONSE_STATUS_CODE,
            "success": True
        }
        response = self.app.get(f'/get/{_key_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SPECIFIC_KEYS_FOUND_RESPONSE)

    ##### Prefix test #####
    def test_get_search_prefix_keys_empty_not_found(self):

        _EXPECTED_GET_SEARCH_PREFIX_KEYS_NOT_FOUND_RESPONSE = {
            "body": SEARCH_KEY_NOT_FOUND_MESSAGE,
            "status_code": SEARCH_KEY_NOT_FOUND_STATUS_CODE,
            "success": False
        }
        response = self.app.get('/search?prefix=nokey', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SEARCH_PREFIX_KEYS_NOT_FOUND_RESPONSE)

    def test_get_search_prefix_keys_empty_found(self):
        key_prefix = "ab"
        _EXPECTED_GET_SEARCH_PREFIX_KEYS_EMPTY_RESPONSE = {
            "body": {"keys": ["abc1", "abc2", "abc3"]},
            "status_code": 200,
            "success": True
        }
        response = self.app.get(
            f'/search?prefix={key_prefix}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SEARCH_PREFIX_KEYS_EMPTY_RESPONSE)

    ##### suffix test #####
    def test_get_search_suffix_keys_empty_not_found(self):

        _EXPECTED_GET_SEARCH_SUFFIX_KEYS_NOT_FOUND_RESPONSE = {
            "body": SEARCH_KEY_NOT_FOUND_MESSAGE,
            "status_code": SEARCH_KEY_NOT_FOUND_STATUS_CODE,
            "success": False
        }
        response = self.app.get('/search?suffix=nokey', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SEARCH_SUFFIX_KEYS_NOT_FOUND_RESPONSE)

    def test_get_search_suffix_keys_empty_found(self):
        key_suffix = "2"
        _EXPECTED_GET_SEARCH_SUFFIX_KEYS_EMPTY_RESPONSE = {
            "body": {"keys": ["abc2", "xyz2"]},
            "status_code": 200,
            "success": True
        }
        response = self.app.get(
            f'/search?suffix={key_suffix}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SEARCH_SUFFIX_KEYS_EMPTY_RESPONSE)

    ##### prefix and suffix test #####
    def test_get_search_prefix_suffix_keys_empty_not_found(self):

        _EXPECTED_GET_SEARCH_PREFIX_SUFFIX_KEYS_NOT_FOUND_RESPONSE = {
            "body": SEARCH_KEY_NOT_FOUND_MESSAGE,
            "status_code": SEARCH_KEY_NOT_FOUND_STATUS_CODE,
            "success": False
        }
        response = self.app.get(
            '/search?prefix=pre&suffix=suf', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SEARCH_PREFIX_SUFFIX_KEYS_NOT_FOUND_RESPONSE)

    def test_get_search_prefix_suffix_keys_empty_found(self):
        key_suffix = "2"
        key_prefix = "xy"
        _EXPECTED_GET_SEARCH_PREFIX_SUFFIX_KEYS_EMPTY_RESPONSE = {
            "body": {"keys": ["xyz2"]},
            "status_code": 200,
            "success": True
        }
        response = self.app.get(
            f'/search?suffix={key_suffix}&prefix={key_prefix}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         _EXPECTED_GET_SEARCH_PREFIX_SUFFIX_KEYS_EMPTY_RESPONSE)
