"""GraphQL Schema definition."""

import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from .models import User as UserModel


class User(MongoengineObjectType):

    class Meta:
        model = UserModel
        interfaces = (Node, )
        exclude_fields = ['_password']


class Query(graphene.ObjectType):
    node = Node.Field()
    all_users = MongoengineConnectionField(User)


schema = graphene.Schema(query=Query, types=[User])
