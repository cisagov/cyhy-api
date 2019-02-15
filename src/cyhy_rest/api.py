"""CyHy REST API Server."""

from flask import Flask, g, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth

from .models import User
from .util import connect_from_config

app = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('task')


# Set the secret key to some random bytes. Keep this really secret!
# TODO get from secret yml
app.secret_key = b'_1#y3L"Q4T8z\n\xbc]/'

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


@auth.verify_password
def verify_password(username_or_token, password):
    """Verify a username:password or token."""
    # first try to authenticate by token
    user = User.objects.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.objects.find_one_user(username_or_token)
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


class Token(Resource):
    """Allow a user to request a token for use instead of username:password."""

    @auth.login_required
    def get(self):
        """Return a new token for an authenticated user."""
        token = g.user.generate_auth_token(600)
        return jsonify({'token': token.decode('ascii'), 'duration': 600})


class Todo(Resource):
    """Handle a single Todo items."""

    def _abort_if_todo_doesnt_exist(self, todo_id):
        if todo_id not in TODOS:
            abort(404, message="Todo {} doesn't exist".format(todo_id))

    def get(self, todo_id):
        """Return a ToDo by id."""
        self._abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    @auth.login_required
    def delete(self, todo_id):
        """Delete a ToDo by id."""
        self._abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    @auth.login_required
    def put(self, todo_id):
        """Create or update a ToDo."""
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    """Handle lists of Todo items."""

    def get(self):
        """Return the list of all Todos."""
        return TODOS

    @auth.login_required
    def post(self):
        """Add multiple Todo items at once."""
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


# Add routes to the API resources
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Token, '/token')


def main():
    """Start the application."""
    # import IPython; IPython.embed()  # noqa: E702 <<< BREAKPOINT >>>
    connect_from_config()
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
