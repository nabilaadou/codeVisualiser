import astroid.nodes
import jedi # amma use it to resolve imported function that can't be resolved with astroid
from cppSourceFilesParser import mapifyList
import astroid
import os
import tempfile
import shutil

def	getCallExprs(callExprs : list, module) -> None:
    for node in module.get_children():
        '''
			use infer() to find the node of the actual function call
            if infer can't resolve the function then use jedi to reolve it
        '''
        if isinstance(node, astroid.nodes.Call):
            callExprs.append(node.func.as_string())
        getCallExprs(callExprs, node)

def	getFunctionCalls(module) -> dict:
    tree = {}
    for node in module.get_children():
        if isinstance(node, astroid.nodes.FunctionDef):
            fElement = {}
            fArgs = '(' + ', '.join(node.argnames()) + ')'
            fName = node.name + fArgs
            fType = node.display_type()

            fElement['args'] = fArgs
            fElement['name'] = fName
            fElement['type'] = fType
            fElement['parentClass'] = '' # empty for now untill i figure out how to get the p class
            fElement['callExprs'] = []
            fElement['children'] = []
            fElement['childNode'] = node
            tree[fName] = fElement
            
        getFunctionCalls(node)
    return tree

def structreInfosTreeLike(info : dict, root : str) -> None:
    for child in info[root]['callExprs']:
        if child in list(info.keys()):
            structreInfosTreeLike(info, child)
            info[root]['children'].append(info[child])

def	pyParseFiles(files : list) -> dict:
    sourceFiles = mapifyList(files)
    graphCallTree = {}

    try:
        tmpDir = tempfile.mkdtemp() #creating a tmp dir

        #opening all files in the tmp dir we created before
        filesPath = []
        for key, value in sourceFiles.items():
            suffix = os.path.splitext(key);
            if suffix[1] == '.py': #opening files with these extensions
                path = os.path.join(tmpDir, key)
                print(path)
                filesPath.append(path) #storing the files path to parse them later
                with open(path, 'w') as fd:
                        fd.write(value)
        print('hereee')
        project = astroid.MANAGER.project_from_files(filesPath)
        for key in list(sourceFiles.keys()):
            fileName = os.path.splitext(key)[0]
            module = project.get_module(fileName)
            filesInfo = getFunctionCalls(module)
            graphCallTree.update(filesInfo)
    except:
        print('Error: operation of writing content to a tmp files failed')
    finally:
        # Clean up the temporary directory
        shutil.rmtree(tmpDir)

    for key in list(graphCallTree.keys()):
        getCallExprs(graphCallTree[key]['callExprs'], graphCallTree[key]['childNode'])
        del graphCallTree[key]['childNode'] # removin this key as it is useless now

    for keys in list(graphCallTree.keys()):
        structreInfosTreeLike(graphCallTree, key)

    for key in list(graphCallTree.keys()):
        print(f"function =======>>>>{key}\nchilds:")
        print(f'{graphCallTree[key]['children']}\ncallExprs:')
        print(f'{graphCallTree[key]['callExprs']}')
