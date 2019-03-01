import graphene

from graphene.relay import Node
from cyhy_api.model import UserModel


class UserField(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()  # TODO remove, here just for play

    class Meta:
        name = "User"
        interfaces = (Node,)

    @classmethod
    def get_node(cls, info, id):
        user = UserModel.objects(username=id).first()
        return UserField(
            username=user.username, password=user.password, id=user.username
        )
