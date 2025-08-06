from abc import ABC, abstractmethod

class BaseTemplate(ABC):   
    def __init__(self, **kwargs):
        # TODO: fix this
        DEFAULT_LINE_WIDTH = 50
        self.line_width = max(kwargs.get("line_width", 0), DEFAULT_LINE_WIDTH)
        super().__init__()

    @abstractmethod
    def generate_docstring(self, **kwargs) -> list[str]:
        pass