# import astroid

# def print_node_info(node, depth):
#     print(f'{' ' * depth}', end='')
#     kind = node.__class__.__name__
#     name = None

#     if hasattr(node, "name"):
#         name = node.name
#     elif kind == "Name":
#         name = node.name  # variable or identifier

#     if name:
#         print(f"{kind} with name: {name}")
#     else:
#         print(f"{kind} (no name)")

# def traverse_ast(node, depth=0):
#     print_node_info(node, depth)

#     for child in node.get_children():
#         traverse_ast(child, depth + 1)

# # Example usage
# source_code = """
# def greet(name):
#     print("Hello", name)

# class Greeter:
#     def greet_all(self, names):
#         for name in names:
#             greet(name)
# """

# module = astroid.parse(source_code)
# traverse_ast(module)


import astroid

source_code = """
def greet(name):
    print("Hello", name)

def greet_all(names):
    for name in names:
        greet(name)
"""

module = astroid.parse(source_code)

def find_and_resolve_calls(node):
    if isinstance(node, astroid.nodes.Call):
        print("Found call to:", node.func.as_string())

        try:
            inferred = next(node.func.infer())
            if isinstance(inferred, astroid.nodes.FunctionDef):
                print("  Resolved to function definition:", inferred.name)
                print(inferred.argnames())
        except astroid.InferenceError:
            print("  Could not resolve function definition")

    for child in node.get_children():
        find_and_resolve_calls(child)

# Start from the top
for node in module.body:
    if isinstance(node, astroid.FunctionDef) and node.name == "greet_all":
        find_and_resolve_calls(node)
