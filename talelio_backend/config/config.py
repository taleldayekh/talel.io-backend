from os import getenv


class Config(object):
    # Flask
    DEBUG = False
    SECRET_KEY = getenv('SECRET_KEY')

    # Email
    EMAIL_USER = getenv('EMAIL_USER')
    EMAIL_PASS = getenv('EMAIL_PASS')
    EMAIL_SERVER = getenv('EMAIL_SERVER')
    EMAIL_SENDER = getenv('EMAIL_SENDER')


class Development(Config):
    # Flask
    DEBUG = True


class Production(Config):
    pass
