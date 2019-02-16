#!/usr/bin/env pytest -vs
"""Tests for User documents."""

import pprint

import pytest

from cyhy_rest.models import User

PP = pprint.PrettyPrinter(indent=4)


@pytest.fixture(scope="class", autouse=True)
def connection():
    """Create connections for tests to use."""
    from cyhy_rest.util import connect_from_config
    connect_from_config()


class TestUsers:
    """User document tests."""

    def test_creation(self):
        """Create a new user, and save it."""
        user = User()
        user.username = 'lemmy'
        user.save()

    def test_find_one_user(self):
        """Find one user."""
        user = User.objects.find_one_user('lemmy')
        assert user is not None, 'user should not be None'
        assert user.username == 'lemmy', 'user has wrong username'

    def test_set_password_without_save(self):
        """Set user's password without save."""
        user = User()
        user.password = 'is_god'
        assert user.password == 'is_god'

    def test_set_password_with_save(self):
        """Set user's password with save."""
        user = User.objects.find_one_user('lemmy')
        user.password = 'is_god'
        user.save()
        assert user.password == 'is_god'

    def test_check_password(self):
        """Verify user's password."""
        user = User.objects.find_one_user('lemmy')
        assert user.password == 'is_god'
