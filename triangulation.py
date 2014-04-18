def triangulate(nodes, randstream, mode='conform'):
	if mode=='pyhull':
		tris = triangulate_pyhull(nodes, randstream)
	elif mode=='triangle':
		tris = triangulate_triangle(nodes, randstream)
	elif mode=='conform':
		tris = triangulate_triangle_conform(nodes, randstream)
	else:
		raise ArgumentException("invalid mode")
	return canonical_order(tris)

def sorter(tri1, tri2):
	s1 = sorted(tri1)
	s2 = sorted(tri2)
	if s1 < s2:
		return -1
	elif s1 > s2:
		return 1
	else:
		return 0

def canonical_order(tris):
	return sorted(list(tris), cmp=sorter)

def triangulate_pyhull(nodes, randstream):
	import pyhull.delaunay
	data = pyhull.delaunay.DelaunayTri(nodes)
	return data.vertices

def triangulate_triangle(nodes, randstream):
	import triangle
	data = triangle.delaunay(nodes)
	return data

def triangulate_triangle_conform(nodes, randstream):
	import triangle
	data = triangle.triangulate({"vertices":nodes}, "DS0F")
	tris = data["triangles"]
	return tris
