import logging
import shutil
from abc import ABC, abstractmethod
from itertools import cycle
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

PARAMS = TypeVar("PARAMS", bound=BaseModel)


class BaseGenerator(ABC, Generic[PARAMS]):
    """The base class for an object that can call API's and generate a series of images
    and save them to a given directory, in some kind of alphanumeric order"""

    def __init__(self, params: PARAMS, height: int, width: int, seed: int, cache_dir: Path) -> None:
        # Parameters common to this specific generator
        self._params = params

        # Parameters common to all generators
        self._height = height
        self._width = width
        self._seed = seed
        self._image_generator: Optional[cycle[Path]] = None
        self.images_dir = cache_dir / self.__class__.__name__
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.images_dir=}, {self._params=})"

    @property
    def next_idx(self) -> int:
        """The name of the index the next image will be saved as"""
        image_paths = list(self.images_dir.glob("*.png"))
        image_paths.sort(key=lambda p: int(p.stem))
        if len(image_paths):
            return int(image_paths[-1].stem) + 1
        return 0

    def generate(self, clear_previous: bool) -> None:
        """Generate new images and then clear the existing images from the cache directory and
        replace them.

        :param clear_previous: If True, previous generations will be deleted and replaced by the new
            ones. If false, new oens will be added, in sequential order after the existing ones.
        """

        start_idx = 0 if clear_previous else self.next_idx

        with TemporaryDirectory() as tempdir:
            logging.info(f"Starting generation for {self}. {start_idx=}. This may take a while.")
            self._generate(Path(tempdir), start_idx)
            logging.info("Done generating!")

            if clear_previous:
                # Since generation completed successfully, delete the current images directory and
                # copy the new one over.
                shutil.rmtree(self.images_dir)
                self.images_dir.unlink(missing_ok=True)

            shutil.copytree(tempdir, self.images_dir, dirs_exist_ok=True)

        # Clear the previous image generator
        self._image_generator = None

    @abstractmethod
    def _generate(self, save_dir: Path, start_idx: int) -> None:
        """Generate set of images using the given parameters to a directory."""
        raise NotImplementedError()
