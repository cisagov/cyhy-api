"""Database Models."""

from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
import bcrypt
from flask import current_app as app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(MongoModel):
    """CyHy User model."""

    username = fields.CharField(primary_key=True)
    hash = fields.CharField()

    class Meta:
        """User Model Meta configuration."""

        indexes = []
        write_concern = WriteConcern(j=True)
        collection_name = 'users'
        final = True

    def check_password(self, password):
        """Check if a provided password matches the password in the object."""
        return bcrypt.checkpw(password.encode('utf-8'),
                              self.hash.encode('utf-8'))

    def hash_password(self, password):
        """Store a new password as a hash."""
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.hash = hash_bytes.decode()

    def generate_auth_token(self, expiration=600):
        """Generate a secure authentication token."""
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.username})

    @staticmethod
    def verify_auth_token(token):
        """Verify a token is valid, and return the associate username."""
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        query = User.objects.raw({'_id': data['id']})
        user = query[0]  # TODO: move this to a custom manager
        return user
