from io import BytesIO
from typing import List

from talelio_backend.app_assets.data.asset_store import Asset, AssetStore
from talelio_backend.app_assets.domain.image_model import Image


def upload_images(asset_store: AssetStore, image_streams: List[BytesIO], user_id: int,
                  bucket: str) -> List[str]:
    image_objects_urls = []
    images = Image(image_streams)

    if images.validate:
        renamed_images = images.generate_new_filenames

        options = {'bucket': bucket, 'asset_type': Asset.IMAGES.value}

        for renamed_image in renamed_images:
            image_object_url = asset_store.upload(renamed_image, user_id, options)
            image_objects_urls.append(image_object_url)

    return image_objects_urls
