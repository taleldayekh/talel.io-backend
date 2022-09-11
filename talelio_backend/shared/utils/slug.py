from re import findall, sub
from unicodedata import category, normalize


def generate_slug(text: str) -> str:
    text = text.lower()
    text = ''.join(findall(r'[\w\s]', text))
    text = sub(' +', '-', text)
    text = ''.join(character for character in normalize('NFKD', text)
                   if category(character) != 'Mn')

    return text
