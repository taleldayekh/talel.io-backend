# pylint: disable=R0902
from markdown import Markdown

from talelio_backend.shared.markdown_extensions import ElementAttributesExtension
from talelio_backend.shared.utils.slug import generate_slug


class Article:
    __article_base_url = 'https://www.talel.io/articles/'

    def __init__(self, title: str, body: str, meta_description: str, featured_image: str) -> None:
        self.title = title
        self.slug = generate_slug(title)
        self.body = body
        self.meta_description = meta_description
        self.html = ''
        self.table_of_contents = ''
        self.featured_image = featured_image
        self.url = self.__article_base_url + self.slug

        self.__markdown = Markdown(
            extensions=['attr_list', 'tables', 'toc', 'fenced_code', 'md_in_html',
                        ElementAttributesExtension()])

    @property
    def convert_body_to_html(self) -> None:
        html = self.__markdown.convert(self.body)
        self.html = html

    @property
    def generate_table_of_contents(self) -> None:
        table_of_contents = self.__markdown.toc  # type: ignore # pylint: disable=E1101
        self.table_of_contents = table_of_contents
