import libcst as cst

class AnnotationParser(cst.CSTVisitor):
    def __init__(self):
        self.result = ""
        self.subscript_stack = 0
        self.bit_or_stack = 0
    
    def visit_Comma(self, node):
        self.result += ", "
    
    def visit_Subscript(self, node):
        self.subscript_stack += 1
    
    def leave_Subscript(self, original_node):
        self.result += "]"
        
        if self.bit_or_stack > 0:
            self.result += " | "
            self.bit_or_stack -= 1
    
    def visit_Name(self, node):
        self.result += node.value
        if self.subscript_stack > 0:
            self.result += "["
            self.subscript_stack -= 1
            
        elif self.bit_or_stack > 0:
            self.result += " | "
            self.bit_or_stack -= 1
    
    def visit_Attribute(self, node):
        self.result += node.attr.value
        if self.subscript_stack > 0:
            self.result += "["
            self.subscript_stack -= 1
            
        elif self.bit_or_stack > 0:
            self.result += " | "
            self.bit_or_stack -= 1
    
    def visit_SimpleString(self, node):
        self.result += node.value
        if self.subscript_stack > 0:
            self.result += "["
            self.subscript_stack -= 1
            
        elif self.bit_or_stack > 0:
            self.result += " | "
            self.bit_or_stack -= 1
            
    def visit_BitOr(self, node):
        self.bit_or_stack += 1
