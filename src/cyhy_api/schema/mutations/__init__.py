import graphene

from .auth import AuthMutation, RefreshMutation
from .register import RegisterMutation

__all__ = ["AuthMutation", "RefreshMutation", "RegisterMutation"]


class Mutation(graphene.ObjectType):
    register = RegisterMutation.Field()
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()
