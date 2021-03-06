#!/usr/bin/env pytest -vs
"""Tests for User documents."""

import pytest
import mongoengine

from cyhy_api.model import UserModel
from cyhy_api.util import HashedPassword


@pytest.fixture(scope="class", autouse=True)
def connection():
    """Create connections for tests to use."""
    from mongoengine import connect

    connect(host="mongomock://localhost", alias="default")


@pytest.fixture
def user():
    """Create a test user."""
    user = UserModel()
    user.email = "lemmy@imotorhead.com"
    user.first_name = "Ian"
    user.last_name = "Kilmister"
    user.phone = "800.333.7680"
    return user


class TestUsers:
    """User document tests."""

    def test_creation_without_password(self, user):
        """Create a new user, and save it."""
        with pytest.raises(mongoengine.errors.ValidationError):
            user.save()

    def test_creation_with_password(self, user):
        """Create a new user, and save it."""
        user.password = "is_god"
        user.save()

    def test_find_one_user(self):
        """Find one user."""
        user = UserModel.objects.get(email="lemmy@imotorhead.com")
        assert user is not None, "User should not be None."
        assert user.email == "lemmy@imotorhead.com", "User has wrong email."

    def test_set_password_with_wrong_type(self):
        """Pass a non-string as the password."""
        user = UserModel()
        with pytest.raises(ValueError):
            user.password = 12345

    def test_set_password_without_save(self):
        """Set user's password without save."""
        user = UserModel()
        user.password = "is_god"
        assert isinstance(user.password, HashedPassword), "password should be hashed"
        assert user.password == "is_god"

    def test_set_password_with_save(self):
        """Set user's password with save."""
        user = UserModel.objects.get(email="lemmy@imotorhead.com")
        user.password = "is_god"
        user.save()
        assert isinstance(user.password, HashedPassword), "password should be hashed"

        assert user.password == "is_god"

    def test_check_password(self):
        """Verify user's password."""
        user = UserModel.objects.get(email="lemmy@imotorhead.com")
        assert user.password == "is_god"

    def test_resave_password(self):
        """Verify user's password."""
        user = UserModel.objects.get(email="lemmy@imotorhead.com")
        user.save()

    def test_delete(self):
        """Test delete."""
        user = UserModel.objects.get(email="lemmy@imotorhead.com")
        user.delete()
        with pytest.raises(mongoengine.errors.DoesNotExist):
            user = UserModel.objects.get(email="lemmy@imotorhead.com")
