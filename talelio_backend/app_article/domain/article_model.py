from markdown import markdown

from talelio_backend.shared.utils import generate_slug


class Article:

    def __init__(self, title: str, body: str) -> None:
        self.title = title
        self.slug = generate_slug(title)
        self.body = body
        self.html = ''

    @property
    def convert_body_to_html(self) -> None:
        html = markdown(self.body, extensions=['fenced_code'])
        self.html = html
