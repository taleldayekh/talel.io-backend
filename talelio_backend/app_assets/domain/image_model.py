from imghdr import what
from io import BytesIO
from typing import List

from talelio_backend.app_assets.domain.asset_model import Asset
from talelio_backend.constants import MAX_IMAGE_FILE_SIZE
from talelio_backend.core.exceptions import ImageError


class Image(Asset):
    def __init__(self, image_streams: List[BytesIO]) -> None:
        self.image_streams = image_streams

    @property
    def validate_type(self) -> bool:
        allowed_image_types = ['gif', 'jpeg', 'png']

        for image_stream in self.image_streams:
            # Reads sufficient bytes of a stream to identify from
            # the header whether the file is of valid image type.
            header = image_stream.read(512)
            image_stream.seek(0)

            image_type = what(None, header)

            if not image_type or image_type not in allowed_image_types:
                return False

        return True

    @property
    def validate_size(self) -> bool:
        return self.validate_file_size(self.image_streams, MAX_IMAGE_FILE_SIZE)

    @property
    def validate(self) -> bool:
        if not self.validate_type:
            raise ImageError('One or more image files are of invalid type')
        if not self.validate_size:
            raise ImageError('One or more image file sizes are too large')

        return True
