import graphene

from cyhy_api.model import UserModel
from ..fields import ResponseMessageField


class RegisterMutation(graphene.Mutation):
    class Arguments(object):
        id = graphene.String()
        username = graphene.String()
        password = graphene.String()
        description = graphene.String()

    result = graphene.Field(ResponseMessageField)

    @staticmethod
    def mutate(root, info, **kwargs):
        user = UserModel()
        user.username = kwargs["username"]
        user.password = kwargs["password"]
        user.save()
        # UserModel(**kwargs).save()

        return RegisterMutation(
            ResponseMessageField(
                is_success=True, message="Successfully registered"
            )
        )
