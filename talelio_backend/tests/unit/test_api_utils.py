from tempfile import TemporaryFile

import pytest
from PIL.JpegImagePlugin import JpegImageFile
from PIL.PngImagePlugin import PngImageFile
from werkzeug.datastructures import FileStorage, ImmutableMultiDict

from talelio_backend.core.exceptions import ImageError
from talelio_backend.interfaces.api.utils import extract_request_image_files
from talelio_backend.tests.mocks.data import generate_request_image_files


def test_can_extract_image_files_from_request() -> None:
    image_one = 'image_one.jpeg'
    image_two = 'image_two.png'

    with generate_request_image_files([image_one, image_two]) as request_image_files:
        extracted_request_image_files = extract_request_image_files(request_image_files)

        assert len(extracted_request_image_files) == 2

        image_one_filename, image_one_extension = image_one.split('.')

        assert extracted_request_image_files[0].filename == image_one_filename
        assert extracted_request_image_files[0].format == image_one_extension.upper()
        assert isinstance(extracted_request_image_files[0], JpegImageFile)

        image_two_filename, image_two_extension = image_two.split('.')

        assert extracted_request_image_files[1].filename == image_two_filename
        assert extracted_request_image_files[1].format == image_two_extension.upper()
        assert isinstance(extracted_request_image_files[1], PngImageFile)


def test_cannot_extract_image_files_from_request_including_non_image_files() -> None:
    image = 'image.jpeg'
    document = 'document.txt'

    with pytest.raises(ImageError):
        with generate_request_image_files([image]) as request_image_files:
            request_image_file_storage = request_image_files[image]

            document_name, document_extension = document.split('.')
            document_file = TemporaryFile(suffix=f'.{document_extension}', prefix=document_name)

            request_document_file_storage = FileStorage(
                document_file, document_name, content_type=f'application/{document_extension}')
            request_files = [(request_image_file_storage.filename, request_image_file_storage),
                             (request_document_file_storage.filename,
                              request_document_file_storage)]

            extract_request_image_files(ImmutableMultiDict(request_files))
