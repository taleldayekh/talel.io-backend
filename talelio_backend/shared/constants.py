from os import getenv
from typing import cast

ENV = getenv('ENV')
SECRET_KEY = cast(str, getenv('SECRET_KEY'))

EMAIL_USER = cast(str, getenv('EMAIL_USER'))
EMAIL_PASS = cast(str, getenv('EMAIL_PASS'))
EMAIL_SENDER = cast(str, getenv('EMAIL_SENDER'))
EMAIL_SERVER = cast(str, getenv('EMAIL_SERVER'))

MAX_IMAGE_FILE_SIZE = 2 * 1024 * 1024
