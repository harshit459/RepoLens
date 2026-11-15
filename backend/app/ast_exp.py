import ast 

code = """
def create_user(name, email, age=18):
    return name
def user(name1, email1):
    return name
"""

tree = ast.parse(code)

function = tree.body[0]

print(ast.dump(tree, indent=4))

print("Function name:", function.name)

for arg in function.args.args:
    print(arg.arg)