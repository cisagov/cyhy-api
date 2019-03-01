import graphene

from cyhy_api.model import UserModel
from ..fields import ResponseMessageField


class RegisterMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    result = graphene.Field(ResponseMessageField)

    @staticmethod
    def mutate(root, info, username, password):
        user = UserModel()
        user.username = username
        user.password = password
        user.save()

        return RegisterMutation(
            ResponseMessageField(
                is_success=True, message="Successfully registered"
            )
        )
