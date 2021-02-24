from os import getenv

from flask import Flask
from flask_cors import CORS  # type: ignore

from talelio_backend.data.orm import start_mappers
from talelio_backend.interfaces.api.account.account_controller import account_v1
from talelio_backend.interfaces.api.errors import error_handlers

start_mappers()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('talelio_backend.config.config.Production' if getenv('ENV') ==
                           'production' else 'talelio_backend.config.config.Development')
    app.register_blueprint(account_v1, url_prefix='/v1/account')

    CORS(app)
    error_handlers(app)

    return app
