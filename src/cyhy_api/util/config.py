"""Utility functions."""

import yaml
from mongoengine import connect


def load_config(filename="/run/secrets/config.yml"):
    """Load a configuration file."""
    print(f"Reading configuration from {filename}")
    with open(filename, "r") as stream:
        config = yaml.safe_load(stream)
    return config


def connect_from_config(config=None, default_alias=None):
    """Create connections from a confguration.

    config: configuration file to load
    default_alias: if set, a single connection is set as the default.
                   if unset, all aliases in the config will be created.
    """
    if not config:
        config = load_config()
    connections = config["databases"]
    if default_alias is not None:
        # only create the specified connection and map it to the "default" alias
        try:
            connect(host=connections[default_alias]["uri"], alias="default")
        except KeyError:
            raise KeyError(
                f"Requested alias '{default_alias}' not found in connection configuration file."
            )
    else:
        # create all connections
        for alias in connections.keys():
            connect(host=connections[alias]["uri"], alias=alias)
