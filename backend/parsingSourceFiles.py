from clang import cindex
from clang.cindex import CursorKind
import os
import tempfile
import shutil

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

def getFunctionArgs(cursor) ->list:
    fArg = []

    for subFunctionChild in cursor.get_children():
        if subFunctionChild.kind == CursorKind.PARM_DECL:
            fArg.append((subFunctionChild.type.spelling, subFunctionChild.spelling))
    return fArg

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
        if subFunctionChild.kind == CursorKind.CALL_EXPR: #CALL-EXPR refers to a node that is being called it can be a function method etc
            if subFunctionChild.spelling != '':
                subCalls.append(subFunctionChild.spelling)
        else:
            tmpSubCalls = getFunctionCalls(subFunctionChild, fileName)
            if tmpSubCalls != []:
                subCalls.extend(tmpSubCalls)
    return subCalls

def extractFunctions(cursor, filename : str) -> dict:
    functionsTree = {}
    for child in cursor.get_children():
        if isUserFunction(child, filename):
            fElement= {}
            callExprs = getFunctionCalls(child, filename)
            fArgs = getFunctionArgs(child)
            fType = getFunctionType(child.kind)
            parentClass = ''
            if fType in {'method', 'constructer', 'destructer', 'operator'}:
                parentClass = child.semantic_parent.spelling

            fElement['args'] = fArgs
            fElement['type'] = fType
            fElement['parentClass'] = parentClass
            fElement['callExprs'] = callExprs
            functionsTree[child.spelling] = fElement

        extractFunctions(child, filename)
    return functionsTree


def generatingCleanedAST(files : list) -> dict:
    #create a map out of this list(key->file name, value->file content)
    mp_files = mapifyList(files)
    index = cindex.Index.create()
    cleanedAST = {}

    try:
        tmpDir = tempfile.mkdtemp() #creating a tmp dir
        #opening all files in the tmp dir we created before
        filesPath = []
        for key, value in mp_files.items():
            path = os.path.join(tmpDir, key)
            filesPath.append(path)
            with open(path, 'w') as f:
                    f.write(value)

        for name in filesPath:
            #extracting the suffix of the file name to check what type it is
            pos = name.rfind('.')
            suffix = ''
            if pos != -1:
                suffix = name[pos+1:]

            if suffix == 'cpp':
                #creating a tu to accessing the ast vie the cursor variable
                translationUnit = index.parse(
                    path=name,
                    args= ["-std=c++17"],
                    options= 0
                )

                filesCleanedAST = extractFunctions(translationUnit.cursor, name)
                cleanedAST.update(filesCleanedAST)
    except:
        print('Error: operation of writing content to a tmp directory failed')
    finally:
        # Clean up the temporary directory
        shutil.rmtree(tmpDir)
    
	#removing callExprs that aren't defined by the user
    for key in list(cleanedAST.keys()):
        for callExpr in cleanedAST[key]['callExprs']:
            if callExpr not in list(cleanedAST.keys()):
                cleanedAST[key]['callExprs'].remove(callExpr)

    return cleanedAST