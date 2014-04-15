from pyhull.delaunay import DelaunayTri
from graphviz.dot import Graph
import random
from DisjointSet import DisjointSet

def generate_node(width, height):
	return [random.randint(0, width-1), random.randint(0, height-1)]

def distance2(node0, node1):
	dx = node1[0] - node0[0]
	dy = node1[1] - node0[1]
	return (dx**2 + dy**2)

def test_node_placement(proposed_node, nodes, exclusion_dist):
	edist2 = exclusion_dist**2
	for node in nodes:
		if distance2(node, proposed_node) < edist2:
			return False
	return True

def generate_nodes(n, width, height, exclusion_dist=1):
	nodes = []
	while len(nodes) < n:
		proposed_node = generate_node(width, height)
		if test_node_placement(proposed_node, nodes, exclusion_dist):
			nodes.append(proposed_node)
	return nodes

def triangle_edges(tri):
	a, b, c = tri
	ab = [min(a, b), max(a, b)]
	bc = [min(b, c), max(b, c)]
	ac = [min(a, c), max(a, c)]
	return [ab, bc, ac]

def triangulate(nodes):
	"""Return the list of edges which achieves a Delaunay triangulation of the specified nodes."""
	triangles = DelaunayTri(nodes)
	edges = set()
	for tri in triangles.vertices:
		for edge in triangle_edges(tri):
			edges.add((edge[0], edge[1]))
	return list(edges)

def kruskal(num_nodes, edges):
	"""Given a list of edges, calculate a minimal spanning tree out of them."""
	tree = []
	partitions = DisjointSet()
	for i in range(num_nodes):
		# create a disjoint set where each node is a singleton partition
		partitions.add(i)
	for edge in edges:
		a, b = edge
		if partitions.find(a) != partitions.find(b):
			# partitions were unconnected: bridge them together
			tree.append(edge)
			partitions.union(a, b)
		if len(tree) == num_nodes-1:
			# minimal spanning tree acquired
			break
	return tree

def extend_edges(starting_edges, target_size, selection_set):
	"""Returns a version of starting_edges with target_size unique elements.  Extra items are drawn from selection_set."""
	selections = set(selection_set)
	for edge in starting_edges:
		selections.discard(edge)
	if len(starting_edges) + len(selection_set) < target_size:
		raise ValueError("not enough unique items in selection_set")
	extended = set(starting_edges)
	selections = list(selections)
	while len(extended) < target_size:
		edge_i = random.choice(range(len(selections)))
		edge = selections.pop(edge_i)
		extended.add(edge)
	return list(extended)

ORD_A = ord('A')
def node_id_char(i):
	return chr(ORD_A + i)

def node_id(i):
	ident = ""
	while i > 0:
		ident += node_id_char(i % 26)
		i = int(i/26)
	if ident == "":
		ident = "A"
	return ident

def write_graph(nodes, edges, width, height, size, filename):
	PIXELS = 1.0/72
	with open(filename, 'w') as f:
		f.write("graph {\n")
		for i in range(len(nodes)):
			node = nodes[i]
			f.write("\t%s [" % node_id(i))
			f.write("pos=\"%d,%d\"" % (node[0], node[1]))
			f.write("];\n")
		for edge in edges:
			id0 = node_id(edge[0])
			id1 = node_id(edge[1])
			f.write("\t%s -- %s;\n" % (id0, id1))
		f.write("}\n")



def main(filename, width=320, height=240, num_nodes=10, num_edges=15, exclusion_radius=32):
	width = int(width)
	height = int(height)
	num_nodes = int(num_nodes)
	num_edges = int(num_edges)
	exclusion_radius = int(exclusion_radius)

	nodes = generate_nodes(num_nodes, width, height, exclusion_radius)
	tedges = triangulate(nodes)
	kedges = kruskal(len(nodes), tedges)
	xedges = extend_edges(kedges, num_edges, tedges)
	edges = xedges

	write_graph(nodes, edges, width, height, 35, filename)

if __name__=='__main__':
	import sys
	main(*(sys.argv[1:]))
