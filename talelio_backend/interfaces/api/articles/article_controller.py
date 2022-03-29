from typing import Tuple, cast

from flask import Blueprint, Response, request

from talelio_backend.app_article.use_cases.create_article import create_article
from talelio_backend.app_article.use_cases.get_articles import get_article
from talelio_backend.core.exceptions import AuthorizationError
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.identity_and_access.authorization import authorization_required
from talelio_backend.interfaces.api.articles.article_serializer import ArticleSchema
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.interfaces.api.utils import extract_access_token_from_authorization_header

articles_v1 = Blueprint('articles_v1', __name__)


@articles_v1.post('')
def create_article_endpoint() -> Tuple[Response, int]:
    authorization_header = request.headers.get('Authorization')

    @authorization_required(authorization_header)
    def protected_create_article_endpoint() -> Tuple[Response, int]:
        try:
            if not request.json:
                raise APIError('Missing request body', 400)

            access_token = extract_access_token_from_authorization_header(
                cast(str, authorization_header))
            uow = UnitOfWork()

            user = Authentication().get_jwt_identity(access_token)
            user_id = int(user['user_id'])
            title = request.json['title']
            body = request.json['body']

            # Allows for an optional featured_image request parameter
            # withour raising the KeyError exception if not provided.
            featured_image = str(request.json.get('featured_image' or ''))

            created_article = create_article(uow, user_id, title, body, featured_image)
            res_body = ArticleSchema().dump(created_article)

            return res_body, 201
        except KeyError as error:
            raise APIError(f'Expected {error} key', 400) from error

    try:
        return protected_create_article_endpoint()
    except AuthorizationError as error:
        raise APIError(str(error), 403) from error


@articles_v1.get('/<string:slug>')
def get_article_endpoint(slug: str) -> Tuple[Response, int]:
    uow = UnitOfWork()

    article = get_article(uow, slug)
    res_body = ArticleSchema().dump(article)

    return res_body, 200
