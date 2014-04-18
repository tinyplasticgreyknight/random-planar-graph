from DisjointSet import *
import triangulation

def generate_node(width, height, randstream):
	return (randstream.randint(0, width-1), randstream.randint(0, height-1))

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

def generate_nodes(n, width, height, exclusion_dist, randstream):
	nodes = []
	while len(nodes) < n:
		proposed_node = generate_node(width, height, randstream)
		if test_node_placement(proposed_node, nodes, exclusion_dist):
			nodes.append(proposed_node)
	return nodes

def triangle_edges(tri):
	a, b, c = tri
	ab = [min(a, b), max(a, b)]
	bc = [min(b, c), max(b, c)]
	ac = [min(a, c), max(a, c)]
	return [ab, bc, ac]

def triangulate(nodes, randstream, tri_mode):
	"""Return the list of edges which achieves a Delaunay triangulation of the specified nodes."""
	triangles = triangulation.triangulate(nodes, randstream, tri_mode)
	edges = set()
	for tri in triangles:
		for edge in triangle_edges(tri):
			edges.add((edge[0], edge[1]))
	return list(edges)

def spanning_tree(nodes, edges, randstream):
	"""Given a list of edges, calculate a minimal spanning tree out of them."""
	num_nodes = len(nodes)
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

def choice(fromset, stream):
	return stream.choice(list(fromset))

def chance(probability, stream):
	return (stream.random() < probability)

def extend_edges(starting_edges, target_size, selections, hair_adjustment, randstream):
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
		edge = choice(selections, randstream)
		if (edge in bad_hair_edges) and chance(hair_adjustment, randstream):
			edge = choice(good_hair_edges, randstream)
			good_hair_edges.discard(edge)
		else:
			selections.discard(edge)
		extended.add(edge)
	return list(extended)

def double_up_edges(edges, probability, randstream):
	double_edges = []
	for edge in edges:
		if chance(probability, randstream):
			double_edges.append(edge)
	return (edges + double_edges)

