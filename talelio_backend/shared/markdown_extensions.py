from xml.etree.ElementTree import ElementTree

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class ImageSrcExtractor(Treeprocessor):

    def run(self, root: ElementTree) -> None:
        setattr(self.md, 'images_src', [])

        for image in root.iter('img'):
            image_src = image.get('src')
            self.md.images_src.append(image_src)


class ImageSrcExtractorExtension(Extension):

    def extendMarkdown(self, md: Markdown) -> None:
        image_src_extractor = ImageSrcExtractor(md)
        md.treeprocessors.register(image_src_extractor, 'image_src_extractor', 2)
