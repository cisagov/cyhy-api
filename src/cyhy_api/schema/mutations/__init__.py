import graphene

from .auth import AuthMutation, RefreshMutation, LogoutMutation
from .register import RegisterMutation

__all__ = ["AuthMutation", "RefreshMutation", "RegisterMutation", "LogoutMutation"]


class Mutation(graphene.ObjectType):
    register = RegisterMutation.Field()
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()
    logout = LogoutMutation.Field()
