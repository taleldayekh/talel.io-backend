from flask import Flask

from talel_io.interfaces.api.user.user_controller import user_v1


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(user_v1, url_prefix='/api/v1/user')

    return app
