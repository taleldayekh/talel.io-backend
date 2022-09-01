import json
from typing import Tuple, Union, cast

from flask import Blueprint, Response, jsonify, request

from talelio_backend.app_article.use_cases.get_articles import get_user_with_articles
from talelio_backend.app_project.use_cases.get_projects import get_user_projects
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.interfaces.api.projects.project_serializer import ProjectSchema
from talelio_backend.interfaces.api.users.user_serializers import UserArticlesSchema

users_v1 = Blueprint('users_v1', __name__)


@users_v1.get('/<string:username>/articles')
def get_user_articles_endpoint(username: str) -> Response:
    try:
        uow = UnitOfWork()

        page_param = request.args.get('page')
        limit_param = request.args.get('limit')

        page = int(page_param) if page_param else None
        limit = int(limit_param) if limit_param else None

        user_with_articles = get_user_with_articles(uow, username, page, limit)

        user = cast(User, user_with_articles['user'])
        next_link = cast(Union[str, None], user_with_articles['next_link'])
        prev_link = cast(Union[str, None], user_with_articles['prev_link'])
        next_rel = 'rel="next"'
        prev_rel = 'rel="prev"'

        # TODO: Resolve type error
        res_body = UserArticlesSchema().dump({
            'user': user,
            'articles': user.articles
        }  # type: ignore
                                             )

        res = Response(json.dumps(res_body), status=200, mimetype='application/json')
        res.headers['X-Total-Count'] = cast(int, user_with_articles['total_articles_count'])
        res.headers['Link'] = (f'{"<" + next_link + ">; " + next_rel if next_link else ""}'
                               f'{", " if prev_link and next_link else ""}'
                               f' {"<" + prev_link + ">; " + prev_rel if prev_link else ""}')

        return res
    except ValueError as error:
        raise APIError('Expected numeric query parameters', 400) from error
    except UserError as error:
        raise APIError(str(error), 400) from error


@users_v1.get('/<string:username>/projects')
def get_user_projects_endpoint(username: str) -> Tuple[Response, int]:
    try:
        uow = UnitOfWork()

        user_projects = get_user_projects(uow, username)
        res_body = ProjectSchema(many=True).dump(user_projects)

        return jsonify(res_body), 200
    except UserError as error:
        raise APIError(str(error), 400) from error
