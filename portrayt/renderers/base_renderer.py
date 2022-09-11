import logging
from abc import ABC, abstractmethod
from pathlib import Path
from threading import Event, Thread
from typing import Any, Optional

from portrayt.configuration import RendererParams
from portrayt.generators import BaseGenerator


class BaseRenderer(ABC):
    def __init__(self, generator: BaseGenerator[Any], params: RendererParams) -> None:
        self._generator = generator
        self._closing = Event()
        self._parameters_changed = Event()

        self._current_image: Optional[Path] = None
        self._params = params

        self._render_thread = Thread(target=self._render_loop, daemon=True)
        self._render_thread.start()

    def _render_loop(self) -> None:
        """A thread that is started on construction and runs 'render' on a timer"""

        while not self._closing.is_set():
            try:
                next_image = self._generator.next()
            except StopIteration:
                logging.warning(f"No images found to render! {self._generator=}")
            else:
                self._current_image = next_image
                self._render(self._current_image)

            # Wait before updating the next image
            self._parameters_changed.wait(timeout=self._params.seconds_between_images)
            self._parameters_changed.clear()

    def update_generator(self, generator: BaseGenerator[Any]) -> None:
        self._generator = generator
        self._parameters_changed.set()

    @property
    def current_image(self) -> Optional[Path]:
        """Returns the current image being displayed"""
        return self._current_image

    @abstractmethod
    def _render(self, image_path: Path) -> None:
        """Render the current image"""

    def close(self) -> None:
        self._closing.set()
        self._parameters_changed.set()
        self._render_thread.join()
