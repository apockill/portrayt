from pydantic import BaseModel, Field


class PromptGenerateVariations(BaseModel):
    """Information for the Replicate API to generate variations of a prompt"""

    prompt: str
    num_variations: int
    prompt_strength: float = Field(default=0.8, ge=0.0, le=1.0)
