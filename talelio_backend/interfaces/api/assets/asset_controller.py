from typing import Tuple

from boto3 import client
from flask import Blueprint, Response, current_app, jsonify, request

from talelio_backend.app_assets.data.asset_store import AssetStore
from talelio_backend.app_assets.use_cases.upload_images import upload_images
from talelio_backend.core.exceptions import AuthorizationError, ImageError
from talelio_backend.identity_and_access.authentication import get_jwt_identity
from talelio_backend.identity_and_access.authorization import authorization_required
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.interfaces.api.utils import (extract_access_token_from_authorization_header,
                                                  get_streams_from_request_files)

assets_v1 = Blueprint('assets_v1', __name__)


@assets_v1.post('/images')
def upload_images_endpoint() -> Tuple[Response, int]:
    authorization_header = request.headers.get('Authorization')

    @authorization_required(authorization_header)
    def protected() -> Tuple[Response, int]:
        try:
            if not authorization_header:
                raise AuthorizationError('No authorization header provided')

            access_token = extract_access_token_from_authorization_header(authorization_header)
            user = get_jwt_identity(access_token)

            asset_store = AssetStore()
            image_streams = get_streams_from_request_files(request.files)
            user_id = int(user['user_id'])
            bucket = current_app.config['S3_BUCKET']

            image_objects_urls = upload_images(asset_store, image_streams, user_id, bucket)

            return jsonify(image_objects_urls), 200
        except ImageError as error:
            raise APIError(str(error), 400) from error
        except client('s3').exceptions.ClientError as error:
            raise APIError(str(error), 400) from error

    try:
        return protected()
    except AuthorizationError as error:
        raise APIError(str(error), 403) from error
