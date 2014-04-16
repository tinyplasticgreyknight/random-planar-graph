from pyhull.delaunay import DelaunayTri
from graphviz.dot import Graph
import random
import time
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

def spanning_tree(num_nodes, edges):
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

def identify_leaf_nodes(edges):
	degree = {}
	def increment(k):
		if k not in degree:
			degree[k] = 0
		degree[k] += 1
	for edge in edges:
		increment(edge[0])
		increment(edge[1])
	leaves = set()
	for k in degree:
		if degree[k]==1:
			leaves.add(k)
	return leaves

def partition_edges_by_nodes(nodes, edges):
	adjacent = set() # edges which have one of those nodes
	distant = set() # the remaining edges
	for edge in edges:
		if (edge[0] in nodes) or (edge[1] in nodes):
			adjacent.add(edge)
		else:
			distant.add(edge)
	return (adjacent, distant)

def choice(fromset):
	return random.choice(list(fromset))

def chance(probability):
	return (random.random() < probability)

def extend_edges(starting_edges, target_size, selections, hair_adjustment):
	"""
	Returns a version of starting_edges with target_size unique elements.
	Extra items are drawn from selections.
	hair_adjustment is the probability that leaf nodes will be left as they are
	"""
	selections = set(selections)
	for edge in starting_edges:
		selections.discard(edge)
	leaf_nodes = identify_leaf_nodes(starting_edges)
	# good hair: edges which don't reduce the number of leaf nodes
	# bad hair: edges which may reduce the number of leaf nodes
	bad_hair_edges, good_hair_edges = partition_edges_by_nodes(leaf_nodes, selections)
	good_hair_edges = good_hair_edges
	bad_hair_edges = bad_hair_edges
	
	if hair_adjustment >= 1.0:
		# in this case we may as well only pick from good hair in the first place
		selections = good_hair_edges
		bad_hair_edges = set()

	if len(starting_edges) + len(selections) < target_size:
		raise ValueError("not enough unique items in selections")

	extended = set(starting_edges)
	while len(extended) < target_size:
		edge = choice(selections)
		if (edge in bad_hair_edges) and chance(hair_adjustment):
			edge = choice(good_hair_edges)
			good_hair_edges.discard(edge)
		else:
			selections.discard(edge)
		extended.add(edge)
	return list(extended)

ORD_A = ord('A')
def node_id_char(i):
	return chr(ORD_A + i)

def node_id(i):
	ident = ""
	i += 1
	while i > 0:
		c = (i-1) % 26
		ident = node_id_char(c) + ident
		i = int((i-c)/26)
	return ident

def write_graph(nodes, edges, width, height, seed, filename):
	with open(filename, 'w') as f:
		f.write("// random seed %d\n" % seed)
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


def main(filename, width=320, height=240, num_nodes=10, num_edges=None, exclusion_radius=40, double_chance=0.1, hair_adjustment=0.0, seed=None):
	if seed is None:
		seed = time.time()
	seed = int(seed)
	width = int(width)
	height = int(height)
	num_nodes = int(num_nodes)
	if num_edges is None:
		num_edges = num_nodes * 1.25
	num_edges = int(num_edges)
	exclusion_radius = int(exclusion_radius)
	double_chance = float(double_chance)
	hair_adjustment = float(hair_adjustment)

	random.seed(seed)
	nodes = generate_nodes(num_nodes, width, height, exclusion_radius)
	tri_edges = triangulate(nodes)
	span_edges = spanning_tree(len(nodes), tri_edges)
	ext_edges = extend_edges(span_edges, num_edges, tri_edges, hair_adjustment)
	double_edges = []
	for edge in ext_edges:
		if chance(double_chance):
			double_edges.append(edge)
	edges = ext_edges + double_edges

	write_graph(nodes, span_edges, width, height, seed, "span.gv")
	write_graph(nodes, edges, width, height, seed, filename)

if __name__=='__main__':
	import sys
	main(*(sys.argv[1:]))
