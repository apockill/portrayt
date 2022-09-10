import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generic, TypeVar

from pydantic import BaseModel

PARAMS = TypeVar("PARAMS", bound=BaseModel)


class BaseGenerator(ABC, Generic[PARAMS]):
    """The base class for an object that can call API's and generate a series of images
    and save them to a given directory, in some kind of alphanumeric order"""

    def __init__(self, params: PARAMS, cache_dir: Path) -> None:
        self._params = params
        self.images_dir = cache_dir / self.__class__.__name__

        self.images_dir.mkdir(parents=True, exist_ok=True)

    def generate(self) -> None:
        """Generate new images and then clear the existing images from the cache directory and
        replace them."""
        with TemporaryDirectory() as tempdir:
            self._generate(Path(tempdir))

            # Since generation completed successfully, delete the current images directory and
            # copy the new one over.
            shutil.rmtree(self.images_dir)
            self.images_dir.unlink(missing_ok=True)

            shutil.copytree(tempdir, self.images_dir)

    @abstractmethod
    def _generate(self, save_dir: Path) -> None:
        """Generate set of images using the given parameters to a directory."""
        raise NotImplementedError()
