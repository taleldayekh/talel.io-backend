class Config(object):
    DEBUG = False


class Development(Config):
    DEBUG = True
    CORS_ORIGIN_WHITELIST = {'origins': ['http://localhost:3000']}


class Production(Config):
    CORS_ORIGIN_WHITELIST = {'origins': ['https://www.talel.io', 'https://talel.io']}
