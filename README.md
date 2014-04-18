Random Planar Graphs
====================
This script creates random planar graphs, suitable as input to graphviz `neato`.

Invocation
----------
The simplest invocation is:
> `python GenerateGraph.py outputgraph.gv`

which you could then render with:
> `neato -Tpng outputgraph.gv > outputgraph.png`

Note that sometimes neato decides to pick a nonplanar embedding.
Try giving `neato` the `-n1` argument to use the node coordinates specified by this script, which are always planar but might not look as pretty.
If you do, you might also want to specify `-Nshape=circle` to tell `neato` to use circular nodes.  The default coordinates assume nodes are roughly circular.

Options
-------
You can read the help text for details on options:
> `python GenerateGraph.py --help`

The most common options are:

* `--width SIZE`: Width of the field on which to place points. `neato` might choose a different width for the output image.
* `--height SIZE`: Height of the field on which to place points. As above, `neato` might choose a different size.
* `--nodes NUM`: Number of nodes to place.
* `--edges NUM`: Number of edges to use for connections. Double edges aren't counted.
* `--radius SIZE`: Nodes will not be placed within this distance of each other. Default 40.
* `--double CHANCE`: Probability of an edge being doubled. Ranges from 0.00 to 1.00. Default 0.10.

License
-------
Copyright (C) 2014 GreyKnight

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies of the Software, its documentation and marketing & publicity
materials, and acknowledgment shall be given in the documentation, materials
and software packages that this Software was used.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
