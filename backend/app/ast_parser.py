import ast
from platform import node

class FunctionExtractor(ast.NodeVisitor):

    def __init__(self):

        self.functions = []
        self.function_stack = []

        self.classes = []
        self.class_stack = []

        self.imports = []

    def visit_Import(self, node):

        for alias in node.names:
            self.imports.append({
                "module": alias.name,
                "alias": alias.asname,
                "type": "import"
            })


    def visit_ImportFrom(self, node):

        for alias in node.names:
            self.imports.append({
                "module": node.module,
                "name": alias.name,
                "alias": alias.asname,
                "level": node.level,
                "type": "from_import"
            })

    def visit_ClassDef(self, node):

        class_info = {
            "name": node.name,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "parent_class": self.class_stack[-1] if self.class_stack else None,
            "base_classes": [
                ast.unparse(base) for base in node.bases
            ]
        }

        self.classes.append(class_info)

        self.class_stack.append(node.name)

        self.generic_visit(node)

        self.class_stack.pop()

    def parameters(self, node):

        params = []

        args = node.args.args
        defaults = node.args.defaults

        start = len(args) - len(defaults)

        for i, arg in enumerate(args):

            default = None

            if i >= start:
                default = ast.unparse(defaults[i - start])
            
            params.append({
                "name": arg.arg,
                "default": default,
                "annotation": ast.unparse(arg.annotation) if arg.annotation else None
            })

        return params

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_FunctionDef(self, node):

        if self.function_stack:
            function_type = "nested"
        elif self.class_stack:
            function_type = "method"
        else:
            function_type = "function"

        decorators = []

        for decorator in node.decorator_list:
            decorators.append(ast.unparse(decorator))

        function_info = {
            "name": node.name,
            "parameters": self.parameters(node),
            "return_annotation": ast.unparse(node.returns) if node.returns else None,
            "decorators": decorators,
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "type": function_type,
            "class_name": self.class_stack[-1] if self.class_stack else None,
            "parent_function": self.function_stack[-1] if self.function_stack else None,
            "start_line": node.lineno,
            "end_line": node.end_lineno
        }

        self.functions.append(function_info)

        self.function_stack.append(node.name)
        self.generic_visit(node)
        self.function_stack.pop()

def extract_functions(source_code):

    try:
        tree = ast.parse(source_code)

        extractor = FunctionExtractor();
        extractor.visit(tree)

        return {
            "success": True,
            "functions": extractor.functions,
            "classes": extractor.classes,
            "imports": extractor.imports,
            "error": None
        }
    
    except SyntaxError as error:
        return {
            "success": False,
            "functions": [],
            "classes": [],
            "imports": [],
            "error": f"SyntaxError: {error}"
        }
