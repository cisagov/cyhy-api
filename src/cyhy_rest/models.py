"""Database Models."""

from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
from pymodm.manager import Manager
from pymodm.base.fields import MongoBaseField
import bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class HashedPassword:
    """A hashed password."""

    def __init__(self, value, is_hash=False):
        """Create a new HashedPassword.

        If is_hash is True, the object is created from an existing hash.
        Otherwise the value will be hash and stored.
        """
        # TODO: This is a workaround until we can reliably
        # pass argument is_hash in from the model when set, and fetched
        # from the database.
        try:
            bcrypt.checkpw(b'', value.encode('utf-8'))
            # if we got here value is a valid hash
            is_hash = True
        except ValueError:
            # the value was invalid, treat as a cleartext password
            is_hash = False

        if is_hash is True:
            self._hash = value
        else:
            self._hash(value)

    def _hash(self, cleartext):
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


class PasswordField(MongoBaseField):
    """Password storage for models."""

    def __init__(self, verbose_name=None, mongo_name=None, **kwargs):
        """Create a new PasswordField.

        :parameters:
          - `verbose_name`: A human-readable name for the Field.
          - `mongo_name`: The name of this field when stored in MongoDB.

        .. seealso:: constructor for
                     :class:`~pymodm.base.fields.MongoBaseField`

        """
        super().__init__(verbose_name=verbose_name,
                         mongo_name=mongo_name,
                         **kwargs)

    def to_python(self, value):
        """Convert field to a python value."""
        return HashedPassword(value, is_hash=True)

    def to_mongo(self, value):
        """Convert field to a mongo value."""
        return value._hash


class UserManager(Manager):
    """Manager for the User Model.

    Contains common queries used to access the User collection.
    """

    def find_one_user(self, username):
        """Search for a user by username."""
        query = self.model.objects.raw({'_id': username})
        if query.count() == 1:
            return query[0]
        else:
            return None

    def verify_auth_token(self, token, app_secret):
        """Verify a token is valid, and return the associate user document."""
        s = Serializer(app_secret)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired TODO: log it
        except BadSignature:
            return None    # invalid token TODO: log it
        return self.find_one_user(data['id'])


class User(MongoModel):
    """CyHy User model."""

    username = fields.CharField(primary_key=True)
    password = PasswordField(mongo_name='password')
    objects = UserManager()

    class Meta:
        """User Model Meta configuration."""

        indexes = []
        write_concern = WriteConcern(j=True)
        collection_name = 'users'
        final = True

    def generate_auth_token(self, app_secret, expiration=600):
        """Generate a secure authentication token."""
        s = Serializer(app_secret, expires_in=expiration)
        return s.dumps({'id': self.username})
