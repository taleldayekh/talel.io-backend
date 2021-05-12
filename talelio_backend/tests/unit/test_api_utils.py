from io import BytesIO

from talelio_backend.interfaces.api.utils import get_streams_from_request_files
from talelio_backend.tests.mocks.data import generate_request_files


def test_can_get_streams_from_request_files() -> None:
    image_file = 'image.jpeg'
    document_file = 'document.pdf'

    with generate_request_files([(image_file, 0), (document_file, 0)]) as request_files:
        file_streams = get_streams_from_request_files(request_files)
        image_file_stream = file_streams[0]
        document_file_stream = file_streams[1]

        assert len(file_streams) == 2
        assert image_file_stream.name == image_file
        assert document_file_stream.name == document_file
        assert isinstance(image_file_stream, BytesIO)
        assert isinstance(document_file_stream, BytesIO)
