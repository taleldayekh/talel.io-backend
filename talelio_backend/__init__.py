from os import getenv

from flask import Flask
from flask_cors import CORS  # type: ignore

from talelio_backend.data.db_tables import create_db_tables
from talelio_backend.interfaces.api.accounts.account_controller import accounts_v1
from talelio_backend.interfaces.api.articles.article_controller import articles_v1
from talelio_backend.interfaces.api.assets.asset_controller import assets_v1
from talelio_backend.interfaces.api.errors import error_handlers
from talelio_backend.interfaces.api.health.health_controller import health_v1
from talelio_backend.interfaces.api.users.user_controller import users_v1

create_db_tables_connection = create_db_tables()
create_db_tables_connection.close()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('talelio_backend.config.config.Production' if getenv('ENV') ==
                           'production' else 'talelio_backend.config.config.Development')

    app.register_blueprint(health_v1, url_prefix='/v1/health')
    app.register_blueprint(accounts_v1, url_prefix='/v1/accounts')
    app.register_blueprint(articles_v1, url_prefix='/v1/articles')
    app.register_blueprint(assets_v1, url_prefix='/v1/assets')
    app.register_blueprint(users_v1, url_prefix='/v1/users')

    CORS(app, resources={r'/*': app.config['CORS_ORIGIN_WHITELIST']}, supports_credentials=True)
    error_handlers(app)

    return app
