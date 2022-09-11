from pydantic import BaseModel, Field


class PromptInterpolationAnimation(BaseModel):
    """Information for the Replicate API to generate variations of a prompt"""

    prompt_start: str
    prompt_end: str
    prompt_strength: float
    seamless_loop: bool
    num_animation_frames: int = Field(default=15, ge=3, le=60)
