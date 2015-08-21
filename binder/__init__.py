"""
    binder
    ~~~~~~

    Brings students closer.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details

"""

__version__ = '0.0.1'

from .app import binder_app, create_app

# import blueprints
from . import pages
from . import auth

# Global list of blueprints
BLUEPRINTS = [
    pages.Pages,
    auth.Auth,
]
