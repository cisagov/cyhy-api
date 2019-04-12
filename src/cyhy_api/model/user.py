from datetime import datetime

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    EmailField,
    EmbeddedDocumentField,
    DateTimeField,
    MapField,
)
from mongoengine.errors import DoesNotExist

from .fields import PasswordField
from ..util import HashedPassword


class RefreshToken(EmbeddedDocument):
    """Embedded document storing refresh token details for a user."""

    # (JWT ID) Claim
    # See: https://tools.ietf.org/html/rfc7519#section-4.1.7
    # jti = UUIDField(required=True)
    # (Expiration Time) Claim
    # https://tools.ietf.org/html/rfc7519#section-4.1.4
    expiration = DateTimeField(required=True)
    # (Not Before) Claim
    # https://tools.ietf.org/html/rfc7519#section-4.1.5
    not_before = DateTimeField(required=True)
    # (Issued At) Claim
    # https://tools.ietf.org/html/rfc7519#section-4.1.6
    issued_at = DateTimeField(required=True)

    def init_from_jwt(self, jwt_token):
        self.expiration = datetime.fromtimestamp(jwt_token["exp"])
        self.not_before = datetime.fromtimestamp(jwt_token["nbf"])
        self.issued_at = datetime.fromtimestamp(jwt_token["iat"])


class UserModel(Document):
    """CyHy User model."""

    # id is used as the uid
    email = EmailField(required=True, help_text="The user's email address")
    _password = PasswordField(
        required=True, db_field="password", help_text="The user's hashed password"
    )
    tokens = MapField(EmbeddedDocumentField(RefreshToken))
    meta = {"collection": "users", "indexes": ["email", "tokens.jti"]}

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

    def add_refresh_token(self, refresh_token):
        token = RefreshToken()
        token.init_from_jwt(refresh_token)
        self.tokens[refresh_token["jti"]] = token

    def revoke_refresh_token(self, refresh_token):
        return self.tokens.pop(refresh_token["jti"], None)

    def verify_refresh_token(self, refresh_token):
        # TODO expire tokens
        return refresh_token["jti"] in self.tokens

    @classmethod
    def find_user_by_email(cls, search):
        """Verify a email, and return the associate user document."""
        if "$" in search:  # TODO better sanitization
            return None
        try:
            return cls.objects.get(email=search)
        except DoesNotExist:
            return None
