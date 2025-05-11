from clang import cindex
from clang.cindex import CursorKind

source_code = """
#include <iostream>

void greet() {
	std::cout << "Hello" << std::endl;
}

void another() {
	greet();
}

int main() {
	greet();
	another();
	return 0;
}
"""

index = cindex.Index.create()

translation_unit = index.parse(
	path="virtual.cpp",
	args=['-std=c++17'],
	unsaved_files=[("virtual.cpp", source_code)],
	options=0
)
print(translation_unit.spelling)

def is_user_function(cursor):
    return (
        cursor.kind == CursorKind.FUNCTION_DECL and
        cursor.is_definition() and
        cursor.location.file and
        cursor.location.file.name == "virtual.cpp"
    )

def get_function_calls(cursor):
    calls = []
    for c in cursor.get_children():
        if c.kind == CursorKind.CALL_EXPR:
            if c.location.file and c.location.file.name == "virtual.cpp":
                calls.append(c.spelling)
        else:
            calls.extend(get_function_calls(c))
    return calls

def extract_user_functions(cursor):
    for child in cursor.get_children():
        if is_user_function(child):
            print(f"\nFunction: {child.spelling}")
            calls = get_function_calls(child)
            for call in calls:
                print(f"  calls: {call}")
        extract_user_functions(child)

extract_user_functions(translation_unit.cursor)
