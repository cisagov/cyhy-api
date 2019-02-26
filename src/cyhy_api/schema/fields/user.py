import graphene

# from graphene.relay import Node

# class UserField(MongoengineObjectType):
#
#     class Meta:
#         model = UserModel
#         interfaces = (Node, )
#         exclude_fields = ['_password']


class UserField(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()  # TODO remove, here just for play
