from flask_jwt_extended import jwt_required, get_current_user

from ..fields import UserField


@jwt_required
def resolve_viewer(root, info, **kwargs):
    user = get_current_user()

    return UserField(email=user.email, password=user.password, id=user.uid)
