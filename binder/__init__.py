"""
binder
~~~~~~

Brings students closer.

:copyright: (c) 2015 by Ananth Bhaskararaman
:license: MIT, see LICENSE for more details

"""

__version__ = '0.0.1'

from flask.ext.script import Manager

from .app import create_app


def binder_app():
    manager = Manager(create_app)
    manager.add_option(
        '-c',
        '--config',
        dest='config',
        required=False,
        help='Path to configuration file'
    )
    # We are off to the races
    manager.run()
