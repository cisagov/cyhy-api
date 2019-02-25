#!/usr/bin/env pytest -vs
"""Tests for User documents."""

import time

import pytest
import mongoengine

from cyhy_rest.models import User, HashedPassword


@pytest.fixture(scope="class", autouse=True)
def connection():
    """Create connections for tests to use."""
    from cyhy_rest.util import connect_from_config
    connect_from_config()


class TestUsers:
    """User document tests."""

    def test_creation_without_password(self):
        """Create a new user, and save it."""
        user = User()
        user.username = 'lemmy'
        with pytest.raises(mongoengine.errors.ValidationError):
            user.save()

    def test_creation_with_password(self):
        """Create a new user, and save it."""
        user = User()
        user.username = 'lemmy'
        user.password = 'is_god'
        user.save()

    def test_find_one_user(self):
        """Find one user."""
        user = User.objects.get(username='lemmy')
        assert user is not None, 'User should not be None.'
        assert user.username == 'lemmy', 'User has wrong username.'

    def test_set_password_without_save(self):
        """Set user's password without save."""
        user = User()
        user.password = 'is_god'
        assert isinstance(user.password, HashedPassword), \
            'password should be hashed'
        assert user.password == 'is_god'

    def test_set_password_with_save(self):
        """Set user's password with save."""
        user = User.objects.get(username='lemmy')
        user.password = 'is_god'
        user.save()
        assert isinstance(user.password, HashedPassword), \
            'password should be hashed'
        assert user.password == 'is_god'

    def test_check_password(self):
        """Verify user's password."""
        user = User.objects.get(username='lemmy')
        assert user.password == 'is_god'

    def test_resave_password(self):
        """Verify user's password."""
        user = User.objects.get(username='lemmy')
        user.save()

    def test_delete(self):
        """Test delete."""
        user = User.objects.get(username='lemmy')
        user.delete()
        with pytest.raises(mongoengine.errors.DoesNotExist):
            user = User.objects.get(username='lemmy')

    def test_user_token(self):
        """Test creation and verification of a token."""
        secret = 'Kevin Spacey is Keyser Söze'
        wrong_secret = 'Darth Vader is Luke\'s Father'
        user = User()
        user.username = 'toki'
        user.password = 'pickel'
        user.save()
        # generate a token that will be valid for one second
        token = user.generate_auth_token(secret, expiration=1)
        user2 = User.verify_auth_token(secret, token)
        assert user == user2, "Equivalent User should have been returned."
        assert user is not user2, "Objects should not be the same (memory)."
        # using the wrong secret should break the verification
        user3 = User.verify_auth_token(wrong_secret, token)
        assert user3 is None, "Token should be invalid."
        # verification after exipration should break the validation
        time.sleep(2)  # wait for token to expired
        user4 = User.verify_auth_token(secret, token)
        assert user4 is None, "Token did not expire properly."
        user.delete()
