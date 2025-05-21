from parsingSourceFiles import generatingCleanedAST
import json

def constructResponse(files : list):
    tree = generatingCleanedAST(files)
    response = json.dumps(tree)
    responseJson = json.loads(response)
    print(responseJson)
    return responseJson