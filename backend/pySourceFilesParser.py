import astroid
import ast
import os

class	pyParser:
	def	__init__(self, sourceFiles : dict):
		self.modules = {}
		self.allFuncDefs = {}
		self.tree = {
			'name': 'pyTreeGenerator.py',
			'children': []
			}

		for key, value in sourceFiles.items():
			suffix = os.path.splitext(key)[1]
			if suffix == '.py':
				self.modules[key] = astroid.parse(value)
		startingNodes = self.findStarterFunction('pyTreeGenerator.py')
		self.getAllFunctionDefs()
		self.structerTree(self.tree['children'], startingNodes)
		print(self.tree)

	def	findStarterFunction(self, executedFile : str) -> list:
		'''
			first amma look for a main() if it exists if not 
			i ll start looking for all global functions and those gonna be the start of my script
		'''
		startingNodes = []
		mainBloc = self.findMain(self.modules[executedFile])
		globalFuncs = []
		if mainBloc == None:
			globalFuncs = self.findAllGlobalFunctions(self.modules[executedFile])
			if globalFuncs == []:
				raise RuntimeError('no existing starting function')
			startingNodes = globalFuncs
		else:
			for node in mainBloc.nodes_of_class(astroid.Call):
				startingNodes.append(node.func.name)
		return startingNodes


	def isMain(self, node):
		"""Check if a node represents __name__ == '__main__' comparison"""
		if not isinstance(node, astroid.Compare):
			return False
		if not (isinstance(node.left, astroid.Name) and node.left.name == '__name__'):
			return False
		if len(node.ops) != 1:
			return False
		op, comparator = node.ops[0]
		if op != '==':
			return False
		if isinstance(comparator, astroid.Const):
			return comparator.value == '__main__'
            
		return False

	def	findMain(self, module):
		for node in module.nodes_of_class(astroid.If):
			if self.isMain(node.test):
				return node
			# Also checking for the reverse order 'main' == __name__
			if isinstance(node.test, astroid.Compare):
				test = node.test #the test variable is the node of whats being evaluated (tested)
				if (isinstance(test.left, astroid.Const) and
					test.left.value == '__main__' and
					len(test.ops) == 1):

					op, comparator = test.ops[0]
					if (isinstance(op, ast.Eq) and
				    	isinstance(comparator, astroid.Name) and
				    	comparator.name == '__name__'):
						return node
		return None
	
	def analyze_call_context(self, node) -> bool:
		# Get the scope of the call
		scope = node.scope()
		if isinstance(scope, astroid.Module):
			return True
		else:
			return False

	def	findAllGlobalFunctions(self, module):
		globalFuncs = []
		for node in module.nodes_of_class(astroid.Call):
			if self.analyze_call_context(node):
				globalFuncs.append(node)
		return globalFuncs
		
	def	getAllFunctionDefs(self):
		for module in list(self.modules.values()):
			for node in module.nodes_of_class(astroid.FunctionDef):
				self.allFuncDefs[node.name] = node

	def	structerTree(self, children : list, callExprs : list):
		'''
			still need to handle recursive calls and display them some how in the tree
		'''
		for callName in callExprs:
			if callName in list(self.allFuncDefs.keys()):
				funcCallExprs = []
				child = {}

				child['name'] = callName
				child['children'] = []
				for node in self.allFuncDefs[callName].nodes_of_class(astroid.Call):
					if hasattr(node.func, 'name') and node.func.name != callName:
						funcCallExprs.append(node.func.name)
				self.structerTree(child['children'], funcCallExprs)
				children.append(child)