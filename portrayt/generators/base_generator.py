import logging
import shutil
from abc import ABC, abstractmethod
from itertools import cycle
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generic, List, Optional, TypeVar

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

    def next(self) -> Path:
        """Return the 'next' image in the generation loop"""
        if self._image_generator is None:
            self._image_generator = cycle(self.image_paths)
        return next(self._image_generator)

    @property
    def image_paths(self) -> List[Path]:
        image_paths = list(self.images_dir.glob("*.png"))
        image_paths.sort(key=lambda p: int(p.stem))
        return image_paths

    def generate(self, clear_previous: bool) -> None:
        """Generate new images and then clear the existing images from the cache directory and
        replace them.

        :param clear_previous: If True, previous generations will be deleted and replaced by the new
            ones. If false, new oens will be added, in sequential order after the existing ones.
        """

        if not clear_previous and len(self.image_paths):
            start_idx = int(self.image_paths[-1].stem) + 1
        else:
            start_idx = 0

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
