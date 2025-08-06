import libcst as cst

from autodocs.core.templates import DocStyle
from autodocs.core.annotation import AnnotationParser

class ExceptionCollector(cst.CSTVisitor):
    def __init__(self):
        self._exceptions: set[str] = set()
        
    def visit_Raise(self, node):
        if node.exc:
            if isinstance(node.exc, cst.Name):
                self._exceptions.add(node.exc.value)
            
            elif isinstance(node.exc, cst.Attribute):
                self._exceptions.add(node.exc.attr.value)
                
            elif isinstance(node.exc, cst.Call):
                if isinstance(node.exc.func, cst.Name):
                    self._exceptions.add(node.exc.func.value)
                    
                elif isinstance(node.exc.func, cst.Attribute):
                    self._exceptions.add(node.exc.func.attr.value)
                    
                else:
                    pass
            
            else:
                pass
    
    @property
    def exceptions(self):
        return list(self._exceptions)

class ParameterCollector(cst.CSTVisitor):
    def __init__(self):
        self.params: list[tuple[str, str]] = []
        
        # config
        self.allow_star_args = False
    
    def visit_Param(self, node: cst.Param):
        if node.name.value == "self" or node.name.value == "cls":
            return False
        
        if not self.allow_star_args and (node.star == "*" or node.star == "**"):
            return False
        
        param_name = node.name.value
        
        if isinstance(node.star, str):
            param_name = node.star + param_name
        
        if not node.annotation:
            self.params.append((param_name, "[unknown]"))
            return False
        
        parser = AnnotationParser()
        node.annotation.visit(parser)
        self.params.append((param_name, parser.result))
        return False

class FunctionDocStringAnnotator(cst.CSTTransformer):
    def __init__(self, indent_style: str):
        self.default_indent = indent_style
        self.current_indent = 0
        
        # config
        self.template_config = {}
        self.template = DocStyle.GOOGLE.value(**self.template_config)
        self.prune_body = False
        
        self.generate_summary = False
        self.generate_references = False
        self.generate_notes = False
        self.generate_examples = False
        
    def visit_IndentedBlock(self, node):
        self.current_indent += 1
        
    def leave_IndentedBlock(self, original_node, updated_node):
        self.current_indent -= 1
        return updated_node
    
    def visit_FunctionDef(self, node):
        return super().visit_FunctionDef(node)
        
    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.CSTNode:
        params_collector = ParameterCollector()
        updated_node.params.visit(params_collector)
        
        annotation_parser = AnnotationParser()
        if updated_node.returns:
            updated_node.returns.annotation.visit(annotation_parser)
        
        exception_collector = ExceptionCollector()
        updated_node.body.visit(exception_collector)
        
        function_info = {
            "summary": generate_function_summary(updated_node),
            "parameters": params_collector.params,
            "returns": annotation_parser.result if updated_node.returns else "[unknown]",
            "references": "[references]",
            "notes": "[notes]",
            "examples": generate_function_usage_examples(updated_node),
            "raises": exception_collector.exceptions
        }
        
        generated_docstring = self.generate_function_docstring(**function_info)
        
        body_stmts = updated_node.body.body
        
        docstring = cst.SimpleStatementLine(
            body=[cst.Expr(value=cst.SimpleString(generated_docstring))]
        )
        
        if self.prune_body:
            body_stmts = []
        
        new_body = [docstring] + list(body_stmts)
        
        return updated_node.with_changes(body=updated_node.body.with_changes(body=new_body))
    
    def generate_function_docstring(
        self,
        summary: str, 
        parameters: list[tuple[str, str]], 
        returns: str, 
        references: str, 
        notes: str,
        examples: str,
        raises: list[str]
        ) -> str:
        
        args = {
            "indent": self.default_indent,
            "params": parameters,
            "returns": returns,
            "raises": raises,
        }
        
        lines = self.template.generate_docstring(**args)
        docstring = '"""\n'
        
        for line in lines:
            docstring += self.default_indent * (self.current_indent + 1) + line + "\n"
            
        docstring += f'{self.default_indent * (self.current_indent + 1)}"""'
        
        return docstring

# TODO
def generate_function_usage_examples(fn_node):
    return "[examples]"

# TODO
def generate_function_summary(fn_node):
    return "[summary]"