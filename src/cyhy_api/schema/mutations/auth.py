import graphene
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
)

from cyhy_api.model import UserModel
from ..unions.mutation import AuthUnion
from ..fields import AuthField, RefreshField, ResponseMessageField


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)

    result = graphene.Field(AuthUnion)

    def mutate(self, info, username, password, **kwargs):
        user = UserModel.objects(username=username).first()

        if user is not None and user.password == password:
            access_token = create_access_token(identity=username, fresh=True)
            refresh_token = create_refresh_token(identity=username)
            return AuthMutation(
                AuthField(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    message="Login Success",
                )
            )
        else:
            return AuthMutation(
                ResponseMessageField(is_success=False, message="Login failed")
            )


class RefreshMutation(graphene.Mutation):
    result = graphene.Field(RefreshField)

    @jwt_refresh_token_required
    def mutate(self, info):
        return RefreshMutation(
            RefreshField(
                access_token=create_access_token(
                    get_jwt_identity(), fresh=False
                ),
                message="Refresh success",
            )
        )
