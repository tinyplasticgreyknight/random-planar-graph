from pyhull.delaunay import DelaunayTri
from graphviz.dot import Graph
from random import randint

def generate_node(width, height):
	return [randint(0, width-1), randint(0, height-1)]

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
	triangles = DelaunayTri(nodes)
	edges = set()
	for tri in triangles.vertices:
		for edge in triangle_edges(tri):
			edges.add((edge[0], edge[1]))
	return list(edges)

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
		#f.write("\tgraph [size=\"%.4f,%.4f\"];\n" % (width*PIXELS, height*PIXELS))
		for i in range(len(nodes)):
			node = nodes[i]
			f.write("\t%s [" % node_id(i))
			f.write("pos=\"%d,%d\"" % (node[0], node[1]))
			#f.write(", pin=true")
			#f.write(", shape=circle")
			#f.write(", width=%.4f, height=%.4f, fixedsize=true" % (size*PIXELS, size*PIXELS))
			f.write("];\n")
		for edge in edges:
			id0 = node_id(edge[0])
			id1 = node_id(edge[1])
			f.write("\t%s -- %s;\n" % (id0, id1))
		f.write("}\n")

def main(filename, width=320, height=240, num_nodes=10, exclusion_radius=2):
	width = int(width)
	height = int(height)
	num_nodes = int(num_nodes)
	exclusion_radius = int(exclusion_radius)

	nodes = generate_nodes(num_nodes, width, height, exclusion_radius)
	edges = triangulate(nodes)

	for i in range(len(nodes)):
		print node_id(i) + ": " + str(nodes[i])
	print edges
	write_graph(nodes, edges, width, height, 35, filename)

if __name__=='__main__':
	import sys
	main(*(sys.argv[1:]))
