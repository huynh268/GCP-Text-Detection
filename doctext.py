import argparse
from enum import Enum
import io

from google.cloud import vision
from PIL import Image, ImageDraw
# [END imports]


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, blocks, color):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_blocks]
    draw = ImageDraw.Draw(image)

    for block in blocks:
        draw.polygon([
            block.vertices[0].x, block.vertices[0].y,
            block.vertices[1].x, block.vertices[1].y,
            block.vertices[2].x, block.vertices[2].y,
            block.vertices[3].x, block.vertices[3].y], None, color)
    return image
    # [END draw_blocks]


def get_document_bounds(image_file, feature):
    # [START detect_bounds]
    """Returns document bounds given an image."""
    vision_client = vision.Client()

    bounds = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)
    document = image.detect_full_text()

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    return bounds
    # [END detect_bounds]


def render_doc_text(filein, fileout):
    # [START render_doc_text]
    image = Image.open(filein)
    bounds = get_document_bounds(filein, FeatureType.PAGE)
    draw_boxes(image, bounds, 'blue')
    bounds = get_document_bounds(filein, FeatureType.PARA)
    draw_boxes(image, bounds, 'red')
    bounds = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(image, bounds, 'yellow')

    if fileout is not 0:
        image.save(fileout)
    else:
        image.show()
    # [END render_doc_text]


if __name__ == '__main__':
    # [START run_crop]
    parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()

    parser = argparse.ArgumentParser()
    render_doc_text(args.detect_file, args.out_file)
    # [END run_crop]
# [END full_tutorial]