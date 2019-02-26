from mongoengine.fields import StringField

from cyhy_api.util import HashedPassword


class PasswordField(StringField):
    """Password storage for documents."""

    def validate(self, value):
        """Validate the internal storage of the Field."""
        if not isinstance(value, HashedPassword):
            self.error(f"expected a HashedPassword, found {value}")

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
