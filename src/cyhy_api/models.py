"""Database Models."""

import bcrypt
from mongoengine import Document
from mongoengine.fields import StringField
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


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
        hash_bytes = bcrypt.hashpw(cleartext.encode('utf-8'), salt)
        self._hash = hash_bytes.decode()

    def __eq__(self, other):
        """Test equality against another object.

        If the other object is a string, it is treated as a password validation
        check.  Otherwise, it is an identity check.
        """
        if self is other:
            return True
        if isinstance(other, str):
            return bcrypt.checkpw(other.encode('utf-8'),
                                  self._hash.encode('utf-8'))
        else:
            return False

    def __str__(self):
        """Return hash for string value of object."""
        return self._hash

    def encode(self, encoding="utf-8", errors="strict"):
        """Encode the string using the codec registered for encoding."""
        return self._hash.encode(encoding, errors)


class PasswordField(StringField):
    """Password storage for documents."""

    def validate(self, value):
        """Validate the internal storage of the Field."""
        if not isinstance(value, HashedPassword):
            self.error(f'expected a HashedPassword, found {value}')

    def to_python(self, value):
        """Convert field to a python value."""
        if value:
            return HashedPassword(value, is_hash=True)
        return None

    def to_mongo(self, value):
        """Convert field to a mongo value."""
        if value:
            return str(value)
        return None


class User(Document):
    """CyHy User model."""

    username = StringField(required=True, primary_key=True)
    _password = PasswordField(required=True, db_field='password')
    meta = {'collection': 'users'}

    @property
    def password(self):
        """Get the hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        if isinstance(value, str):
            self._password = HashedPassword(value)
        else:
            raise ValueError('Expected a string to set password')

    def generate_auth_token(self, app_secret, expiration=600):
        """Generate a secure authentication token."""
        s = Serializer(app_secret, expires_in=expiration)
        return s.dumps({'id': self.username})

    @classmethod
    def verify_auth_token(cls, app_secret, token):
        """Verify a token is valid, and return the associate user document."""
        s = Serializer(app_secret)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired TODO: log it
        except BadSignature:
            return None    # invalid token TODO: log it
        return cls.objects.get(username=data['id'])
