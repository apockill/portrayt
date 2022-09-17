from enum import Enum
from typing import Dict, Type

from .base_renderer import BaseRenderer
from .inky_renderer import Inky4Renderer, Inky5Renderer
from .opencv_renderer import OpenCVRenderer


class RendererType(Enum):
    OPENCV = "opencv"
    INKY_4 = "inky_4_inch"
    INKY_5 = "inky_5_inch"


RENDERER_TYPES: Dict[RendererType, Type[BaseRenderer]] = {
    RendererType.OPENCV: OpenCVRenderer,
    RendererType.INKY_5: Inky5Renderer,
    RendererType.INKY_4: Inky4Renderer,
}
"""A dictionary of all available renderer types and their associated object"""
