from pyhull import qdelaunay
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

print generate_nodes(20, 10, 10, 2)
