from mongoengine import Document
from mongoengine.fields import EmailField
from mongoengine.errors import DoesNotExist

from .fields import PasswordField
from ..util import HashedPassword


class UserModel(Document):
    """CyHy User model."""

    # id is used as the uid
    email = EmailField(required=True, help_text="The user's email address")
    _password = PasswordField(
        required=True, db_field="password", help_text="The user's hashed password"
    )
    meta = {"collection": "users", "indexes": ["email"]}

    @property
    def uid(self):
        """Get the user id as a string."""
        return str(self.id)

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
    def find_user_by_email(cls, search):
        """Verify a email, and return the associate user document."""
        if "$" in search:  # TODO better sanitization
            return None
        try:
            return cls.objects.get(email=search)
        except DoesNotExist:
            return None
