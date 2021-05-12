from io import BytesIO
from typing import List

from werkzeug.datastructures import MultiDict


def get_streams_from_request_files(request_files: MultiDict) -> List[BytesIO]:
    file_streams: List[BytesIO] = []

    for file in request_files.values():
        file_stream = BytesIO(file.stream.read())
        setattr(file_stream, 'name', file.filename)
        file_streams.append(file_stream)

    return file_streams
