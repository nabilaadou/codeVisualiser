from clang import cindex
from clang.cindex import CursorKind
import os
import tempfile
import shutil

potential_call_exprs = [
        CursorKind.CALL_EXPR,              # Normal case
        CursorKind.OVERLOADED_DECL_REF,    # Most common alternative
        CursorKind.DECL_REF_EXPR,          # Function pointers
        # CursorKind.UNEXPOSED_EXPR,         # Hidden calls
        CursorKind.TEMPLATE_REF,           # Template functions
        # CursorKind.CXX_UNARY_EXPR,         # Unary operators
        # CursorKind.CXX_BINARY_EXPR,        # Binary operators  
        # CursorKind.CXX_OPERATOR_CALL_EXPR, # Operator overloads
        # CursorKind.CXX_CONSTRUCT_EXPR,     # Constructors
        # CursorKind.CXX_TEMPORARY_OBJECT_EXPR, # Temporary objects
        # CursorKind.CXX_FUNCTIONAL_CAST_EXPR,  # Functional casts
        # CursorKind.CXX_MEMBER_CALL_EXPR,   # Member calls
        # CursorKind.MEMBER_REF_EXPR,        # Member references
        # CursorKind.MACRO_EXPANSION,        # Macro calls
        # CursorKind.UNEXPOSED_STMT,         # Unexposed statements
        CursorKind.LAMBDA_EXPR,            # Lambda calls
    ]

def mapifyList(files : list) -> dict:
    mp_files = {}
    for element in files:
        fileName = element["fileName"]
        fileContent = element["content"]
        mp_files[fileName] = fileContent
    return mp_files

def isUsersInclude(line : str) -> str:
    line = line.strip();
    pos = line.find("include")
    if pos != 0:
        return ''
    line = line[7:]
    line = line.strip()
    if line[0] == '"' and line[-1] == '"':
        return line.strip('"')
    return ''

def getIncludedHeaders(cppSourceCode : str) -> list:
    headers = []
    pos = cppSourceCode.find('#')
    while pos != -1:
        nlPos = cppSourceCode.find('\n', pos)
        if nlPos != -1:
            line = cppSourceCode[pos+1:nlPos]
            path = isUsersInclude(line)
            if path != '':
                headers.append(path)
        pos = cppSourceCode.find('#', pos + 1)
    return headers        

def isUserFunction(cursor, fileName : str) -> bool:
    return (
        cursor.kind in {
            CursorKind.FUNCTION_DECL,           # free functions
            CursorKind.CXX_METHOD,              # class methods
            CursorKind.CONSTRUCTOR,             # class constructor
            CursorKind.DESTRUCTOR,              # class destructor
            CursorKind.CONVERSION_FUNCTION		# class operator
        } and
        cursor.is_definition() and
        cursor.location.file and
        cursor.location.file.name == fileName
    )

    
def getFunctionArgs(cursor) ->str:
    fArg = []

    for subFunctionChild in cursor.get_children():
        if subFunctionChild.kind == CursorKind.PARM_DECL:
            fArg.append(subFunctionChild.type.spelling + ' ' + subFunctionChild.spelling)
    return '(' + ', '.join(fArg) + ')'

def getFunctionType(kind : str) -> str:
    if kind == CursorKind.FUNCTION_DECL:
        return 'function'
    elif kind == CursorKind.CXX_METHOD:
        return 'method'
    elif kind == CursorKind.CONSTRUCTOR:
        return 'constructer'
    elif kind == CursorKind.DESTRUCTOR:
        return 'destructer'
    else:
        return 'operator'

def getFunctionCalls(cursor, fileName : str) -> list:
    subCalls = []

    for subFunctionChild in cursor.get_children():
        print(f"name -> {subFunctionChild.spelling} -> kind -> {subFunctionChild.kind}")
        if subFunctionChild.kind in potential_call_exprs:
            if subFunctionChild.spelling != '':
                subCalls.append(subFunctionChild.spelling)

        tmpSubCalls = getFunctionCalls(subFunctionChild, fileName)
        if tmpSubCalls != []:
            subCalls.extend(tmpSubCalls)
    return subCalls

def extractFunctions(cursor, filename : str) -> dict:
    '''
    for child in cursor.get_children():
        for 
        cursor = child
    '''
    functionsTree = {}
    for child in cursor.get_children():
        if isUserFunction(child, filename):
            fElement= {}
            fName = child.spelling
            print(f'function  => {child.spelling}')
            callExprs = getFunctionCalls(child, filename)
            fArgs = getFunctionArgs(child)
            fType = getFunctionType(child.kind)
            parentClass = ''
            if fType in {'method', 'constructer', 'destructer', 'operator'}:
                parentClass = child.semantic_parent.spelling

            fElement['name'] = fName
            fElement['args'] = fArgs
            fElement['type'] = fType
            fElement['parentClass'] = parentClass
            fElement['callExprs'] = callExprs
            fElement['children'] = []
            functionsTree[child.spelling+fArgs] = fElement

        extractFunctions(child, filename)
    return functionsTree

def structreInfosTreeLike(info : dict, root : str) -> None:
    for child in info[root]['callExprs']:
        if child in list(info.keys()):
            structreInfosTreeLike(info, child)
            info[root]['children'].append(info[child])


def removeExtraNodes(info : dict) -> None:
    for key in list(info.keys()):
        if key != 'main':
            del info[key]

def generatingCleanedAST(files : list) -> dict:
    #create a map out of this list(key->file name, value->file content)
    mp_files = mapifyList(files)
    #creating an instance from the libclang so we can connect with the api => check if this is what is really happening
    index = cindex.Index.create()
    filesFunctionsInfo = {}

    try:
        tmpDir = tempfile.mkdtemp() #creating a tmp dir


        #opening all files in the tmp dir we created before
        filesPath = []
        for key, value in mp_files.items():
            suffix = os.path.splitext(key);
            if suffix[1] in {'.cpp', '.hpp', '.h', '.tpp'}: #opening files with these extensions
                path = os.path.join(tmpDir, key)
                filesPath.append(path) #storing the files path to parse them later
                with open(path, 'w') as f:
                        f.write(value)

        for name in filesPath:
            #extracting the suffix of the file name to check what type it is
            suffix = os.path.splitext(name)[1]

            if suffix == '.cpp':
                #creating a tu to accessing the ast vie the cursor variable
                translationUnit = index.parse(
                    path=name,
                    args= ["-std=c++17", "-I."],
                    options=0
                )
                currentFileInfo = extractFunctions(translationUnit.cursor, name)
                filesFunctionsInfo.update(currentFileInfo)
    except:
        print('Error: operation of writing content to a tmp files failed')
    finally:
        # Clean up the temporary directory
        shutil.rmtree(tmpDir)
    
	#removing callExprs that aren't defined by the user
    for key in list(filesFunctionsInfo.keys()):
        for callExpr in filesFunctionsInfo[key]['callExprs']:
            if callExpr not in list(filesFunctionsInfo.keys()):
                filesFunctionsInfo[key]['callExprs'].remove(callExpr)
    
    for key in list(filesFunctionsInfo.keys()):
        print(f"{key} -> {filesFunctionsInfo[key]}")

    if 'main' in list(filesFunctionsInfo.keys()):
        #structring the data as a tree with the main() as the root
        structreInfosTreeLike(filesFunctionsInfo, 'main')
        #removin nodes in the first layer leaving just main() as the root
        removeExtraNodes(filesFunctionsInfo)
        return filesFunctionsInfo['main']
    return {}