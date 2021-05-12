import pytest

from talelio_backend.app_assets.domain.image_model import Image
from talelio_backend.constants import MAX_IMAGE_FILE_SIZE
from talelio_backend.core.exceptions import ImageError
from talelio_backend.tests.mocks.data import generate_file_streams


def test_validates_allowed_image_types() -> None:
    with generate_file_streams([('image.gif', 0), ('image.jpeg', 0),
                                ('image.png', 0)]) as file_streams:
        images = Image(file_streams)
        assert images.validate_type
        assert images.validate


def test_does_not_validate_unallowed_image_types() -> None:
    with generate_file_streams([('image.tiff', 0)]) as file_streams:
        images = Image(file_streams)
        assert not images.validate_type

        with pytest.raises(ImageError, match='One or more image files are of invalid type'):
            assert not images.validate


def test_does_not_validate_non_image_files() -> None:
    with generate_file_streams([('image.jpeg', 0), ('document.pdf', 0)]) as file_streams:
        images = Image(file_streams)
        assert not images.validate_type

        with pytest.raises(ImageError, match='One or more image files are of invalid type'):
            assert not images.validate


def test_validates_images_within_max_file_size() -> None:
    one_mb_file_size = 1 * 1024 * 1024

    with generate_file_streams([('image.jpeg', one_mb_file_size),
                                ('image.png', MAX_IMAGE_FILE_SIZE)]) as file_streams:
        images = Image(file_streams)
        assert images.validate_size
        assert images.validate


def test_does_not_validate_images_above_max_file_size() -> None:
    three_mb_file_size = 3 * 1024 * 1024

    with generate_file_streams([('image.jpeg', three_mb_file_size)]) as file_streams:
        images = Image(file_streams)
        assert not images.validate_size

        with pytest.raises(ImageError, match='One or more image file sizes are too large'):
            assert not images.validate
