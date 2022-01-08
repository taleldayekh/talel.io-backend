from os import getenv


class Config(object):
    DEBUG = False
    S3_BUCKET = getenv('S3_BUCKET')


class Development(Config):
    DEBUG = True
    CORS_ORIGIN_WHITELIST = {'origins': ['http://127.0.0.1:3000']}


class Production(Config):
    CORS_ORIGIN_WHITELIST = {'origins': ['https://www.talel.io', 'https://talel.io']}
