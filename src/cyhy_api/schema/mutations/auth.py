import graphene
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_raw_jwt,
    jwt_refresh_token_required,
)

from cyhy_api.model import UserModel
from ..unions.mutation import AuthUnion, RefreshUnion
from ..fields import AuthField, RefreshField, ResponseMessageField


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)

    result = graphene.Field(AuthUnion)

    def mutate(self, info, email, password, **kwargs):
        user = UserModel.find_user_by_email(email)
        if user is not None and user.password == password:
            access_token = create_access_token(identity=user.uid, fresh=True)
            refresh_token = create_refresh_token(identity=user.uid)
            # store token
            user.add_refresh_token(decode_token(refresh_token))
            user.save()
            return AuthMutation(
                AuthField(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    uid=user.uid,
                    message="Login Success",
                )
            )
        else:
            return AuthMutation(
                ResponseMessageField(is_success=False, message="Login failed")
            )


class RefreshMutation(graphene.Mutation):
    result = graphene.Field(RefreshUnion)

    @jwt_refresh_token_required
    def mutate(self, info):
        user = get_current_user()
        refresh_token = get_raw_jwt()
        # verify that this refresh token has not been revoked
        if user.verify_refresh_token(refresh_token):
            return RefreshMutation(
                RefreshField(
                    access_token=create_access_token(user.uid, fresh=False),
                    uid=user.uid,
                )
            )
        else:
            return RefreshMutation(
                ResponseMessageField(
                    is_success=False, message="Refresh token expired or revoked."
                )
            )


class LogoutMutation(graphene.Mutation):
    result = graphene.Field(ResponseMessageField)

    @jwt_refresh_token_required
    def mutate(self, info):
        user = get_current_user()
        refresh_token = get_raw_jwt()
        success = user.revoke_refresh_token(refresh_token) is not None
        if success:
            user.save()
            return LogoutMutation(
                ResponseMessageField(
                    is_success=True, message="Refresh token revoked.  User logged out."
                )
            )
        else:
            return LogoutMutation(
                ResponseMessageField(
                    is_success=False, message="Unable to revoke refresh token."
                )
            )
