"""
    binder.models.user
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

from ..database import db


class User(db.Model):
    UUID = db.Column(db.String(36), primary_key=True)
    Name = db.Column(db.String(50))
    Email = db.Column(db.String(200))
    IsActive = db.Column(db.Boolean)

    def __init__(self, u_id, name, email, is_active):
        self.UUID = u_id
        self.Name = name
        self.Email = email
        self.IsActive = is_active

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.IsActive

    def is_anonymous(self):
        return True

    def get_id(self):
        return self.UUID
