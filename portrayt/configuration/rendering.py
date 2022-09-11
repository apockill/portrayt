from pydantic import BaseModel


class RendererParams(BaseModel):
    seconds_between_image: int
