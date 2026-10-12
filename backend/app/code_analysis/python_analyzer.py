import ast
from pathlib import Path

def analyze_python_file(file_path):
    path = Path(file_path)
    source_code = path.read_text(encoding="utf-8")
    tree = ast.parse(source_code)
    
    results = []
    
    def analyze_body(body, class_path=None):
        for node in body:
        
            if isinstance(node, ast.ClassDef):
                current_class = (
                    f"{class_path}.{node.name}"
                    if class_path
                    else node.name
                )
    
                analyze_body(node.body, current_class)
    
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                results.append({
                    "name": node.name,
                    "type": "method" if class_path else "function",
                    "class": class_path,
                    "file": str(path),
                    "start_line": node.lineno,
                    "end_line": node.end_lineno
                })
    
    analyze_body(tree.body)
    
    return results