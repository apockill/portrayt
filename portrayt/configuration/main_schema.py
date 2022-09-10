from pydantic import BaseModel

from portrayt.configuration.prompt_variations import PromptGenerateVariations


class Configuration(BaseModel):

    current_prompt_type: str
    """The current prompt type to be displayed on screen, as a string. For example,
    the value 'PromptGenerateVariations'"""

    # Parameters for each individual prompt type
    prompt_generate_variations: PromptGenerateVariations

    # Default parameters all users will use
    portrait_height: int
    portrait_width: int
