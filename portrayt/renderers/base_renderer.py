import logging
import random
from abc import ABC, abstractmethod
from pathlib import Path
from threading import Event, Thread
from time import sleep
from typing import List, Optional

from portrayt.configuration import RendererParams


class BaseRenderer(ABC):
    def __init__(self, images_dir: Path, params: RendererParams) -> None:
        self._closing = Event()
        self._parameters_changed = Event()

        self._params = params

        # Rendering modes
        self._images_dir = images_dir
        self._current_image: Optional[Path] = None

        self._render_thread = Thread(target=self._render_loop, daemon=True)
        self._render_thread.start()

    def _render_loop(self) -> None:
        """A thread that is started on construction and runs 'render' on a timer"""

        while not self._closing.is_set():
            next_image = self._next_image()
            self._current_image = next_image
            self._parameters_changed.clear()

            # Render the next image, if there is one
            if self._current_image is None:
                logging.warning(f"No images found to render in: {self._images_dir}")
            else:
                self._render(self._current_image)

            # Wait before updating the next image
            self._parameters_changed.wait(timeout=self._params.seconds_between_images)

    def update_image_dir(self, images_dir: Path) -> None:
        if self._images_dir != images_dir:
            # Reset the position in the queue by setting current image to None
            self._current_image = None

        self._images_dir = images_dir
        self._parameters_changed.set()

        # Get the new 'current image'
        self._wait_for_parameters_updated()

    @property
    def current_image(self) -> Optional[Path]:
        """Returns the current image being displayed"""
        return self._current_image

    def next(self) -> None:
        self._parameters_changed.set()
        self._wait_for_parameters_updated()

    def toggle_shuffle(self) -> None:
        self._params.shuffle = not self._params.shuffle
        self._parameters_changed.set()
        self._wait_for_parameters_updated()

    def _wait_for_parameters_updated(self) -> None:
        """Wait until the parameter change has been observed"""
        while self._parameters_changed.is_set():
            sleep(0.1)

    @property
    def _image_paths(self) -> List[Path]:
        image_paths = list(self._images_dir.glob("*.png"))
        image_paths.sort(key=lambda p: int(p.stem))
        return image_paths

    def _next_image(self) -> Optional[Path]:
        paths = self._image_paths
        if self._params.shuffle:
            # Always shuffle in a consistent order so that the images that appear are
            # new, instead of shuffling each time another image is called which could
            # cause multiple renders in a row (or nearby) to show the same image
            seeded_random = random.Random(x="mmm sunflower seeds")
            seeded_random.shuffle(paths)

        try:
            next_idx = paths.index(self._current_image) + 1  # type: ignore
        except ValueError:
            next_idx = 0

        try:
            if next_idx == len(paths):
                return paths[0]
            else:
                return paths[next_idx]
        except IndexError:
            return None

    @abstractmethod
    def _render(self, image_path: Path) -> None:
        """Render the current image"""

    def close(self) -> None:
        self._closing.set()
        self._parameters_changed.set()
        self._render_thread.join()
