from xml.etree.ElementTree import Element

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class ElementAttributes(Treeprocessor):

    def run(self, root: Element) -> None:
        for image_element in root.iter('img'):
            image_element.set('loading', 'lazy')

        for anchor_element in root.iter('a'):
            anchor_element.set('target', '_blank')


class ElementAttributesExtension(Extension):

    def extendMarkdown(self, md: Markdown) -> None:
        image_lazy_load_attribute = ElementAttributes(md)
        md.treeprocessors.register(image_lazy_load_attribute, 'image_lazy_load_attribute', 1)
