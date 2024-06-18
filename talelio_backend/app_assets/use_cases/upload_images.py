from io import BytesIO
from typing import Dict, List

from talelio_backend.app_assets.data.asset_store import Asset, AssetStore
from talelio_backend.app_assets.domain.image_model import Image
from talelio_backend.data.uow import UnitOfWork


def upload_images(uow: UnitOfWork, asset_store: AssetStore, image_streams: List[BytesIO],
                  user_id: int, bucket: str, api_base_url: str,
                  api_version: str) -> Dict[str, List[str]]:
    with uow:
        user_record = uow.user.get_by_id(user_id)
        username = user_record[4]

        image_objects_urls = []
        images = Image(image_streams)

        if images.validate:
            renamed_images = images.generate_new_filenames

            options = {'bucket': bucket, 'asset_type': Asset.IMAGES.value}

            for renamed_image in renamed_images:
                asset_store.upload(renamed_image, user_id, options)

                image_object_url = (
                    f'{api_base_url}/{api_version}/users/{username}/images/{renamed_image.name}')
                image_objects_urls.append(image_object_url)

        return {'image_objects_urls': image_objects_urls}
