from io import BytesIO

import pytest
from mypy_boto3_s3.client import S3Client

from talelio_backend.app_assets.data.asset_store import Asset, AssetStore
from talelio_backend.tests.constants import INITIAL_USER_ID, S3_TEST_BUCKET
from talelio_backend.tests.mocks.data import generate_file_streams

images = [('image.jpeg', 0)]
options = {'bucket': S3_TEST_BUCKET, 'asset_type': Asset.IMAGES.value}


@pytest.mark.parametrize('mocked_s3', [None], indirect=True)
def test_can_upload_to_asset_store(mocked_s3: S3Client) -> None:
    with generate_file_streams(images) as file_streams:
        asset_store = AssetStore(mocked_s3)
        file = file_streams[0]
        uploaded_object_url = asset_store.upload(file, INITIAL_USER_ID, options)

        assert uploaded_object_url == (f'https://s3.amazonaws.com/{S3_TEST_BUCKET}/' +
                                       f'{INITIAL_USER_ID}/{Asset.IMAGES.value}/image.jpeg')


@pytest.mark.parametrize('mocked_s3', [None], indirect=True)
def test_cannot_upload_to_asset_store_with_non_existing_bucket(mocked_s3: S3Client) -> None:
    with generate_file_streams(images) as file_streams:
        asset_store = AssetStore(mocked_s3)
        file = file_streams[0]

        with pytest.raises(mocked_s3.exceptions.NoSuchBucket):
            asset_store.upload(file, INITIAL_USER_ID, {
                'bucket': 'non_existing_bucket',
                'asset_type': Asset.IMAGES.value
            })


@pytest.mark.parametrize('mocked_s3', ['stockholm'], indirect=True)
def test_can_get_object_url_with_region(mocked_s3: S3Client) -> None:
    with generate_file_streams(images) as file_streams:
        asset_store = AssetStore(mocked_s3)
        file = file_streams[0]
        object_url = asset_store.upload(file, INITIAL_USER_ID, options)

        assert object_url == (f'https://s3-stockholm.amazonaws.com/{S3_TEST_BUCKET}/' +
                              f'{INITIAL_USER_ID}/{Asset.IMAGES.value}/image.jpeg')


@pytest.mark.parametrize('mocked_s3', [None], indirect=True)
def test_can_download_user_asset_as_binary_data(mocked_s3: S3Client) -> None:
    with generate_file_streams(images) as file_streams:
        asset_store = AssetStore(mocked_s3)
        file = file_streams[0]

        asset_store.upload(file, INITIAL_USER_ID, options)
        binary_data = asset_store.download(file.name, INITIAL_USER_ID, options)

        assert isinstance(binary_data, BytesIO)


@pytest.mark.parametrize('mocked_s3', [None], indirect=True)
def test_cannot_download_non_existing_user_asset(mocked_s3: S3Client) -> None:
    asset_store = AssetStore(mocked_s3)

    with pytest.raises(mocked_s3.exceptions.ClientError):
        asset_store.download('non-existing-user-asset', INITIAL_USER_ID, options)
