def triangulate(nodes):
	import pyhull.delaunay
	return pyhull.delaunay.DelaunayTri(nodes)
