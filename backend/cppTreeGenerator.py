from cppSourceFilesParser import cppParseFiles
import json

def cppGenerateTree(files : list):
    tree = cppParseFiles(files)
    for key in list(tree.keys()):
        print(f"{key} -> {tree[key]}")
    # response = json.dumps(tree)
    # responseJson = json.loads(response)
    # return responseJson
    return {}
