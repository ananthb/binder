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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    DEBUG = True
    OPENID_PROVIDERS = [
        "https://openid.stackexchange.com/",
    ]


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
