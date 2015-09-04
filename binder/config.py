"""
    binder.config
    ~~~~~~~~~~~~~

    Contains default configuration options for binder.

    :copyright: (c) 2015 by Ananth Bhaskararaman
    :license: MIT, See LICENSE for more details
"""


class Config(object):
    """ Default configuration """
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass
