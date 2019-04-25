#!/usr/bin/env pytest -vs
"""Tests for GraphQL authentication API."""

import pytest
from graphene.test import Client
from cyhy_api.schema import schema
from mongoengine import connect
from cyhy_api.model import UserModel
from cyhy_api.api import create_app
from cyhy_api.util import load_config


@pytest.fixture(scope="class", autouse=True)
def connection():
    """Create connections for tests to use."""
    connect(host="mongomock://localhost", alias="default")


@pytest.fixture(scope="class", autouse=True)
def context():
    """Create the Flask application for use with contexts."""
    config = load_config()
    secret_filename = config.get("secret-key-file")
    app = create_app(config, secret_filename)
    return app.app_context()


@pytest.fixture(scope="class")
def client():
    """Create a client."""
    return Client(schema)


class TestAuth:
    """GraphQL authentication tests."""

    def test_register_mutation(self, client):
        """Test user registration."""
        query = """
                mutation {
                  register(email: "bobbo@pekinggourmet.com", password: "foobar") {
                    result {
                      isSuccess
                      message
                    }
                  }
                }
                """
        executed = client.execute(query)
        # the api says it worked
        assert (
            executed["data"]["register"]["result"]["isSuccess"] is True
        ), "Expected success."
        # let's check the database and see if the user is really there
        user = UserModel.objects(email="bobbo@pekinggourmet.com").first()
        assert user is not None
        assert user.email == "bobbo@pekinggourmet.com"
        assert user.password == "foobar"

    def test_auth_mutation(self, client, context):
        """Test user authentication."""
        query = """
                mutation {
                  auth(email: "bobbo@pekinggourmet.com", password: "foobar") {
                    result {
                      __typename
                      ... on AuthField {
                        accessToken
                        refreshToken
                        message
                      }
                      ... on ResponseMessageField {
                        message
                        isSuccess
                      }
                    }
                  }
                }
                """
        with context:
            executed = client.execute(query)
        print(executed)
        assert (
            executed["data"]["auth"]["result"]["__typename"] == "AuthField"
        ), "Expected an AuthField response."
        assert (
            executed["data"]["auth"]["result"]["accessToken"] is not None
        ), "Expected an accessToken."
        assert (
            executed["data"]["auth"]["result"]["refreshToken"] is not None
        ), "Expected an refreshToken."

        # TODO use the tokens
