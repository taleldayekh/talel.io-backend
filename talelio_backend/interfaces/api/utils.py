from typing import List

from PIL import Image as img
from PIL.Image import Image
from werkzeug.datastructures import MultiDict

from talelio_backend.core.exceptions import ImageError


def extract_request_image_files(request_files: MultiDict) -> List[Image]:
    image_files = []

    for file in request_files.values():
        try:
            image = img.open(file)
            setattr(image, 'filename', file.filename)
            image_files.append(image)
        except Exception as e:
            raise ImageError(e) from e

    return image_files
