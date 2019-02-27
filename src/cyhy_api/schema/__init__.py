import graphene
from flask_graphql import GraphQLView

from .mutations import Mutation
from .queries import Query


schema = graphene.Schema(query=Query, mutation=Mutation)


class Schema:
    def __init__(self, app):
        app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view(
                "graphql", schema=schema, graphiql=app.config["GRAPHIQL"]
            ),
        )
        print(
            f"[INFO] GraphQLView was successfully added "
            f'with GraphiQL:{app.config["GRAPHIQL"]}'
        )
