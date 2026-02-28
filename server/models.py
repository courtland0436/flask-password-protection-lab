from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    # Protect password_hash property
    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password is write-only.")

    # Set password hash property using bcrypt
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # Authenticate user
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'


class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()