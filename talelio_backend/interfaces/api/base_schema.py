from typing import Any, Dict, Union

from marshmallow import Schema, ValidationError

from talelio_backend.shared.exceptions import SchemaValidationError


class CustomBaseSchema(Schema):

    def handle_error(self, error: ValidationError, data: Union[Dict[str, Any], None], many: bool,
                     **kwargs: Any) -> None:
        raise SchemaValidationError(error)
