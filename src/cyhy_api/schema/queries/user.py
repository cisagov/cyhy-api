from cyhy_api.model import UserModel
from ..fields import UserField, ResponseMessageField
from ..unions.query import UserResults

from flask_graphql_auth import query_jwt_required


@query_jwt_required
def resolve_user(root, info, **kwargs):
    username = kwargs.get("username", None)

    if username:
        users = UserModel.objects(username=username)
    else:
        users = UserModel.objects()

    if users.count() == 0:
        return ResponseMessageField(is_success=False, message="Not found")

    return UserResults(
        users=[
            UserField(username=user.username, password=user.password)
            for user in users
        ]
    )
