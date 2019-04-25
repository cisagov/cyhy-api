import graphene


class AccountField(graphene.ObjectType):
    id = graphene.Int(required=True, description="The unique numeric identifier.")
    name = graphene.String(
        required=True, description="The name assigned to this account."
    )

    class Meta:
        description = (
            "An account is a child of an Organization.  "
            "Accounts can be accessed by Users that have the correct "
            "permissions assigned to them."
        )
