#!/usr/bin/env pytest -vs
"""Tests for utility functions."""

from cyhy_api.util import connect_from_config, load_config


class TestUtils:
    """Util function tests."""

    def test_connect_from_config(self):
        """Create a new connection."""
        config = load_config("tests/secrets/config-mock.yml")
        connect_from_config(config)
