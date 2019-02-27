from uuid import uuid4

import graphene
from flask_graphql_auth import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    mutation_jwt_refresh_token_required,
)

from cyhy_api.model import UserModel
from ..unions.mutation import AuthUnion, RefreshUnion
from ..fields import AuthField, RefreshField, ResponseMessageField


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    result = graphene.Field(AuthUnion)

    def mutate(self, info, **kwargs):
        user = UserModel.objects(username=kwargs["username"]).first()

        if user is not None and user.password == kwargs["password"]:
            access_token = create_access_token(identity=kwargs["username"])
            refresh_token = create_refresh_token(identity=str(uuid4()))
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
    class Arguments:
        refresh_token = graphene.String()

    result = graphene.Field(RefreshUnion)

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, info):
        return RefreshMutation(
            RefreshField(
                access_token=create_access_token(get_jwt_identity()),
                message="Refresh success",
            )
        )
