from io import BytesIO

from talelio_backend.app_assets.data.asset_store import Asset, AssetStore
from talelio_backend.data.uow import UnitOfWork


def download_image(uow: UnitOfWork, asset_store: AssetStore, image_file_name: str, username: str,
                   bucket: str) -> BytesIO:
    user_id = uow.user.get_by_username(username)

    # TODO: Throw exception if user does not exist

    options = {'bucket': bucket, 'asset_type': Asset.IMAGES.value}

    return asset_store.download(image_file_name, user_id, options)
