from enum import Enum
from typing import Dict, Type

from .base_renderer import BaseRenderer
from .opencv_renderer import OpenCVRenderer


class RendererType(Enum):
    OPENCV = "opencv"


RENDERER_TYPES: Dict[RendererType, Type[BaseRenderer]] = {RendererType.OPENCV: OpenCVRenderer}
"""A dictionary of all available renderer types and their associated object"""
