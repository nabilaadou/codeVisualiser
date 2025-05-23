from clang import cindex
import tempfile
import os

def deep_debug_clang(main_cpp_content, header_content, header_path):
    """
    Comprehensive debugging for clang parsing issues
    """
    
    # Create temporary files
    temp_dir = tempfile.mkdtemp()
    try:
        main_path = os.path.join(temp_dir, "main.cpp")
        zombie_h_path = os.path.join(temp_dir, "Zombie.h")
        
        with open(main_path, 'w') as f:
            f.write(main_cpp_content)
        with open(zombie_h_path, 'w') as f:
            f.write(header_content)
        
        index = cindex.Index.create()
        
        # Parse with maximum verbosity
        tu = index.parse(
            path=main_path,
            args=[
                "-std=c++17", 
                f"-I{temp_dir}",
                "-v",  # Verbose
                "-H",  # Show headers
            ],
            options=(cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD |
                    cindex.TranslationUnit.PARSE_INCOMPLETE)
        )
        
        print("=== DIAGNOSTICS ===")
        for diag in tu.diagnostics:
            print(f"[{diag.severity}] {diag}")
        
        print("\n=== SYMBOL TABLE DEBUG ===")
        def analyze_symbols(cursor, depth=0):
            indent = "  " * depth
            
            # Print all cursors with their details
            if cursor.spelling and ("newZombie" in cursor.spelling or 
                                  "deleteZombie" in cursor.spelling or
                                  cursor.kind == cindex.CursorKind.CALL_EXPR):
                print(f"{indent}>>> {cursor.kind} — '{cursor.spelling}'")
                print(f"{indent}    Type: {cursor.type.spelling if cursor.type else 'None'}")
                print(f"{indent}    Location: {cursor.location}")
                if cursor.referenced:
                    print(f"{indent}    References: {cursor.referenced.kind} — {cursor.referenced.spelling}")
                print(f"{indent}    USR: {cursor.get_usr()}")
                print()
            
            for child in cursor.get_children():
                analyze_symbols(child, depth + 1)
        
        analyze_symbols(tu.cursor)
        
        print("\n=== FIND ALL FUNCTION DECLARATIONS ===")
        def find_function_decls(cursor, depth=0):
            if cursor.kind == cindex.CursorKind.FUNCTION_DECL:
                print(f"Function: {cursor.spelling}")
                print(f"  Type: {cursor.type.spelling}")
                print(f"  Location: {cursor.location}")
                print(f"  USR: {cursor.get_usr()}")
                print()
            
            for child in cursor.get_children():
                find_function_decls(child, depth + 1)
        
        find_function_decls(tu.cursor)
        
        print("\n=== MANUAL SYMBOL LOOKUP ===")
        # Try to manually find the symbol
        def find_cursor_by_name(cursor, name):
            if cursor.spelling == name:
                return cursor
            for child in cursor.get_children():
                result = find_cursor_by_name(child, name)
                if result:
                    return result
            return None
        
        newZombie_cursor = find_cursor_by_name(tu.cursor, "newZombie")
        if newZombie_cursor:
            print(f"Found newZombie cursor: {newZombie_cursor.kind}")
            print(f"Type: {newZombie_cursor.type.spelling}")
        else:
            print("Could not find newZombie cursor anywhere in AST!")
        
    finally:
        import shutil
        shutil.rmtree(temp_dir)

# Example usage:
main_cpp = '''
#include "Zombie.h"

int main ()
{
    Zombie *AllocatedZombie;
    AllocatedZombie = newZombie("heapZombie");
    newZombie("ss");
    AllocatedZombie->announce();
    randomChump("stackZombie");
    deleteZombie(AllocatedZombie);
    return 0;
}
'''

zombie_h = '''
#pragma once

#include <iostream>

class Zombie {
private:
    std::string _name;
public:
    Zombie(std::string name);
    ~Zombie();
    void announce();
};

Zombie* newZombie( std::string name );
void    randomChump( std::string name );
void    deleteZombie(Zombie *zombie);
'''

# Run the deep debug
deep_debug_clang(main_cpp, zombie_h, "")