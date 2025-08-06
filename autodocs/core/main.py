from string import Template
import libcst as cst

class FunctionCollector(cst.CSTVisitor):
    def __init__(self):
        self.functions: list[cst.FunctionDef] = []

    def visit_FunctionDef(self, node: cst.FunctionDef):
        self.functions.append(node)
        
def get_function_returns(func_node: cst.FunctionDef) -> str:
    """
    Only works with function that are annotated
    """
    
    if not func_node.returns:
        return "[unknown]"

    return parse_annotation(func_node.returns)


# TODO: infer a function return type
def infer_function_returns(func_node: cst.FunctionDef) -> list[str]:
    """What should we do if there are multiple return points

    Args:
        func_node (cst.FunctionDef): _description_

    Returns:
        list[str]: _description_
    """
    pass

def subscript_dfs(current: cst.Subscript) -> str:
    res = ""
    
    if isinstance(current.value, cst.Name):
        res += current.value.value + "["
        
    if isinstance(current.value, cst.Attribute):
        res += current.value.attr.value + "["
        
    for s in current.slice:
        if isinstance(s.slice, cst.Index):
            if isinstance(s.slice.value, cst.Subscript):
                res += subscript_dfs(s.slice.value) + ", "
            
            elif isinstance(s.slice.value, cst.Name):
                res += s.slice.value.value + ", "
                
            elif isinstance(s.slice.value, cst.Attribute):
                res += s.slice.value.attr.value + ", "
            
            elif isinstance(s.slice.value, cst.SimpleString):
                res += s.slice.value.value
        
            else:
                res += f"[{str(type(s.value))}], "
                
    return res[:-2] + "]"

def parse_annotation(annotation_node: cst.Annotation) -> str:
    if not annotation_node or not annotation_node.annotation:
        return "[unknown]"
    
    expr = annotation_node.annotation
    
    if isinstance(expr, cst.Name):
        res = expr.value
        
    elif isinstance(expr, cst.Subscript):
        res = subscript_dfs(expr)
    
    elif isinstance(expr, cst.Attribute):
        res = expr.attr.value
        
    elif isinstance(expr, cst.SimpleString):
        res = expr.value
    
    else:
        res = f"[unknown cst type: {str(type(expr))}]"
    
    return res

def get_function_arguments(func_node: cst.FunctionDef) -> list[tuple[str, str]]:
    arguments = []
    
    params = func_node.params

    # Positional-only parameters
    for param in params.posonly_params:
        name = param.name.value
        annotation = parse_annotation(param.annotation)
        arguments.append((name, annotation))

    # Positional or keyword parameters
    for param in params.params:
        name = param.name.value
        annotation = parse_annotation(param.annotation)
        arguments.append((name, annotation))

    # *args
    if params.star_arg is not None and not isinstance(params.star_arg, cst.MaybeSentinel) and not isinstance(params.star_arg, cst.ParamStar):
        name = "*" + params.star_arg.name.value
        annotation = parse_annotation(params.star_arg.annotation)
        arguments.append((name, annotation))

    # Keyword-only parameters
    for param in params.kwonly_params:
        name = param.name.value
        annotation = parse_annotation(param.annotation)
        arguments.append((name, annotation))

    # **kwargs
    if params.star_kwarg is not None:
        name = "**" + params.star_kwarg.name.value
        annotation = parse_annotation(params.star_kwarg.annotation)
        arguments.append((name, annotation))

    return arguments

def parse_file(file_path: str) -> cst.Module:
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()
    
    return cst.parse_module(source_code)

def write_file(file_path: str, module: cst.Module) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(module.code)