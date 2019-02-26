import graphene

# from graphene.relay import Node

from .user import resolve_user
from ..unions.query import UserUnion


class Query(graphene.ObjectType):
    # node = Node.Field()
    # all_users = MongoengineConnectionField(User)

    user = graphene.Field(
        type=UserUnion,
        token=graphene.NonNull(graphene.String),
        id=graphene.Int(default_value=None),
        username=graphene.String(default_value=None),
        resolver=resolve_user,
    )
