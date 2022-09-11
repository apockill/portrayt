from typing import Literal

from pydantic import BaseModel

from portrayt.configuration import RendererParams
from portrayt.configuration.prompt_variations import PromptGenerateVariations

_VALID_FRAME_SIZES = Literal[128, 256, 512, 768, 1024]


class Configuration(BaseModel):

    current_prompt_type: str
    """The current prompt type to be displayed on screen, as a string. For example,
    the value 'PromptGenerateVariations'"""

    # Parameters for each individual prompt type
    prompt_generate_variations: PromptGenerateVariations

    # Renderer configuration
    renderer: RendererParams

    # Default parameters all users will use
    portrait_height: _VALID_FRAME_SIZES
    portrait_width: _VALID_FRAME_SIZES
    seed: int

    class Config:
        validate_assignment = True
        validate_all = True
