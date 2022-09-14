import math
from typing import Tuple

from PIL import Image


def resize_crop(image: Image, size: Tuple[int, int]) -> Image:
    """Crop the image with a centered rectangle of the specified size"""
    img_format = image.format
    image = image.copy()
    old_size = image.size
    left = (old_size[0] - size[0]) / 2
    top = (old_size[1] - size[1]) / 2
    right = old_size[0] - left
    bottom = old_size[1] - top
    rect = [int(math.ceil(x)) for x in (left, top, right, bottom)]
    left, top, right, bottom = rect
    crop = image.crop((left, top, right, bottom))
    crop.format = img_format
    return crop


def resize_cover(image: Image, size: Tuple[int, int]) -> Image:
    """Resize image by resizing and keeping aspect ratio, then center cropping."""
    img_format = image.format
    img = image.copy()
    img_size = img.size
    ratio = max(size[0] / img_size[0], size[1] / img_size[1])
    new_size = [int(math.ceil(img_size[0] * ratio)), int(math.ceil(img_size[1] * ratio))]
    img = img.resize((new_size[0], new_size[1]), Image.LANCZOS)
    img = resize_crop(img, size)
    img.format = img_format
    return img
