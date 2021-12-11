import json
import unittest
import pytest

from run_server import app
from constants import *
from lib.serializers import check_set_request, check_search_request, generate_response


@pytest.mark.unittest
class EmptyKeysTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)


################# TESTS #################
    ##### START check_set_request #####

    def test_check_set_request_success(self):
        req_input = {
            "key_name": "a",
            "key_value": "n"
        }
        encoded_req_input = json.dumps(req_input).encode('utf-8')
        self.assertEqual(check_set_request(encoded_req_input), req_input)

    def test_check_set_request_failure(self):
        req_input = {
            "key_name": "q",
            "key_value_wrong": "w"
        }
        encoded_req_input = json.dumps(req_input).encode('utf-8')

        with self.assertRaises(Exception) as custom_exception:
            check_set_request(encoded_req_input)

        self.assertEqual(
            custom_exception.exception.args[0], BAD_REQUEST_PARAMS_MISSING_MESSAGE)
        self.assertEqual(
            custom_exception.exception.args[1], BAD_REQUEST_STATUS_CODE)
    ##### END check_set_request #####

    ##### START generate_response #####
    def test_generate_response(self):

        # with 2 args
        message_string = "test something"
        with app.app_context():
            method_response, status_code = generate_response(
                message_string,  False)

            self.assertDictEqual(json.loads(method_response.data.decode('utf-8')), {
                "status_code": SUCCESS_RESPONSE_STATUS_CODE,
                "body": message_string,
                "success": False
            })
            self.assertEqual(status_code, SUCCESS_RESPONSE_STATUS_CODE)


            # with 3 args
            message_string = "testing new args"
            method_response, status_code = generate_response(
                message_string,  True, 207)

            self.assertDictEqual(json.loads(method_response.data.decode('utf-8')), {
                "status_code": 207,
                "body": message_string,
                "success": True
            })

    ##### END generate_response #####
