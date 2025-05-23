from pySourceFilesParser import pyParseFiles
import json

def pyGenerateTree(files : list):
    tree = pyParseFiles(files)
    # for key in list(tree.keys()):
    #     print(f"{key} -> {tree[key]}")
    # response = json.dumps(tree)
    # responseJson = json.loads(response)
    # return responseJson
    return {}
