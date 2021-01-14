# mypy: ignore-errors
from flask import Flask
from flask_cors import CORS

from talelio_backend.interfaces.api.user.user_controller import user_v1


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(user_v1, url_prefix='/')

    return app
