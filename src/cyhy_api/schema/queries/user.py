from flask_jwt_extended import jwt_required, get_current_user

from cyhy_api.model import UserModel
from ..fields import UserField, ResponseMessageField
from ..unions.query import UserResults


@jwt_required
def resolve_user(root, info, **kwargs):
    whos_asking = get_current_user()
    print(f"WHO'S ASKING!> {whos_asking.username}")
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
