"""
    binder.auth
    ~~~~~~~~~~~

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

import uuid

from flask import g, Blueprint, current_app, redirect, url_for, flash
from flask.ext.login import (current_user, logout_user,
                             login_user, LoginManager)
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound

from .models import User

__all__ = ['Auth', 'FacebookOAuth']


def setup_login_manager(app):
    """ setup_login_manager::flask.Flask->None

        Creates a login manager object and attaches an application
        object to it.

        Also sets up the login view function to redirect to, and
        the user_loader function.

    """

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'facebook.login'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            # we need a request context for a valid db connection
            with current_app.test_request_context('/'):
                db = g.db
                user = db.session.query(User).filter(User.UUID == user_id).one()
                return user
        except NoResultFound as e:
            current_app.logger.debug(e)
            return None


Auth = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


@Auth.route('/logout')
def logout():
    current_app.logger.debug("UUID:{} logged out.".format(current_user.UUID))
    logout_user()
    flash("Logged out.")
    return redirect(url_for('pages.index'))


# Facebook OAuth blueprint
FacebookOAuth = make_facebook_blueprint(
    redirect_to='dashboard.me'
)

FacebookOAuth.url_prefix = '/auth'


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(FacebookOAuth)
def facebook_logged_in(blueprint, token):
    db = g.db
    if not token:
        msg = "Failed to log in with {name}".format(name=blueprint.name)
        flash(msg)
        current_app.logger.error(msg)
        return
    # figure out who the user is
    resp = blueprint.session.get("/me")
    if resp.ok:
        name = resp.json()["name"]
        query = db.session.query(User).filter(User.Name == name)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            u_id = str(uuid.uuid4())
            user = User(u_id=u_id, name=name, email=None, is_active=True)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash("Successfully signed in with Facebook")
    else:
        msg = "Failed to fetch user info from {}".format(blueprint.name)
        current_app.logger.error(msg)
        flash(msg, category="error")


# notify on OAuth provider error
@oauth_error.connect_via(FacebookOAuth)
def facebook_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")
    current_app.logger.error(msg)
