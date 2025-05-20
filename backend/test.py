from clang import cindex
import os
import tempfile
import shutil

# Create a temporary directory
temp_dir = tempfile.mkdtemp()
try:
    # Write files to the temp directory
    main_cpp_path = os.path.join(temp_dir, "main.cpp")
    rpn_hpp_path = os.path.join(temp_dir, "RPN.hpp")
    rpn_cpp_path = os.path.join(temp_dir, "RPN.cpp")
    
    with open(main_cpp_path, 'w') as f:
        f.write("""
#include "RPN.hpp"

int main(int ac, char** av) {
    RPN a(av);
    a.greet()
    return 0;
}
""")
    
    with open(rpn_hpp_path, 'w') as f:
        f.write("""
#pragma once

class RPN {
public:
    RPN(char** av);
    void greet();
};
""")
    
    with open(rpn_cpp_path, 'w') as f:
        f.write("""
#include "RPN.hpp"

RPN::RPN(char** av) {
    // Implementation
}
void    RPN::greet() {
    std::cout << "hello" << std::endl;
}
""")
    
    # Now parse using the files on disk
    index = cindex.Index.create()
    tu = index.parse(
        path=main_cpp_path,
        args=["-std=c++17"],
        options=0
    )
    
    # Print diagnostics
    for diag in tu.diagnostics:
        print("[Diagnostic]", diag)
    
    # AST dump function
    def dump_ast(cursor, indent=0):
        print("  " * indent + f"{cursor.kind} — {cursor.spelling}")
        for child in cursor.get_children():
            dump_ast(child, indent + 1)
    
    # Run the AST dump
    dump_ast(tu.cursor)

finally:
    # Clean up the temporary directory
    shutil.rmtree(temp_dir)