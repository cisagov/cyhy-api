import graphene

from cyhy_api.model import UserModel
from ..fields import ResponseMessageField


class RegisterMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    result = graphene.Field(ResponseMessageField)

    @staticmethod
    def mutate(root, info, email, password, first_name, last_name):
        user = UserModel()
        user.email = email
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return RegisterMutation(
            ResponseMessageField(is_success=True, message="Successfully registered")
        )
