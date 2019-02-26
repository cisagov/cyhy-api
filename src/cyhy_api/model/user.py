from mongoengine import Document
from mongoengine.fields import StringField
from mongoengine.errors import DoesNotExist

from .fields import PasswordField
from ..util import HashedPassword


class UserModel(Document):
    """CyHy User model."""

    username = StringField(required=True, primary_key=True)
    _password = PasswordField(
        required=True,
        db_field="password",
        help_text="The user's hashed password",
    )
    meta = {"collection": "users"}

    @property
    def password(self):
        """Get the hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        if isinstance(value, str):
            self._password = HashedPassword(value)
        else:
            raise ValueError("Expected a string to set password")

    @classmethod
    def find_user_by_username(cls, search):
        """Verify a username, and return the associate user document."""
        if "$" in search:  # TODO better sanitization
            return None
        try:
            return cls.objects.get(username=search)
        except DoesNotExist:
            return None
