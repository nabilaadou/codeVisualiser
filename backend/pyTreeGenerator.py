from pySourceFilesParser import pyParser
from cppSourceFilesParser import mapifyList
import json

def pyGenerateTree(files : list):
    sourceFiles = mapifyList(files)
    treeObj = pyParser(sourceFiles)
    response = json.dumps(treeObj.tree)
    responseJson = json.loads(response)
    return responseJson
    return {}
