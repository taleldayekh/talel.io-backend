import json
from typing import Tuple, Union, cast

from flask import Blueprint, Response, jsonify, request

from talelio_backend.app_article.use_cases.get_articles import get_articles_for_user
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.interfaces.api.articles.article_serializer import SerializeArticles
from talelio_backend.interfaces.api.errors import APIError

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
