"""
    binder.auth.views
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

import sys
import uuid
import logging

from flask import (g, redirect, request, current_app,
                   session, flash, url_for, Blueprint)
from flask.ext.login import login_user, logout_user, current_user
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from ..models import User

Auth = Blueprint('auth', __name__, url_prefix='/auth')


@Auth.record_once
def check_facebook_creds(setup_state):
    """ check_facebook_creds::flask.Flask.state->None

        Checks for facebook oauth credentials when registering
        the blueprint.
    """

    app = setup_state.app
    fb_id = app.config.get('FACEBOOK_APP_ID')
    fb_secret = app.config.get('FACEBOOK_APP_SECRET')
    if fb_id is None or fb_secret is None:
        print("[binder] error: Facebook app ID or secret not found.",
              file=sys.stderr)
        sys.exit(1)


@Auth.before_request
def redirect_logged_in_user():
    if current_user.is_authenticated and not current_user.is_anonymous:
        flash("Already logged in!")
        return redirect(url_for('dashboard.me'))


@Auth.before_request
def setup_faecbook_oauth():
    fb_id = current_app.config.get('FACEBOOK_APP_ID')
    facebook = OAuth2Session(
        client_id=fb_id,
        redirect_uri=url_for('auth.fb_authorized', _external=True),
    )
    facebook = facebook_compliance_fix(facebook)
    g.fb_oauth = facebook


@Auth.route('/login')
def login():
    facebook = g.fb_oauth
    authorization_url, state = facebook.authorization_url(
        'https://www.facebook.com/dialog/oauth'
    )
    session['fb_oauth_state'] = state
    return redirect(authorization_url)


@Auth.route('/fb_authorized/')
def fb_authorized():
    # verify that state returned by facebook is the same
    fb_state = request.args.get('state')
    if fb_state != session['fb_oauth_state']:
        flash("Oops! Something went wrong. Try again", 'error')
        logging.warn("Different state received from facebook. Very fishy!")
        return redirect(url_for('pages.home'))

    facebook = g.fb_oauth
    client_secret = current_app.config.get('FACEBOOK_APP_SECRET')
    facebook.fetch_token(
        'https://graph.facebook.com/oauth/access_token',
        client_secret=client_secret,
        authorization_response=request.url,
    )
    session['fb_oauth_token'] = facebook.token
    fb_profile = facebook.get('https://graph.facebook.com/me').json()
    username = fb_profile['name']
    u_id = uuid.uuid4()
    user = User(str(u_id), username, None, True)
    g.db.session.add(user)
    login_user(user)
    flash("Signed in as {}".format(username), 'success')
    return redirect(url_for('dashboard.me'))


@Auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.index'))


@Auth.teardown_request
def cleanup_facebook_oauth(exception=None):
    if exception:
        logging.error(exception)
    del g.fb_oauth
