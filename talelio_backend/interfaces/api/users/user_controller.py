import json
import mimetypes
from typing import Tuple, Union, cast

from boto3 import client
from flask import Blueprint, Response, current_app, jsonify, request, send_file

from talelio_backend.app_article.use_cases.get_articles import get_articles_for_user
from talelio_backend.app_assets.data.asset_store import AssetStore
from talelio_backend.app_assets.use_cases.download_image import download_image
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.interfaces.api.articles.article_serializer import SerializeArticles
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.shared.exceptions import UserError

users_v1 = Blueprint('users_v1', __name__)


@users_v1.get('/<string:username>/articles')
def get_user_articles_endpoint(username: str) -> Union[Tuple[Response, int], Response]:
    try:
        uow = UnitOfWork()

        page_param = request.args.get('page')
        limit_param = request.args.get('limit')

        page = int(page_param) if page_param else None
        limit = int(limit_param) if limit_param else None

        articles_for_user = get_articles_for_user(uow, username, page, limit)

        if not 'articles' in articles_for_user:
            return jsonify(articles_for_user), 200

        total_articles_count = cast(str, articles_for_user['total_articles_count'])
        next_link = cast(Union[str, None], articles_for_user['next_link'])
        prev_link = cast(Union[str, None], articles_for_user['prev_link'])
        next_rel = 'rel="next"'
        prev_rel = 'rel="prev"'

        res_body = SerializeArticles().dump({
            'articles': articles_for_user['articles'],
            'user': articles_for_user['user']
        })

        res = Response(json.dumps(res_body), status=200, mimetype='application/json')
        res.headers['X-Total-Count'] = total_articles_count
        res.headers['Link'] = (f'{"<" + next_link + ">; " + next_rel if next_link else ""}'
                               f'{", " if prev_link and next_link else ""}'
                               f' {"<" + prev_link + ">; " + prev_rel if prev_link else ""}')

        return res

    except ValueError as error:
        raise APIError('Expected numeric query parameters', 400) from error


@users_v1.get('/<string:username>/images/<string:image_file_name>')
def get_user_image_endpoint(username: str, image_file_name: str):
    try:
        uow = UnitOfWork()

        asset_store = AssetStore()
        bucket = current_app.config['S3_BUCKET']

        image_file_stream = download_image(uow, asset_store, image_file_name, username, bucket)
        mimetype = mimetypes.guess_type(image_file_name)[0] or 'application/octet-stream'

        res = Response(image_file_stream, status=200, mimetype=mimetype)

        return res
    except UserError as error:
        raise APIError(str(error), 404) from error
    except client('s3').exceptions.ClientError as error:
        raise APIError(str(error), 400) from error
