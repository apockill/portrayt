from pydantic import BaseModel


class PromptInterpolationAnimation(BaseModel):
    """Information for the Replicate API to generate variations of a prompt"""

    prompt_start: str
    prompt_end: str
    prompt_strength: float
    num_animation_frames: int
