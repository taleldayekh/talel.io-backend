from typing import Any

from flask import Blueprint, jsonify

user_v1 = Blueprint('user_v1', __name__)


@user_v1.route('/', methods=['GET'])
def user() -> Any:
    user_response = {'message': 'talel.io API'}
    return jsonify(user_response), 200