from flask import Blueprint, Response, jsonify

user_v1 = Blueprint('user_v1', __name__)


@user_v1.route('/', methods=['GET'])
def user() -> Response:
    user_response = {'first_name': 'Talel', 'last_name': 'Dayekh'}
    return jsonify(user_response)
