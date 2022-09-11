from pydantic import BaseModel, Field


class PromptGenerateVariations(BaseModel):
    """Information for the Replicate API to generate variations of a prompt"""

    prompt: str
    num_variations: int = Field(default=1, ge=1, le=10)
