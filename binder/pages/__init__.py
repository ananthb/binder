"""
    binder.pages
    ~~~~~~~~~~~~

    This module exposes a flask blueprint which renders all the static pages
    on the site.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, see LICENSE for more details
"""

from .views import Pages

__all__ = ['Pages']
