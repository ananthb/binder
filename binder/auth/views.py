"""
    binder.auth.views
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

import sys
from flask import (g, redirect, request, render_template,
                   session, flash, url_for, Blueprint)
from flask_oauthlib.client import OAuth

from binder.models import User

Auth = Blueprint('auth', __name__, url_prefix='/auth')
oauth = OAuth()
facebook = None


@Auth.record_once
def record_auth(setup_state):
    """ record_auth::flask.Flask.state->None

        This function sets up the oauth object.
        Config options can only be retrieved from an
        app object. Hence, this func.
    """

    app = setup_state.app
    fb_id = app.config.get('FACEBOOK_APP_ID')
    fb_secret = app.config.get('FACEBOOK_APP_SECRET')
    if fb_id is None or fb_secret is None:
        print("[binder] error: Facebook app ID or secret not found.",
              file=sys.stderr)
        sys.exit(1)
    global facebook
    facebook = oauth.remote_app(
        'facebook',
        base_url='https://graph.facebook.com/',
        request_token_url=None,
        access_token_url='/oauth/access_token',
        authorize_url='https://www.facebook.com/dialog/oauth',
        consumer_key=app.config.get('FACEBOOK_APP_ID'),
        consumer_secret=app.config.get('FACEBOOK_APP_SECRET'),
        request_token_params={'scope': 'email'}
    )


@Auth.route('/login')
def login():
    return facebook.authorize(
        callback=url_for(
            '.fb_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True
        ))


@Auth.route('/fb_authorized')
def fb_authorized():
    next_url = request.args.get('next') or url_for('pages.index')
    resp = facebook.authorized_response()
    if resp is None:
        flash("You denied the sign in request.")
        return redirect(next_url)
    # Must add way of storing logged in user's creds
    # and actually signing them in.
    flash("Signed in", 'success')
    return redirect(next_url)
