import graphene

from graphene.relay import Node

from .user import resolve_user
from .viewer import resolve_viewer
from ..fields import UserField


class Query(graphene.ObjectType):
    node = Node.Field()
    # all_users = MongoengineConnectionField(User)

    viewer = graphene.Field(
        type=graphene.NonNull(UserField),
        resolver=resolve_viewer,
        description="The currently authenticated user.",
    )

    user = graphene.Field(
        type=graphene.List(UserField),
        username=graphene.String(default_value=None),
        resolver=resolve_user,
    )
