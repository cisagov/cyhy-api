#!/usr/bin/env pytest -vs
"""Tests for email validation."""

import pytest

from cyhy_api.util import valid_enough_email

valid_addresses = [
    "local_part_is_len_64_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@foo.bar",
    "foo@domain_part_is_len_255_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.gov",
    # https://en.wikipedia.org/wiki/Email_address#Examples
    "simple@example.com",
    "very.common@example.com",
    "disposable.style.email.with+symbol@example.com",
    "other.email-with-hyphen@example.com",
    "fully-qualified-domain@example.com",
    "user.name+tag+sorting@example.com",
    "x@example.com",
    "example-indeed@strange-example.com",
    "admin@mailserver1",
    "example@s.example",
    '" "@example.org',
    '"john..doe"@example.org',
    '"john(with a comment)doe"@foo.bar',
    # https://tools.ietf.org/html/rfc3696#section-3
    r"Abc\@def@example.com",
    r"Fred\ Bloggs@example.com",
    r"Joe.\\Blow@example.com",
    "user+mailbox@example.com",
    "customer/department=shipping@example.com",
    "$A12345@example.com",
    "!def!xyz%abc@example.com",
    "_somename@example.com",
    u"áöüñ@example.com",
    # https://en.wikipedia.org/wiki/International_email#Email_addresses
    u"用户@例子.广告",
    u"अजय@डाटा.भारत",
    u"квіточка@пошта.укр",
    u"θσερ@εχαμπλε.ψομ",
    u"Dörte@Sörensen.example.com",
    u"коля@пример.рф",
]

# detection of these bad addresses should work
invalid_addresses = [
    None,
    "",
    12345,
    "local_part_is_len_65_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@foo.bar",
    "foo@domain_part_is_len_256_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.gov",
    "no.arobase.in.this.address",
]

# we cannot detect that these are invalid
invalid_addresses_xfail = [
    # https://en.wikipedia.org/wiki/Email_address#Examples
    "A@b@c@example.com",
    r'a"b(c)d,e:f;g<h>i[j\k]l@example.com',
    'just"not"right@example.com',
    r'this is"not\allowed@example.com',
    r"this\ still\"not\\allowed@example.com",
    "no-end-dash-allow@domain.dash-",
    "no-end-space-in-local @foo.com",
    "test@-gmail.com",
    "test@gmail.-com",
]


@pytest.mark.parametrize("address", valid_addresses)
def test_valid(address):
    """Test with valid email addresses."""
    assert valid_enough_email(address) is True, "Valid address evaluated as invalid."


@pytest.mark.parametrize("address", invalid_addresses)
def test_invalid(address):
    """Test with invalid email addresses."""
    assert valid_enough_email(address) is False, "Invalid address evaluated as valid."


@pytest.mark.xfail
@pytest.mark.parametrize("address", invalid_addresses_xfail)
def test_invalid_xfail(address):
    """Test with invalid email addresses that we can't handle yet."""
    assert valid_enough_email(address) is False, "Invalid address evaluated as valid."
