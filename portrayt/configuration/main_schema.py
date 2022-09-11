from pydantic import BaseModel

from portrayt.configuration import RendererParams
from portrayt.configuration.prompt_interpolation_animation import PromptInterpolationAnimation
from portrayt.configuration.prompt_variations import PromptGenerateVariations


class Configuration(BaseModel):

    current_prompt_type: str
    """The current prompt type to be displayed on screen, as a string. For example,
    the value 'PromptGenerateVariations'"""

    # Parameters for each individual prompt type
    prompt_generate_variations: PromptGenerateVariations
    prompt_interpolation_animation: PromptInterpolationAnimation

    # Renderer configuration
    renderer: RendererParams

    # Default parameters all users will use
    portrait_height: int
    portrait_width: int
    seed: int

    class Config:
        validate_assignment = True
        validate_all = True
