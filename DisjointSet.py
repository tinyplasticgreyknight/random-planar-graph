
class DisjointSet(dict):
	def add(self, item):
		self[item] = item

	def find(self, needle):
		parent = self[needle]
		while self[parent] != parent:
			parent = self[parent]
		self[needle] = parent
		return parent

	def union(self, item1, item2):
		self[self.find(item2)] = self[item1]
