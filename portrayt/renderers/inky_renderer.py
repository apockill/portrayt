import logging
from pathlib import Path
from typing import Any

from inky.inky_uc8159 import Inky as Inky7Color
from PIL import Image

from portrayt.renderers import BaseRenderer

from .crop_utils import resize_cover

_INKY_SKUS = {"4_inch": (640, 400), "5.7_inch": ((600, 448))}


class InkyRenderer(BaseRenderer):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.display = Inky7Color(resolution=_INKY_SKUS["4_inch"])

        logging.info(f"Initialized Inky with resolution {self.display.resolution}")

    def _render(self, image_path: Path) -> None:
        image = Image.open(image_path)
        resized = resize_cover(image, self.display.resolution)

        self.display.set_image(resized)
        self.display.show()
