import math
class Tree(list):
	def insert(self, node):
		self.append(node)
		return self

	def each(self, block=None):
		if block is None:
			return iter(self)
		for i, node in enumerate(self):
			self[i] = block(node)
		return self

	def each_with_level(self, block=None):
		if block is None:
			return iter(self)
		for i, node in enumerate(self):
			depth = int(math.log(i+1,2))
			self[i] = block(node,depth)
		return self