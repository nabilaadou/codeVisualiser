from clang import cindex
from clang.cindex import CursorKind
from classes.tree import tree
import os
import tempfile
import shutil

index = cindex.Index.create()

# def extract_user_functions(cursor, fileName) -> dict:
#     elements = {}

#     for child in cursor.get_children():
#         if is_user_function(child, fileName):
#             calls = get_function_calls(child, fileName)
#             elementsValue = {}

#             for call in calls:
#                 elementsValue[call] = {}
#             elements[child.spelling] = elementsValue
#         extract_user_functions(child, fileName)
#     return elements;

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

def isUserFunction(cursor, fileName):
    return (
        cursor.kind in {
            CursorKind.FUNCTION_DECL,           # free functions
            CursorKind.CXX_METHOD,              # class methods
            CursorKind.CONSTRUCTOR,             # class constructor
            CursorKind.DESTRUCTOR,              # class destructor
        } and
        cursor.is_definition() and
        cursor.location.file and
        cursor.location.file.name == fileName
    )

def getFunctionCalls(cursor, fileName) -> list:
    subCalls = []

    for subFunctionChild in cursor.get_children():
        if subFunctionChild.kind == CursorKind.CALL_EXPR: #CALL-EXPR refers to a node that is being called it can be a function method etc
            if subFunctionChild.location.file and subFunctionChild.location.file.name == fileName:
                subCalls.append(subFunctionChild.spelling)
        else:
            subCalls.extend(getFunctionCalls(subFunctionChild, fileName))
    return subCalls

def extractFunctions(cursor, filename : str) -> dict:
    functionsTree = {}
    for child in cursor.get_children():
        if isUserFunction(child, filename):
            subFunctions = getFunctionCalls(child, filename)

            subFunctionsNode = {}
            for function in subFunctions:
                subFunctionsNode[function] = {}
            functionsTree[child.spelling] = subFunctions

        extractFunctions(child, filename)
    return functionsTree


def createDiagram(files : list) :
    programStructre = tree()

    #create a map out of this list(key->file name, value->file content)
    mp_files = mapifyList(files)
    filesPath = []
    cleanedAST = {}
    temp_dir = tempfile.mkdtemp() #creating a tmp dir

    #opening all files
    try:
        for key, value in mp_files.items():
            path = os.path.join(temp_dir, key)
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
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

    # #add nodes to tree class
    print(cleanedAST)
    # for key, value in cleanedAST.items():
    #     programStructre.addNode(key, value)
    # programStructre.display()












    # for element in files:
    #     fileName = element["fileName"]
    #     fileContent = element["content"]
    #     cppFiles[fileName] = fileContent
    #     print(fileName)
    #     translation_unit = index.parse(
    #         path=fileName,
	#         args=['-std=c++17'],
	#         unsaved_files=[(fileName, fileContent)],
	#         options=0
    #     )
    #     elements = extract_user_functions(translation_unit.cursor, fileName)
    #     for key, value in elements.items():
    #        programStructre.addNode(key, value)
    
    # programStructre.clean()
    # print('---')
    # programStructre.display()
    # print('---')
















# def addHeadersContentToSourcefiles(mp_files : dict) -> None:
#     for key, value in mp_files.items():
#         dotOccurence = key.rfind('.')
#         suffix = ""
#         if dotOccurence != -1:
#             suffix = key[dotOccurence:]
        
#         if suffix != '.cpp' and suffix != '.hpp' and suffix != '.h':
#             # remove file from dict because its not what i am planing to work with
#             del mp_files[key]
#         elif suffix == '.cpp':
#             # find included headers and add its content in the top of the file
#             getListOfUsersHeaders(value)