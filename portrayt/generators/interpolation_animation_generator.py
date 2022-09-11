import logging
from itertools import count
from pathlib import Path
from tempfile import NamedTemporaryFile

import cv2
import replicate
import requests

from portrayt.configuration import PromptInterpolationAnimation

from .base_generator import BaseGenerator


class InterpolationAnimationGenerator(BaseGenerator[PromptInterpolationAnimation]):
    def _generate(self, save_dir: Path, start_idx: int) -> None:

        model = replicate.models.get("andreasjansson/stable-diffusion-animation")
        gif_url = next(
            model.predict(
                prompt_start=self._params.prompt_start,
                prompt_end=self._params.prompt_end,
                propmt_strength=self._params.prompt_strength,
                num_animation_frames=self._params.num_animation_frames,
                gif_ping_pong=self._params.seamless_loop,
                width=self._width,
                height=self._height,
                seed=self._seed,
                film_interpolation=True,
                num_interpolation_steps=1,
                guidance_scale=7.5,
                gif_frames_per_second=1,  # irrelevant
                output_format="gif",
                num_inference_steps=50,
            )
        )

        logging.info(f"Generated gif {gif_url}")

        gif_data = requests.get(gif_url).content

        # Write the gif to a temporary file, then save each individual frame
        with NamedTemporaryFile() as gif_path:
            Path(gif_path.name).write_bytes(gif_data)

            # Open the gif and save the individual frames
            gif = cv2.VideoCapture(str(gif_path.name))
            for frame_id in count():
                ret, image_bgr = gif.read()
                if not ret:
                    break

                image_path = save_dir / f"{start_idx + frame_id}.png"
                cv2.imwrite(str(image_path), image_bgr)
