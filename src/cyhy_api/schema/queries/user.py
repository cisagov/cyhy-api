from flask_jwt_extended import jwt_required, get_current_user

from cyhy_api.model import UserModel
from ..fields import UserField


@jwt_required
def resolve_user(root, info, **kwargs):
    whos_asking = get_current_user()
    print(f"WHO'S ASKING!> {whos_asking.username}")
    username = kwargs.get("username", None)

    if username:
        users = UserModel.objects(username=username)
    else:
        users = UserModel.objects()

    return [
        UserField(
            username=user.username, password=user.password, id=user.username
        )
        for user in users
    ]
