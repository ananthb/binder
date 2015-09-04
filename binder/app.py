"""
    binder.app
    ~~~~~~~~~~

    Module for initialising the app's environment
    and creating the application.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

import os
import sys
import enum
import logging

from flask import g, Flask, render_template, current_app
from flask_menu import Menu
from flask.ext.script import Manager
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap
from sqlalchemy.orm.exc import NoResultFound

from . import pages, auth, dash
from .database import db
from .models import User
from .config import DevelopmentConfig, TestingConfig, ProductionConfig

__all__ = ['create_app', 'binder_app']

# Global list of blueprints
BLUEPRINTS = [
    pages.Pages,
    auth.Auth,
    dash.DashBoard
]

Mode = enum.Enum('Mode', 'Development Testing Production')


# This is the function that runs when the binder command is executed in a shell
def binder_app():
    manager = Manager(create_app)
    manager.add_option(
        '-c',
        '--config',
        dest='config',
        required=False,
        help='Path to configuration file'
    )
    manager.add_option(
        '-m',
        '--mode',
        dest='mode',
        required=False,
        help='App running mode. One of Development, Testing, and Production'
    )
    # We are off to the races
    manager.run()


def create_app(config, mode):
    """ create_app::Flask.Config->binder.Mode->Flask

        Creates a Flask app and registers blueprints if any.

        config is the path to a configuration file.
        If the path to the config file is a relative path, then
        the instance folder of the app is searched. If the config file
        is located outside the app's instance folder, an absolute path
        can be used for it.
    """

    app = Flask('binder', instance_relative_config=True)

    # Add bootstrap functionality
    Bootstrap(app)

    # init flask_menu
    Menu(app)

    # Apply configuration options
    config_app(mode, config, app)

    # initialize and configure the db for use in request handlers
    config_db(db, app)

    # flask login
    setup_login_manager(app)

    # app error handlers
    @app.errorhandler(404)
    def error_handler(e):
        return render_template('error_404.html'), 404

    # Register app blueprints
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
    return app


def config_app(app_mode, config, app):
    """ config_app::binder.Mode->flask.Flask.config->flask.Flask->None

        Configures the app to run in the given mode.
        If a configuration file is supplied, that is also applied.
    """

    if app_mode is None:
        app_mode = "Development"

    config_map = {
        Mode.Development: DevelopmentConfig,
        Mode.Testing: TestingConfig,
        Mode.Production: ProductionConfig
    }
    try:
        app.config.from_object(config_map[Mode[app_mode]])
    except KeyError:
        print("[binder] Error: Invalid mode. Run binder --help for more.",
              file=sys.stderr)
        sys.exit(1)

    if config:
        try:
            app.config.from_pyfile(config)
        except (FileNotFoundError, PermissionError):
            print("[binder] Error: Config file not readable or not found.",
                  file=sys.stderr)
            sys.exit(1)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = app.config.get(
        'OAUTHLIB_INSECURE_TRANSPORT'
    )


def config_db(db, app):
    """ config_db::SQLAlchemy->flask.Flask->None

        Initializes the database. Also creates the tables.
        *This should check if tables exist before creating them.*
        Then attaches the database object to the flask.g object
    """

    db.init_app(app)
    if app.config['DEBUG'] is True:
        # create database tables in an app request context
        with app.test_request_context():
            db.create_all()
            db.session.commit()

    # inject db into app context for request handlers
    @app.before_request
    def inject_db():
        g.db = db

    # Subsequently clean up the db connection
    @app.teardown_request
    def cleanup_db(exception):
        if exception is not None:
            logging.error(exception)

        if g.get(db):
            g.db.session.commit()
            del g.db


def setup_login_manager(app):
    """ setup_login_manager::flask.Flask->None

        Creates a login manager object and attaches an application
        object to it.

        Also sets up the login view function to redirect to, and
        the user_loader function.

    """

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            # we need a request context for a valid db connection
            with current_app.test_request_context('/'):
                db = g.db
                user = db.session.query(User).filter(User.UUID == user_id).one()
            return user
        except NoResultFound as e:
            logging.debug(e)
            return None
