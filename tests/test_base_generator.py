from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

import pytest
from pydantic import BaseModel

from portrayt.generators import BaseGenerator


class ExampleParams(BaseModel):
    pass


class ExampleGenerator(BaseGenerator[ExampleParams]):
    N_PER_GENERATION = 3
    """How many images to generate per _generate call"""

    def _generate(self, save_dir: Path, start_idx: int) -> None:
        """Generates images in the given directory"""
        for frame_id in range(self.N_PER_GENERATION):
            image_path = save_dir / f"{start_idx + frame_id}.png"
            image_path.write_text("Fake data")


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    with TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def test_generate(temp_dir: Path) -> None:
    generator = ExampleGenerator(
        params=ExampleParams(), height=1, width=2, seed=3, cache_dir=Path(temp_dir)
    )
    expected_image_dir = temp_dir / generator.__class__.__name__
    assert generator.next_idx == 0

    generator.generate(clear_previous=False)
    assert len(list(expected_image_dir.glob("*.png"))) == ExampleGenerator.N_PER_GENERATION
    assert generator.next_idx == ExampleGenerator.N_PER_GENERATION

    generator.generate(clear_previous=False)
    assert len(list(expected_image_dir.glob("*.png"))) == ExampleGenerator.N_PER_GENERATION * 2
    assert generator.next_idx == ExampleGenerator.N_PER_GENERATION * 2

    generator.generate(clear_previous=True)
    assert len(list(expected_image_dir.glob("*.png"))) == ExampleGenerator.N_PER_GENERATION
    assert generator.next_idx == ExampleGenerator.N_PER_GENERATION
