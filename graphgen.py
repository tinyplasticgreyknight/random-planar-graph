#!/usr/bin/env python
from random import Random
from DisjointSet import *
import triangulation

def generate_node(width, height, randstream):
	return [randstream.randint(0, width-1), randstream.randint(0, height-1)]

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

def make_streams(seed):
	# since triangulator is specialised and might need its own random stream
	# may as well stream the other steps too!
	streams = {}
	i=0
	for k in ['gen', 'tri', 'span', 'ext', 'double']:
		streams[k] = Random(seed+i)
		i += 1
	return streams

def double_up_edges(edges, probability, randstream):
	double_edges = []
	for edge in edges:
		if chance(probability, randstream):
			double_edges.append(edge)
	return (edges + double_edges)

def main(opts):
	num_nodes = opts.nodes
	num_edges = opts.edges
	streams = make_streams(opts.seed)

	# first generate some points in the plane, according to our constraints
	nodes = generate_nodes(num_nodes, opts.width, opts.height, opts.radius, streams['gen'])
	num_nodes = len(nodes)
	# find a delaunay triangulation, so we have a list of edges that will give planar graphs
	tri_edges = triangulate(nodes, streams['tri'], opts.debug_trimode)
	# compute a spanning tree to ensure the graph is joined
	span_edges = spanning_tree(nodes, tri_edges, streams['span'])
	# extend the tree with some more edges to achieve our target num_edges
	# pick the extra ones from tri_edges to preserve planarity
	ext_edges = extend_edges(span_edges, num_edges, tri_edges, opts.hair, streams['ext'])
	# randomly double some edges
	doubled_edges = double_up_edges(ext_edges, opts.double, streams['double'])

	# write out to file
	write_graph(nodes, doubled_edges, opts.width, opts.height, opts.seed, opts.filename)
	# write out debug traces if specified
	if opts.debug_tris is not None:
		write_graph(nodes, tri_edges,     opts.width, opts.height, opts.seed, opts.debug_tris)
	if opts.debug_span is not None:
		write_graph(nodes, span_edges,    opts.width, opts.height, opts.seed, opts.debug_span)

if __name__=='__main__':
	import argparse
	import time, os
	defaults = {
		"width": 320,
		"height": 240,
		"nodes": 10,
		"edges": None,
		"radius": 40,
		"double": 0.1,
		"hair": 0.0,
		"seed": int(time.time()) | os.getpid(),
		"debug_trimode": 'conform',
		"debug_tris": None,
		"debug_span": None,
	}

	def posint(string):
		value = int(string)
		if value <= 0:
			raise argparse.ArgumentTypeError("positive value expected")
		return value

	def nonnegative_int(string):
		value = int(string)
		if value < 0:
			raise argparse.ArgumentTypeError("non-negative value expected")
		return value

	def probability(string):
		value = float(string)
		if value < 0.0 or value > 1.0:
			raise argparse.ArgumentTypeError("value in the range [0.0, 1.0] expected")
		return value

	parser = argparse.ArgumentParser(
		description="Create random planar graphs, suitable as input to graphviz neato.",
		epilog="Note that sometimes neato decides to pick a nonplanar embedding.  Try giving neato the -n1 argument to use the node coordinates specified by this script, which are always planar but might not look as pretty."
	)
	parser.add_argument("--width", metavar="SIZE", type=posint, required=False, help="Width of the field on which to place points.  neato might choose a different width for the output image.")
	parser.add_argument("--height", metavar="SIZE", type=posint, required=False, help="Height of the field on which to place points.  As above, neato might choose a different size.")
	parser.add_argument("--nodes", metavar="NUM", type=posint, required=False, help="Number of nodes to place.")
	parser.add_argument("--edges", metavar="NUM", type=posint, required=False, help="Number of edges to use for connections.  Double edges aren't counted.")
	parser.add_argument("--radius", metavar="SIZE", type=nonnegative_int, required=False, help="Nodes will not be placed within this distance of each other.  Default %d." % defaults["radius"])
	parser.add_argument("--double", metavar="CHANCE", type=probability, required=False, help="Probability of an edge being doubled.  Ranges from 0.00 to 1.00.  Default %.2f." % defaults["double"])
	parser.add_argument("--hair", metavar="AMOUNT", type=probability, required=False, help="Adjustment factor to favour dead-end nodes.  Ranges from 0.00 (least hairy) to 1.00 (most hairy).  Some dead-ends may exist even with a low hair factor.  Default %.2f." % defaults["hair"])
	parser.add_argument("--seed", metavar="NUMBER", type=int, required=False, help="Seed for the random number generator.  You can check the output file to see what seed was used.")
	parser.add_argument("--debug-trimode", type=str, choices=['pyhull', 'triangle', 'conform'], required=False, help="Triangulation mode to generate the initial triangular graph.  Default is conform.")
	parser.add_argument("--debug-tris", metavar="FILENAME", type=str, required=False, help="If a filename is specified here, the initial triangular graph will be saved as a graph for inspection.")
	parser.add_argument("--debug-span", metavar="FILENAME", type=str, required=False, help="If a filename is specified here, the spanning tree will be saved as a graph for inspection.")
	parser.add_argument("filename", type=str, help="The graphviz output will be written to this file.")
	parser.set_defaults(**defaults)
	options = parser.parse_args()

	if options.edges is None:
		options.edges = int(options.nodes * 1.25)
	options.edges = max(options.edges, options.nodes-1) # necessary to avoid a disjoint graph
	main(options)
