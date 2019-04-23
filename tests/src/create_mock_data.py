#!/usr/bin/env python

"""Create mock data for CyHy

Usage:
  create_mock_data.py [--log-level=LEVEL] [--alias=ALIAS]
  create_mock_data.py (-h | --help)

Options:
  -a --alias=ALIAS       Database connection alias to use as default. [default: dev]
  -h --help              Show this message.
  --log-level=LEVEL      If specified, then the log level will be set to
                         the specified value.  Valid values are "debug", "info",
                         "warning", "error", and "critical". [default: info]
"""

import logging
import sys

import docopt
from mimesis import Person

from cyhy_api.model import UserModel
from cyhy_api.util import connect_from_config


def setup(alias):
    logging.info(f"Creating default database connection for alias '{alias}'")
    connect_from_config(default_alias=alias)


def generate_users(count=1024, locale="en"):
    logging.info(f"Generating {count} users.")
    person = Person(locale)
    for i in range(count):
        user = UserModel()
        user.first_name = person.name()
        user.last_name = person.surname()
        user.email = person.email()
        user.password = person.password()
        user.phone = person.telephone(mask="###.###.####")
        user.save()


def generate():
    """Generate each type of object"""
    generate_users(10)


def main():
    args = docopt.docopt(__doc__, version="0.0.1")

    # Set up logging
    log_level = args["--log-level"]
    try:
        logging.basicConfig(
            format="%(asctime)-15s %(levelname)s %(message)s", level=log_level.upper()
        )
    except ValueError:
        logging.critical(
            f'"{log_level}" is not a valid logging level.  Possible values '
            "are debug, info, warning, and error."
        )
        return 1

    setup(args["--alias"])
    generate()

    # Stop logging and clean up
    logging.shutdown()


if __name__ == "__main__":
    sys.exit(main())
