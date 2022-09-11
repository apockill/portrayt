from pydantic import BaseModel


class PromptGenerateVariations(BaseModel):
    """Information for the Replicate API to generate variations of a prompt"""

    prompt: str
    num_variations: int
