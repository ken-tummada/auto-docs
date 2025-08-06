from .base import BaseTemplate

class GoogleTemplate(BaseTemplate):
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
        
        lines = []
        indent = kwargs["indent"] if kwargs["indent"] else " " * 4
        
        if "summary" in kwargs:
            lines += self._generate_section_summary(kwargs["summary"])
            
        if "params" in kwargs:
            lines += self._generate_section_params(kwargs["params"], indent)
            
        if "returns" in kwargs:
            lines += self._generate_section_returns(kwargs["returns"], indent)
            
        if "raises" in kwargs:
            lines += self._generate_section_raises(kwargs["raises"], indent)
        
        return lines
    
    def _generate_section_summary(self, summary: str) -> list[str]:
        lines = [""]
        width = 0
        for word in summary.split(" "):
            if width + len(word) > self.line_width:
                lines.append(word)
                width = len(word)
            else:
                lines[-1].append(" " + word)
                
        return lines
    
    def _generate_section_params(self, params: list[tuple[str, str]], indent: str) -> list[str]:
        if len(params) == 0:
            return []
        
        lines = ["Args:"]
        for param in params:
            lines.append(f"{indent}{param[0]} ({param[1]})")
            
        return lines
    
    def _generate_section_returns(self, returns: str, indent: str) -> list[str]:
        lines = ["Returns:", f"{indent}{returns}"]
            
        return lines
    
    def _generate_section_raises(self, raises: list[str], indent: str) -> list[str]:
        if len(raises) == 0:
            return []
        
        lines = ["Raises:"]
        for exception in raises:
            lines.append(f"{indent}{exception}")
        
        return lines
    
    def _generate_section_references(self, references: str) -> list[str]:
        pass
    
    def _generate_section_notes(self, notes: list[str]) -> list[str]:
        pass
    
    def _generate_section_examples(self, args: list[str]) -> list[str]:
        pass