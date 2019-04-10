"""CyHy API Server."""

from datetime import timedelta
import pprint

from flask import Flask, request
from flask_jwt_extended import JWTManager, decode_token
from flask_cors import CORS

from .util import connect_from_config
from .schema import Schema
from .model import UserModel


def load_secret(app, filename="/run/secrets/flask.key"):
    """Load a secret key from file."""
    print(f"Reading secret key from {filename}")
    with open(filename, "r") as stream:
        key = stream.read()
    app.secret_key = key


def create_app():
    """Create the Flask application."""
    app = Flask(__name__)
    load_secret(app)
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_TOKEN_LOCATION"] = ("headers", "cookies")
    app.config["DEBUG"] = True
    app.config["GRAPHIQL"] = True
    Schema(app)
    jwt = JWTManager(app)
    CORS(app)  # TODO define specific origin

    @jwt.user_loader_callback_loader
    def user_loader(uid):
        app.logger.debug(f"Looking up user with uid: {uid}")
        user = UserModel.objects(id=uid).first()
        if user:
            app.logger.debug(f"Found user: {user.email}")
            return user
        else:
            app.logger.warn(f"Could not find a user with uid: {uid}")
            return None

    @app.before_request
    def log_request():
        # app.logger.debug("Request Headers %s", request.headers)
        if "Authorization" in request.headers:
            header_value = request.headers.get("Authorization")
            if header_value:
                bearer, token = header_value.split()
                app.logger.debug(
                    pprint.pformat(decode_token(token, allow_expired=True))
                )
        return None

    return app


def main():
    """Start the application."""
    # import IPython; IPython.embed()  # noqa: E702 <<< BREAKPOINT >>>
    app = create_app()
    connect_from_config()
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
