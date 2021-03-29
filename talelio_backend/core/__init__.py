from os import getenv

from flask import Flask
from flask_cors import CORS  # type: ignore

from talelio_backend.data.orm import start_mappers
from talelio_backend.interfaces.api.accounts.account_controller import accounts_v1
from talelio_backend.interfaces.api.errors import error_handlers
from talelio_backend.interfaces.api.users.user_controller import users_v1

start_mappers()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('talelio_backend.config.config.Production' if getenv('ENV') ==
                           'production' else 'talelio_backend.config.config.Development')

    app.register_blueprint(accounts_v1, url_prefix='/v1/accounts')
    app.register_blueprint(users_v1, url_prefix='/v1/users')

    CORS(app, resources={r'/*': app.config['CORS_ORIGIN_WHITELIST']})
    error_handlers(app)

    return app
