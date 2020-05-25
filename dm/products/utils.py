# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import tempfile

from django.conf import settings

from PIL import Image, ImageDraw, ImageFont


def resize(file, width=None, height=None):
    image = Image.open(file)
    imageWidth, imageHeight = image.size

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


def image_from_file(file):
    image = Image.open(file)
    return image


def create_resized_image_from_file(file, resolution):
    tmpfile = tempfile.TemporaryFile()
    if resolution > 0:
        resize(file, resolution, None).save(tmpfile, format='JPEG')
    else:
        image_from_file(file).save(tmpfile, format='JPEG')
    tmpfile.seek(0)

    return tmpfile
    