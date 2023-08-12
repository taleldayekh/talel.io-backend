from __future__ import annotations

from contextlib import contextmanager
from io import SEEK_END, BytesIO
from sys import getsizeof
from tempfile import TemporaryFile
from typing import Generator, List, Tuple

from PIL import Image
from werkzeug.datastructures import FileStorage, ImmutableMultiDict


@contextmanager
def generate_file_streams(
        filenames_and_sizes: List[Tuple[str, int]]) -> Generator[List[BytesIO], None, None]:
    image_file_extensions = ['gif', 'jpeg', 'png']
    file_streams: List[BytesIO] = []

    try:
        for filename_and_size in filenames_and_sizes:
            filename, extension = filename_and_size[0].split('.')
            file_size = filename_and_size[1]

            if extension in image_file_extensions:
                image = Image.new('RGB', (500, 500))
                image_stream = BytesIO()
                setattr(image_stream, 'name', filename_and_size[0])
                image.save(image_stream, format=extension)
                image_file_size = getsizeof(image_stream)
                image_stream.seek(0, SEEK_END)
                image_stream.write(b'0' * (file_size - image_file_size))
                image_stream.seek(0)

                file_streams.append(image_stream)
                image.close()
            else:
                with TemporaryFile(suffix=f'.{extension}', prefix=filename) as temp_file:
                    temp_file_size = getsizeof(temp_file)
                    temp_file.write(b'0' * (file_size - temp_file_size))
                    temp_file.seek(0)
                    file_stream = BytesIO(temp_file.read())
                    setattr(file_stream, 'name', filename_and_size[0])

                    file_streams.append(file_stream)
        yield file_streams
    finally:
        for streams in file_streams:
            streams.close()


@contextmanager
def generate_request_files(
        filenames_and_sizes: List[Tuple[str, int]]) -> Generator[ImmutableMultiDict, None, None]:
    try:
        request_files: List[Tuple[str, FileStorage]] = []

        with generate_file_streams(filenames_and_sizes) as file_streams:
            for file_stream in file_streams:
                filename = file_stream.name
                request_file_storage = FileStorage(file_stream, filename)
                request_files.append((filename, request_file_storage))

            yield ImmutableMultiDict(request_files)
    finally:
        for request_file in request_files:
            request_file[1].close()
