import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple

from inky.inky_uc8159 import Inky as Inky7Color
from PIL import Image

from portrayt.renderers import BaseRenderer

from .crop_utils import resize_cover


class _InkyRenderer(BaseRenderer, ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.display = Inky7Color(resolution=self.resolution)

        logging.info(f"Initialized Inky with resolution {self.display.resolution}")

    def _render(self, image_path: Path) -> None:
        image = Image.open(image_path)
        resized = resize_cover(image, self.display.resolution)

        self.display.set_image(resized, saturation=0.6)
        self.display.show()

    @property
    @abstractmethod
    def resolution(self) -> Tuple[float, float]:
        """Enter the resolution of the inky screen here"""


class Inky5Renderer(_InkyRenderer):
    resolution = (600, 448)


class Inky4Renderer(_InkyRenderer):
    resolution = (640, 400)
