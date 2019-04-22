import bcrypt


class HashedPassword:
    """A hashed password."""

    def __init__(self, value, is_hash=False):
        """Create a new HashedPassword.

        If is_hash is True, the object is created from an existing hash.
        Otherwise the value will be hash and stored.
        """
        if is_hash is True:
            self._hash = value
        else:
            self._calculate_hash(value)

    def _calculate_hash(self, cleartext):
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(cleartext.encode("utf-8"), salt)
        self._hash = hash_bytes.decode()

    def __eq__(self, other):
        """Test equality against another object.

        If the other object is a string, it is treated as a password validation
        check.  Otherwise, it is an identity check.
        """
        if self is other:
            return True
        if isinstance(other, str):
            return bcrypt.checkpw(other.encode("utf-8"), self._hash.encode("utf-8"))
        else:
            return False

    def __str__(self):
        """Return hash for string value of object."""
        return self._hash

    def encode(self, encoding="utf-8", errors="strict"):
        """Encode the string using the codec registered for encoding."""
        return self._hash.encode(encoding, errors)
