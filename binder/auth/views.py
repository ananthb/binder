"""
    binder.auth.views
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

import sys
from flask import (redirect, request, current_app,
                   session, flash, url_for, Blueprint)
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from binder.models import User

Auth = Blueprint('auth', __name__, url_prefix='/auth')


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
    facebook = OAuth2Session(client_id=fb_id)
    facebook = facebook_compliance_fix(facebook)
    Auth.facebook_oauth = facebook


@Auth.route('/login')
def login():
    facebook = Auth.facebook_oauth
    facebook.redirect_uri = url_for('auth.fb_authorized', _external=True)
    authorization_url, state = facebook.authorization_url(
        'https://www.facebook.com/dialog/oauth'
    )
    session['oauth_state'] = state
    return redirect(authorization_url)


@Auth.route('/fb_authorized')
def fb_authorized():
    facebook = Auth.facebook_oauth
    next_url = request.args.get('next') or url_for('pages.index')
    client_secret = current_app.config.get('FACEBOOK_APP_SECRET')
    facebook.fetch_token(
        'https://graph.facebook.com/oauth/access_token',
        client_secret=client_secret,
        authorization_response=request.url,
    )
    # and actually signing them in.
    flash("Signed in", 'success')
    return redirect(next_url)
