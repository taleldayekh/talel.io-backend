from io import BytesIO
from os.path import splitext
from re import sub
from sys import getsizeof
from typing import List


class Asset:
    @staticmethod
    def validate_file_size(file_streams: List[BytesIO], max_file_size: int) -> bool:
        for file_stream in file_streams:
            if getsizeof(file_stream) > max_file_size:
                return False

        return True

    @staticmethod
    def generate_secure_filename(filename: str) -> str:
        """
        Removes characters which are not letters or numbers and replaces all
        whitespaces with underscores and converts the string into lowercase.
        """
        (filename, extension) = splitext(filename)

        return sub(r'[^A-Za-z0-9\s]', '', filename).replace(' ', '_').lower() + extension
