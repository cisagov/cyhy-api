"""CyHy API Server."""

from datetime import timedelta
import pprint

from flask import Flask, request
from flask_jwt_extended import JWTManager, decode_token
from flask_cors import CORS

from .util import load_config, connect_from_config
from .schema import Schema
from .model import UserModel


def load_secret(filename="/run/secrets/flask.key"):
    """Load a secret key from file."""
    print(f"Reading secret key from {filename}")
    with open(filename, "r") as stream:
        key = stream.read()
    return key


def create_app(config, secret_filename=None):
    """Create the Flask application."""
    app = Flask(__name__)
    # copy configurations into the application
    app.config["SECRET_KEY"] = app.config["JWT_SECRET_KEY"] = load_secret(
        secret_filename
    )
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
        **config["tokens"]["refresh-expire"]
    )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        **config["tokens"]["access-expire"]
    )
    app.config["JWT_TOKEN_LOCATION"] = config["tokens"]["location"]
    app.config["GRAPHIQL"] = config["graphiql"]
    app.config["CYHY_MAIL_SERVERS"] = config["mail-servers"]
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

    if app.config["DEBUG"]:
        app.logger.debug("application config\n" + pprint.pformat(app.config))
    return app


def main():
    """Start the application."""
    # import IPython; IPython.embed()  # noqa: E702 <<< BREAKPOINT >>>
    config = load_config()
    secret_filename = config.get("secret-key-file")
    app = create_app(config, secret_filename)
    connect_from_config(config)
    app.run(host=config["listen"]["interface"], port=config["listen"]["port"])


if __name__ == "__main__":
    main()
