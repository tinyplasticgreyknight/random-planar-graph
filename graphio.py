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

ESCAPES = {'\\':'\\', '\n':'n', '\t':'t', '\r':'r', '"':'"', "'":"'", }
def escape(string):
	result = '"'
	for c in string:
		if c in ESCAPES:
			result += '\\' + ESCAPES[c]
		else:
			result += c
	return result + '"'

def write_attributes(stream, attribs_dict):
	if len(attribs_dict)==0:
		return
	stream.write(" [")
	first = True
	for key in attribs_dict:
		if not first:
			stream.write(", ")
		first = False
		value = attribs_dict[key]
		stream.write("%s=" % str(key))
		stream.write(escape(str(value)))
	stream.write("]")

def write_edge(stream, edge, index):
	attribs = {}
	if len(edge)>2:
		attribs = edge[2]

	id0 = node_id(edge[0])
	id1 = node_id(edge[1])

	stream.write("\t")
	stream.write("%s -- %s" % (id0, id1))
	write_attributes(stream, attribs)
	stream.write(";\n")

def write_node(stream, node, index):
	attribs = {}
	if len(node)>2:
		attribs = node[2]
	attribs['pos'] = "%d,%d" % (node[0], node[1])

	stream.write("\t")
	stream.write(node_id(index))
	write_attributes(stream, attribs)
	stream.write(";\n")

def write_graph_meta(stream, attribs):
	if len(attribs)==0:
		return
	stream.write("\tgraph")
	write_attributes(stream, attribs)
	stream.write(";\n")

def write_graph(stream, nodes, edges, attribs):
	stream.write("graph {\n")
	write_graph_meta(stream, attribs)
	for i in range(len(nodes)):
		write_node(stream, nodes[i], i)
	for i in range(len(edges)):
		write_edge(stream, edges[i], i)
	stream.write("}\n")

def write(filename, nodes, edges, seed, graph_attribs={}):
	with open(filename, 'w') as f:
		f.write("// random seed %d\n" % seed)
		write_graph(f, nodes, edges, graph_attribs)
