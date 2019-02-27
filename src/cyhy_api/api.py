"""CyHy API Server."""

from flask import Flask
from flask_graphql_auth import GraphQLAuth

from .util import connect_from_config
from .schema import Schema


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
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 30
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 10
    app.config["DEBUG"] = True
    app.config["GRAPHIQL"] = True
    Schema(app)
    GraphQLAuth(app)
    return app


def main():
    """Start the application."""
    # import IPython; IPython.embed()  # noqa: E702 <<< BREAKPOINT >>>
    app = create_app()
    connect_from_config()
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
