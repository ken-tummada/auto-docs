from .base import BaseTemplate

class NumPyTemplate(BaseTemplate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    
    def generate_docstring(self, **kwargs) -> list[str]:
        """
        Args:
            indent (str): base indentation
            summary (str): a summary of class or function
            params (list[tuple[str, str]]): 
            returns (str)
        Returns
            str: the generated docstring
        """
        
        # TODO: implement this
        pass