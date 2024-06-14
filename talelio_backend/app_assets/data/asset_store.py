from enum import Enum, unique
from io import BytesIO
from os import getenv
from typing import Dict

from boto3 import client
from mypy_boto3_s3.client import S3Client

AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')

s3_client = client('s3',
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


@unique
class Asset(Enum):
    IMAGES = 'images'


class AssetStore:

    def __init__(self, s3: S3Client = s3_client) -> None:
        self.s3 = s3

    def upload(self, file: BytesIO, user_id: int, options: Dict[str, str]) -> str:
        try:
            bucket = options['bucket']
            asset_type = options['asset_type']
            key = f'{user_id}/{asset_type}/{file.name}'

            self.s3.upload_fileobj(file, bucket, key)

            return self._get_object_url(bucket, key)
        except self.s3.exceptions.ClientError as error:
            raise error

    def download(self, file_name: str, user_id: int, options: Dict[str, str]) -> BytesIO:
        try:
            file_stream = BytesIO()

            bucket = options['bucket']
            asset_type = options['asset_type']
            key = f'{user_id}/{asset_type}/{file_name}'

            self.s3.download_fileobj(bucket, key, file_stream)
            file_stream.seek(0)

            return file_stream
        except self.s3.exceptions.ClientError as error:
            raise error

    def _get_object_url(self, bucket: str, key: str) -> str:
        bucket_location = self.s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
        region = ''

        if bucket_location:
            region = f'-{bucket_location}'

        return f'https://s3{region}.amazonaws.com/{bucket}/{key}'
