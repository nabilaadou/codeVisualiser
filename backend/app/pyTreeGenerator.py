from pySourceFilesParser import pyParser
import json

def pyGenerateTree(data : dict):
    treeObj = pyParser(data['folder'], data['file'])
    response = json.dumps(treeObj.tree)
    responseJson = json.loads(response)
    return responseJson
