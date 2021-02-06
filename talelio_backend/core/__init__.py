from flask import Flask
from flask_cors import CORS

from talelio_backend.data.orm import start_mappers
from talelio_backend.interfaces.api.user.user_controller import user_v1

start_mappers()


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(user_v1, url_prefix='/v1/user')
    CORS(app)

    return app
