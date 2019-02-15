"""Database Models."""

from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
from pymodm.manager import Manager
import bcrypt
from flask import current_app as app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


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

    def verify_auth_token(self, token):
        """Verify a token is valid, and return the associate user document."""
        s = Serializer(app.config['SECRET_KEY'])
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
    hash = fields.CharField()
    # Change the "objects" manager to use our own custom manager.
    objects = UserManager()

    class Meta:
        """User Model Meta configuration."""

        indexes = []
        write_concern = WriteConcern(j=True)
        collection_name = 'users'
        final = True

    def check_password(self, password):
        """Check if a password matches the password in the document."""
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
