import argparse
from enum import Enum
import io
import re

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw


def draw_boxes(image, color):
    draw = ImageDraw.Draw(image)

    draw.polygon([
        646,252,
        939,252,
        939,303,
        646,303], None, color)

    return image


def get_document(image_file):
    client = vision.ImageAnnotatorClient()

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    return document


def assemble_word(word):
    assembled_word=""
    for symbol in word.symbols:
        assembled_word+=symbol.text
    return assembled_word


def find_word_location(document,word_to_find):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled_word=assemble_word(word)
                    if(assembled_word==word_to_find):
                        return word.bounding_box



def text_within(document,x1,y1,x2,y2): 
    text=""
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        min_x=min(symbol.bounding_box.vertices[0].x,
                            symbol.bounding_box.vertices[1].x,
                            symbol.bounding_box.vertices[2].x,
                            symbol.bounding_box.vertices[3].x)
                        max_x=max(symbol.bounding_box.vertices[0].x,
                            symbol.bounding_box.vertices[1].x,
                            symbol.bounding_box.vertices[2].x,
                            symbol.bounding_box.vertices[3].x)
                        min_y=min(symbol.bounding_box.vertices[0].y,
                            symbol.bounding_box.vertices[1].y,
                            symbol.bounding_box.vertices[2].y,
                            symbol.bounding_box.vertices[3].y)
                        max_y=max(symbol.bounding_box.vertices[0].y,
                            symbol.bounding_box.vertices[1].y,
                            symbol.bounding_box.vertices[2].y,
                            symbol.bounding_box.vertices[3].y)
                        if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):
                            text+=symbol.text
                            if(symbol.property.detected_break.type==1 or 
                               symbol.property.detected_break.type==3):
                                text+=' '
                            if(symbol.property.detected_break.type==2):
                                text+='\t'
                            if(symbol.property.detected_break.type==5):
                                text+='\n'
    return text


def detect_text(image):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(image, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    # read_texts = []

    # for text in texts:
    #     print('\n"{}"'.format(text.description))
    #     read_texts.append(text.description)

        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))
    read_texts = re.findall(r'\w+', texts[0].description)
    print(read_texts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()

    detect_text(args.image)

    # document = get_document(args.image)
    # locations = {}

    # image = Image.open(args.image)
    # for word in ['NOELYN', 'JOYCE']:
    #     locations[word] = find_word_location(document,word)
    # located_text = text_within(document, 646,252,939,303)

    # draw_boxes(image, 'red')
    # image.show()
    # print (locations)
    # print("Located text: %s" % located_text)