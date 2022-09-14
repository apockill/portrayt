from enum import Enum
from typing import Dict, Type

from .base_renderer import BaseRenderer
from .inky_renderer import InkyRenderer
from .opencv_renderer import OpenCVRenderer


class RendererType(Enum):
    OPENCV = "opencv"
    INKY = "inky"


RENDERER_TYPES: Dict[RendererType, Type[BaseRenderer]] = {
    RendererType.OPENCV: OpenCVRenderer,
    RendererType.INKY: InkyRenderer,
}
"""A dictionary of all available renderer types and their associated object"""
