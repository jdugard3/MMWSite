"""
Core API endpoints
"""
from flask import request, jsonify
from . import api
from api.models import User
from api.utils import APIException

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    """
    Example endpoint
    """
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200 