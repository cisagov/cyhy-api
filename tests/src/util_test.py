#!/usr/bin/env pytest -vs
"""Tests for utility functions."""

from cyhy_api.util import connect_from_config


class TestUtils:
    """Util function tests."""

    def test_connect_from_config(self):
        """Create a new connection."""
        connect_from_config()
