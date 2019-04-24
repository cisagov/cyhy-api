def valid_enough_email(address):
    """Sanity check a user supplied email address.

    Validation of an email address is very difficult.  Make a best effort attempt to
    see if it minimally conforms to the following RFCs.

    https://tools.ietf.org/html/rfc822
    https://tools.ietf.org/html/rfc2822
    https://tools.ietf.org/html/rfc5335
    https://tools.ietf.org/html/rfc5336
    https://tools.ietf.org/html/rfc3696
    """

    if not address or not isinstance(address, str):
        return False

    # split address into parts. rsplit is probably a better match then split.
    local_part, domain_part = address.rsplit("@", 1)

    # https://tools.ietf.org/html/rfc3696#section-3
    if len(address) > 320:
        return False
    if address.count("@") == 0:
        return False

    # https://tools.ietf.org/html/rfc2821#section-4.5.3.1
    if len(local_part) < 0 or len(local_part) > 64:
        return False
    if len(domain_part) < 0 or len(domain_part) > 255:
        return False

    # good enough
    return True
