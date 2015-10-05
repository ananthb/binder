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
    FLASK_LOG_LEVEL = 'INFO'


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    FLASK_LOG_LEVEL = 'ERROR'
