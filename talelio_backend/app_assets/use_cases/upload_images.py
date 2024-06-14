from io import BytesIO
from typing import Dict, List

from talelio_backend.app_assets.data.asset_store import Asset, AssetStore
from talelio_backend.app_assets.domain.image_model import Image


def upload_images(asset_store: AssetStore, image_streams: List[BytesIO], user_id: int,
                  bucket: str) -> Dict[str, List[str]]:
    base_url = 'https://api.talel.io'
    api_version = 'v1'
    image_objects_urls = []
    images = Image(image_streams)

    # TODO: Map user id to username

    if images.validate:
        renamed_images = images.generate_new_filenames

        options = {'bucket': bucket, 'asset_type': Asset.IMAGES.value}

        for renamed_image in renamed_images:
            asset_store.upload(renamed_image, user_id, options)
            image_object_url = f'{base_url}/{api_version}/users/<username>/images/{renamed_image.name}'
            image_objects_urls.append(image_object_url)

    return {'image_objects_urls': image_objects_urls}
