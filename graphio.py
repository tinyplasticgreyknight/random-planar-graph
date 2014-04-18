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

def write_edge(stream, edge, index):
	id0 = node_id(edge[0])
	id1 = node_id(edge[1])
	stream.write("\t%s -- %s;\n" % (id0, id1))

def write_node(stream, node, index):
	stream.write("\t%s [" % node_id(index))
	stream.write("pos=\"%d,%d\"" % (node[0], node[1]))
	stream.write("];\n")

def write_graph(stream, nodes, edges):
	stream.write("graph {\n")
	for i in range(len(nodes)):
		write_node(stream, nodes[i], i)
	for i in range(len(edges)):
		write_edge(stream, edges[i], i)
	stream.write("}\n")

def write(filename, nodes, edges, seed):
	with open(filename, 'w') as f:
		f.write("// random seed %d\n" % seed)
		write_graph(f, nodes, edges)
