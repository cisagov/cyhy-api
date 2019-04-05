import graphene

from graphene.relay import Node
from cyhy_api.model import UserModel


class UserField(graphene.ObjectType):
    uid = graphene.String()
    email = graphene.String()
    password = graphene.String()  # TODO remove, here just for play

    class Meta:
        name = "User"
        interfaces = (Node,)

    @classmethod
    def get_node(cls, info, uid):
        user = UserModel.objects(uid=uid).first()
        return UserField(uid=user.uid, email=user.email, password=user.password)
