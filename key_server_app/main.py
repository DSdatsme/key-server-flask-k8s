#!/usr/bin/env python3

from flask import Flask, jsonify, request
import threading
import time
from lib import serializers
from lib import key_utils

app = Flask(__name__)

# In-memory store variable.
key_storage = {}


@app.route('/get/<key>', methods=['GET'])
def get_key(key: str):
    """Method to return specific key value based on ID in url.

    Returns:
        [dict]: dict with the value of the key.

    Sample:
      Request:
        GET http://<domain>/get/<keyID>
      Response:
        {
          "body": {
              "value": "idk"
          },
          "status_code": 200,
          "success": true
        }
    """
    global key_storage
    try:
        found_value = key_utils.is_key_present(key_storage, key)
        return serializers.generate_response({"value": found_value}, True)
    except Exception as e:
        return serializers.generate_response(e.args[0], False, e.args[1])


@app.route('/get', methods=['GET'])
def get_all_keys():
    """Method to return all key stored in the process.

    Returns:
        [dict]: dict with all key and value data.

    Sample:
      Request:
        GET http://<domain>/get
      Response:
        {
          "body": {
              "keys": {
                  "key1": "idk",
                  "key2": "passwd"
              }
          },
          "status_code": 200,
          "success": true
        }
    """
    global key_storage
    # blindly return everything
    return serializers.generate_response({"keys": key_storage}, True)


@app.route('/set', methods=['POST'])
def set_key():
    """Method to store key in the flask process.

    Raises:
      Exception: Desired exception with message is raised if input is invalid.

    Returns:
        [dict]: an acknowledgement satating that key was received.

    Sample:
      Request:
        POST http://<domain>/set
          {
            "key_name": "<key ID>",
            "key_value": "<key value>"
          }
        Response:
          {
            "body": "Key created with ID <key ID>",
            "status_code": 201,
            "success": true
          }       
    """
    global key_storage
    try:
        user_data = serializers.check_set_request(request.data)

        # setter for key-value
        key_storage[user_data['key_name']] = user_data['key_value']

        return serializers.generate_response(f"Key created with ID {user_data['key_name']}", True, 201)
    except Exception as e:
        print("Error: Key Creation failed!")
        return serializers.generate_response(e.args[0], False, e.args[1])


@app.route('/search', methods=['GET'])
def search_key():
    """Method to have search key functionality based on prefix and suffix of key ID

    Raises:
        Exception: Desired exception with message is raised if input is invalid or no key is found

    Returns:
        [dict]: returns a dict response with list of keys

    Sample:
      Request:
        GET http://<domain>/search?suffix=<str>&postfix=<str>
      Response:
        {
          "body": {
            "keys": ["key1", "key2", ...]
          },
          "status_code": 200,
          "success": true
        }
    """
    global key_storage
    try:
        user_data = serializers.check_search_request(request)

        # make a clone so that you dont overwrite
        response_data = list(key_storage.copy().keys())

        if user_data.get('prefix'):
            response_data = key_utils.search_key_by_prefix(
                response_data, user_data['prefix'])
        if user_data.get('suffix'):
            response_data = key_utils.search_key_by_suffix(
                response_data, user_data['suffix'])
        if response_data:
            return serializers.generate_response({"keys": response_data}, True)
        else:
            raise Exception("No keys found with the given query", 404)
    except Exception as e:
        print("Error: Key Search failed!")
        return serializers.generate_response(e.args[0], False, e.args[1])


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
