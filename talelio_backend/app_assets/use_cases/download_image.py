from io import BytesIO

from talelio_backend.app_assets.data.asset_store import Asset, AssetStore
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.shared.exceptions import UserError


def download_image(uow: UnitOfWork, asset_store: AssetStore, image_file_name: str, username: str,
                   bucket: str) -> BytesIO:
    with uow:
        user_record = uow.user.get_by_username(username)

        if not user_record:
            raise UserError(f"User with username '{username}' does not exist")

        user_id = user_record[0]
        options = {'bucket': bucket, 'asset_type': Asset.IMAGES.value}

        return asset_store.download(image_file_name, user_id, options)
