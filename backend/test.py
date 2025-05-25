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

def analyze_call_context(call_node):
    """Analyze the context of a function call"""
    # Get the scope of the call
    scope = call_node.scope()
    
    if isinstance(scope, astroid.Module):
        return "global"
    elif isinstance(scope, (astroid.FunctionDef, astroid.AsyncFunctionDef)):
        return "function"
    elif isinstance(scope, astroid.ClassDef):
        return "class"
    else:
        return "other"

def is_call_global(call_node):
    """Check if a function call is at global scope"""
    current = call_node
    while current.parent:
        current = current.parent
        # If we find a FunctionDef or AsyncFunctionDef parent, it's not global
        if isinstance(current, (astroid.FunctionDef, astroid.AsyncFunctionDef)):
            return False
        # If we reach a Module, it's global
        if isinstance(current, astroid.Module):
            return True
    return False

def get_call_scope_type(call_node):
    """Get the type of scope where the call is made"""
    current = call_node
    while current.parent:
        current = current.parent
        if isinstance(current, astroid.FunctionDef):
            return "function"
        elif isinstance(current, astroid.AsyncFunctionDef):
            return "async_function"
        elif isinstance(current, astroid.ClassDef):
            # Check if we're directly in class body or in a method
            for child in current.body:
                if call_node in child.nodes_of_class(astroid.Call):
                    return "class"
            return "method"  # If not directly in class body
        elif isinstance(current, astroid.Module):
            return "global"
    return "unknown"

# Example usage
code = """
print("global call")  # Global

def my_function():
    print("inside function")  # Not global
    
class MyClass:
    print("in class")  # Global (class level)
    
    def method(self):
        print("in method")  # Not global

if 1:
    sayyes()
"""

tree = astroid.parse(code)
for node in tree.nodes_of_class(astroid.Call):
    if hasattr(node.func, 'name'):
        # print(f"Call to '{node.func.name}': {'Global' if is_call_global(node) else 'Local'}")
        print(f"Call to '{node.func.name}': {analyze_call_context(node)}")