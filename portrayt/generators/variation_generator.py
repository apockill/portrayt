import logging
from pathlib import Path

import replicate
import requests

from portrayt.configuration import PromptGenerateVariations

from .base_generator import BaseGenerator


class VariationGenerator(BaseGenerator[PromptGenerateVariations]):
    def _generate(self, save_dir: Path) -> None:
        model = replicate.models.get("stability-ai/stable-diffusion")
        for variation_id in range(self._params.num_variations):
            image_url = model.predict(
                prompt=self._params.prompt,
                prompt_strength=0.8,
                guidance_scale=7.5,
                num_inference_steps=50,
                seed=self._seed + variation_id,
                width=self._width,
                height=self._height,
            )[0]

            logging.info(f"Generated image {image_url}")

            image_data = requests.get(image_url).content
            image_path = save_dir / f"{variation_id}.png"
            image_path.write_bytes(image_data)
