from markdown import markdown


class Project:
    def __init__(self, title: str, body: str) -> None:
        self.title = title
        self.body = body
        self.html = ''

    @property
    def convert_body_to_html(self) -> None:
        html = markdown(self.body)
        self.html = html
