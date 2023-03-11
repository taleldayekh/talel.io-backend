from typing import Tuple

from flask import Blueprint

health_v1 = Blueprint('health_v1', __name__)


@health_v1.get('')
def health_endpoint() -> Tuple[str, int]:
    return '👍', 200
