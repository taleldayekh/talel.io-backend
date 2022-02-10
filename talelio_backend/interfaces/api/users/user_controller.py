from typing import Tuple

from flask import Blueprint, Response, jsonify

from talelio_backend.app_article.use_cases.get_articles import get_user_articles
from talelio_backend.app_project.use_cases.get_projects import get_user_projects
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.interfaces.api.articles.article_serializer import ArticleSchema
from talelio_backend.interfaces.api.errors import APIError
from talelio_backend.interfaces.api.projects.project_serializer import ProjectSchema

users_v1 = Blueprint('users_v1', __name__)


@users_v1.get('/<string:username>/articles')
def get_user_articles_endpoint(username: str) -> Tuple[Response, int]:
    try:
        uow = UnitOfWork()

        user_articles = get_user_articles(uow, username)
        res_body = ArticleSchema(many=True).dump(user_articles)

        return jsonify(res_body), 200
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
