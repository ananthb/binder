"""
    binder.pages
    ~~~~~~~~~~~~

    This module exposes a flask blueprint which renders all the static pages
    on the site.

"""

from .views import Pages

__all__ = ['Pages']
