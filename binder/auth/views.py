"""
    binder.auth.views
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

from flask import (g, redirect, request, render_template,
                   session, flash, url_for, Blueprint)
from flask_oauthlib.client import OAuth

from binder.models import User

Auth = Blueprint('auth', __name__, url_prefix='/auth')
