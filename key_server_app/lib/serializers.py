from flask import Response, jsonify
import json
# These are custom implemented serializers


def check_set_request(req):
    req_data = json.loads(req.decode('utf-8'))
    if 'key_name' in req_data and 'key_value' in req_data:
        return req_data
    else:
        raise Exception("Request is missing required params.", 400)


def check_search_request(req):
    if {"prefix", "suffix"}.intersection(set(req.args.keys())):
      print("valid search request received.")
      return req.args
    else:
        raise Exception("Search request is missing required queryparams.", 400)


def generate_response(message, state: bool, status_code=200):
    _response = {
        "status_code": status_code,
        "body": message,
        "success": state
    }

    return jsonify(_response), status_code
