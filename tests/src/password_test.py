#!/usr/bin/env pytest -vs
"""Tests for Password objects."""

import pytest

from cyhy_api.models import HashedPassword


class TestHashedPassword:
    """HashedPassword tests."""

    def test_empty_creation(self):
        """Create an empty password."""
        with pytest.raises(TypeError):
            p = HashedPassword()  # noqa: F841

    def test_value_creation(self):
        """Create an password from a string."""
        p = HashedPassword('is_god')  # noqa: F841

    def test_identity_equality(self):
        """Verify identity equality."""
        p = HashedPassword('is_god')
        assert p == p, 'Identity equality is broken'

    def test_validation_eqality(self):
        """Verify validation check against cleartext."""
        p = HashedPassword('is_god')
        assert p == 'is_god', 'Password did not verify correctly'
        assert p != 'is_man', 'Password did not verify correctly'

    def test_creation_from_hash(self):
        """Test object creation from hash."""
        # hash is for 'is_god'
        p = HashedPassword('$2b$12$j8hhjG.VS9wH3m5QM8BewOLy9gx7rfOhdONbA7kFVnpxvfFeImxGC', is_hash=True)  # noqa: E501
        assert p == 'is_god', 'Password did not verify correctly'
        assert p != 'is_man', 'Password did not verify correctly'
