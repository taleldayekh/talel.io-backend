from typing import Optional

from markdown import Markdown

from talelio_backend.shared.markdown_extensions import ImageSrcExtractorExtension
from talelio_backend.shared.utils import generate_slug


class Article:

    def __init__(self, title: str, body: str, featured_image: Optional[str] = '') -> None:
        self.title = title
        self.slug = generate_slug(title)
        self.body = body
        self.html = ''
        self.featured_image = featured_image

        self.markdown = Markdown(extensions=['fenced_code', ImageSrcExtractorExtension()])

    @property
    def convert_body_to_html(self) -> None:
        html = self.markdown.convert(self.body)
        self.html = html

    @property
    def set_featured_image(self) -> None:
        image_urls = self.markdown.images_src  # type: ignore # pylint: disable=E1101

        self.featured_image = image_urls[0] if len(image_urls) else self.featured_image
