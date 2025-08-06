from .google import GoogleTemplate
from .numpy import NumPyTemplate

from enum import Enum

class DocStyle(Enum):
    GOOGLE = GoogleTemplate
    NUMPY = NumPyTemplate

__all__ = [
    "DocStyle",
]