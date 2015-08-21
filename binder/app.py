"""
    binder.app
    ~~~~~~~~~~

    Module for initialising the app's environment
    and creating the application.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

import sys
import enum

from flask import g, Flask
from flask import render_template
from flask_menu import Menu
from flask.ext.script import Manager
from flask_bootstrap import Bootstrap

import binder
from .auth import oid
from .database import db
from .models import User
from .config import DevelopmentConfig, TestingConfig, ProductionConfig

__all__ = ['create_app', 'binder_app']

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

    if mode is None:
        mode = "Development"

    app = Flask('binder', instance_relative_config=True)

    # Add bootstrap functionality
    Bootstrap(app)

    # init flask_menu
    Menu(app)

    # Apply configuration options
    config_app(mode, config, app)

    # activate OpenID
    oid.init_app(app)

    # SQLAlchemy init
    db.init_app(app)
    # development mode
    if mode == "Development":
        with app.test_request_context():
            db.create_all()
    # attach the db connection to the application context
    with app.app_context():
        g.db = db

    # app error handlers
    @app.errorhandler(404)
    def error_handler(e):
        return render_template('error_404.html'), 404

    # Register app blueprints
    for blueprint in binder.BLUEPRINTS:
        app.register_blueprint(blueprint)
    return app


def config_app(app_mode, config, app):
    """ config_app::binder.Mode->flask.Flask.config->flask.Flask->None

        Configures the app to run in the given mode.
        If a configuration file is supplied, that is also applied.
    """

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
