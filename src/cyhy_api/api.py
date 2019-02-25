"""CyHy API Server."""

from flask import Flask, g, jsonify, request
from flask_graphql import GraphQLView
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from .models import User
from .util import connect_from_config
from .schema import schema

app = Flask(__name__)
app.config['DEBUG'] = True
jwt = JWTManager(app)


@jwt.unauthorized_loader
def unauthorized_callback(expired_token):
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'No authorization token provided'
    }), 401


@app.route('/token', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if '$' in username:     # TODO scrub username input better
        return jsonify({"msg": "Bad username or password"}), 401

    user = User.find_user_by_username(username)

    if not user or not password == user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route('/whoami', methods=['GET'])
@jwt_required
def whoami():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


def graphql_token_view():
    view = GraphQLView.as_view('graphql',
                               schema=schema,
                               graphiql=bool(app.config.get("DEBUG", False)))
    view = jwt_required(view)  # TODO doesn't fail nicely when no JWT
    return view


app.add_url_rule('/graphql', view_func=graphql_token_view)


def load_secret(filename='/run/secrets/flask.key'):
    """Load a secret key from file."""
    print(f'Reading secret key from {filename}')
    with open(filename, 'r') as stream:
        key = stream.read()
    app.secret_key = key


def main():
    """Start the application."""
    # import IPython; IPython.embed()  # noqa: E702 <<< BREAKPOINT >>>
    load_secret()
    connect_from_config()

    # read and set secret
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
