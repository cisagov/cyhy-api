import graphene

from ..fields import ResponseMessageField, AuthField


# class ResponseUnion(graphene.Union):
#     class Meta:
#         types = (ResponseMessageField,)
#
#     @classmethod
#     def resolve_type(cls, instance, info):
#         return type(instance)


class AuthUnion(graphene.Union):
    class Meta:
        types = (AuthField, ResponseMessageField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


# class RefreshUnion(graphene.Union):
#     class Meta:
#         types = (RefreshField, ResponseMessageField)
#
#     @classmethod
#     def resolve_type(cls, instance, info):
#         return type(instance)
