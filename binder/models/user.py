"""
    binder.models.user
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

from ..database import db


class User(db.Model):
    Id = db.Column(db.Integer(), primary_key=True)
    FirstName = db.Column(db.String(20))
    MiddleName = db.Column(db.String(20))
    LastName = db.Column(db.String(20))
    Email = db.Column(db.String(200))
    OpenID = db.Column(db.String(200))

    def __init__(f_name, m_name, l_name, email, openid):
        f_name = self.Firstname
        m_name = self.MiddleName
        l_name = self.LastName
        email = self.Email
