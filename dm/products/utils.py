# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import tempfile

from django.conf import settings

from PIL import Image, ImageDraw, ImageFont


def resize(image, width=None, height=None):
    if width is None and height is not None:
        imageWidth = (imageWidth * height) / imageHeight
        imageHeight = height
    elif width is not None and height is None:
        imageHeight = (imageHeight * width) / imageWidth
        imageWidth = width
    elif width is not None and height is not None:
        imageWidth = width
        imageHeight = width

    return image.resize((int(imageWidth), int(imageHeight)), Image.ANTIALIAS)

def create_resized_image_from_file(file, width=None, height=None):
    tmpfile = tempfile.TemporaryFile()
    image = Image.open(file)
    imageWidth, imageHeight = image.size

    if width and width > 0:
        resize(image, width, height).save(tmpfile, format='JPEG')
    else:
        image = image_from_file(file)
        image.save(tmpfile, format='JPEG', optimize=True, quality=95)
    tmpfile.seek(0)

    return tmpfile, imageWidth, imageHeight
    