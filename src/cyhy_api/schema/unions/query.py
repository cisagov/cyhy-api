from ..fields import UserField, ResponseMessageField

from flask_graphql_auth import AuthInfoField
import graphene


class UserResults(graphene.ObjectType):
    users = graphene.List(of_type=UserField)


class UserUnion(graphene.Union):
    class Meta:
        types = (UserResults, ResponseMessageField, AuthInfoField)
