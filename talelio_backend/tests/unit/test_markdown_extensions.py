# pylint: disable=E1101
from markdown import Markdown

from talelio_backend.shared.markdown_extensions import ImageSrcExtractorExtension
from talelio_backend.tests.mocks.example_markdown import (ART_TO_ENGINEERING_ARTICLE_BODY,
                                                          SERVER_PROJECT_ARCHITECTURE_DIAGRAM_URL,
                                                          SERVER_PROJECT_FEATURED_IMAGE_URL,
                                                          TALELIO_SERVER_PROJECT_BODY)


def test_image_src_extractor_can_extract_image_urls_list() -> None:
    markdown = Markdown(extensions=[ImageSrcExtractorExtension()])
    markdown.convert(TALELIO_SERVER_PROJECT_BODY)

    image_urls = markdown.images_src  # type: ignore

    assert len(image_urls) == 2
    assert image_urls[0] == SERVER_PROJECT_FEATURED_IMAGE_URL
    assert image_urls[1] == SERVER_PROJECT_ARCHITECTURE_DIAGRAM_URL


def test_images_src_returns_empty_list_if_image_urls_not_available() -> None:
    markdown = Markdown(extensions=[ImageSrcExtractorExtension()])
    markdown.convert(ART_TO_ENGINEERING_ARTICLE_BODY)

    image_urls = markdown.images_src  # type: ignore

    assert not image_urls
