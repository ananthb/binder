"""
    binder.app
    ~~~~~~~~~~

    Module for initialising the app's environment
    and creating the application.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details

"""

import sys
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

import binder
from .config import DefaultConfig

__all__ = ['create_app']


def create_app(config=None):
    """ create_app::Flask.Config->String->[Blueprint]->Flask

        Creates a Flask app and registers blueprints if any.

        config is the path to a configuration file.
    """

    app = Flask('binder')

    # Add bootstrap functionality
    Bootstrap(app)

    # Apply configuration options
    config_app(config, app)

    # app error handlers
    @app.errorhandler(404)
    def error_handler(e):
        return render_template('error_404.html'), 404

    # Register app blueprints
    for blueprint in binder.BLUEPRINTS:
            app.register_blueprint(blueprint)
    return app


def config_app(config, app):
    """ config_app::flask.Flask->None

        Configures the app with the defailt configuration.
        If a configuration file is supplied, that is also applied.
    """

    app.config.from_object(DefaultConfig)
    if config:
        try:
            app.config.from_pyfile(config)
        except (FileNotFoundError, PermissionError):
            print("[binder] Error: Config file not readable or not found.",
                  file=sys.stderr)
            sys.exit(1)
