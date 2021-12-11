from flask import Response, jsonify
import json
# These are custom implemented serializers
from constants import SUCCESS_RESPONSE_STATUS_CODE, BAD_REQUEST_STATUS_CODE, SEARCH_INVAILD_REQUEST_MESSAGE, BAD_REQUEST_PARAMS_MISSING_MESSAGE, SEARCH_INVAILD_REQUEST_STATUS_CODE


def check_set_request(req):
    req_data = json.loads(req.decode('utf-8'))
    if 'key_name' in req_data and 'key_value' in req_data:
        return req_data
    else:
        raise Exception(BAD_REQUEST_PARAMS_MISSING_MESSAGE,
                        BAD_REQUEST_STATUS_CODE)


def check_search_request(req):
    if {"prefix", "suffix"}.intersection(set(req.args.keys())):
        print("valid search request received.")
        return req.args
    else:
        raise Exception(SEARCH_INVAILD_REQUEST_MESSAGE,
                        SEARCH_INVAILD_REQUEST_STATUS_CODE)


def generate_response(message, state: bool, status_code=SUCCESS_RESPONSE_STATUS_CODE):
    _response = {
        "status_code": status_code,
        "body": message,
        "success": state
    }

    return jsonify(_response), status_code
