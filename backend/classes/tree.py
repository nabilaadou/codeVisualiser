class tree:
	def __init__(self):
		self.programStructure = {}

	def findNode(self, node: dict, wantedKey: str):
		for key, value in node.items():
			if key == wantedKey:
				return value
			elif isinstance(value, dict):
				found = self.findNode(value, wantedKey)
				if found is not None:
					return found
		return None

	def	addNode(self, fName : str, fCalledInMainF : dict):
		# check if one of the values already exist as key to move its value under this key too
		for key in list(fCalledInMainF.keys()):
			node = self.findNode(self.programStructure, key)
			if node is not None:
				fCalledInMainF[key] = node
		# check if functionName as a key exist already
		node = self.findNode(self.programStructure, fName)
		if node is None:
			self.programStructure[fName] = fCalledInMainF # if the key doesn't exist i ll simply insert a node in the first layer of the tree
		else:
			node.update(fCalledInMainF) # if the key already exist then i ll just update the existing node with the new values;
	
	def clean(self):
		for key in list(self.programStructure.keys()):
			if key != "main":
				del self.programStructure[key]

	def display(self, node=None, indent=0):
		if node is None:
			node = self.programStructure
		for key, value in node.items():
			print("  " * indent + key)
			if isinstance(value, dict):
				self.display(value, indent + 1)






'''
	okeeeeeeeeey lets build this tree

	key: function name | value: dic of function called inside the function

	when doing this operation we ll have to do some checks
		- checking if the key is
			- if it doesn't exist then i ll normal just insert in the dict first layer
			- if it already exist somewhere

'''