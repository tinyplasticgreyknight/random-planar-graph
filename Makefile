GRAPHDESC=graph.gv
SPANDESC=span.gv
GRAPHIMG=graph.png
SPANIMG=span.png
RENDER=neato -Tpng -n1 -Nshape=circle

all: $(GRAPHIMG) $(SPANIMG)

clean:
	-rm $(GRAPHIMG)
	-rm $(SPANIMG)
	-rm $(GRAPHDESC)
	-rm $(SPANDESC)

spotless: clean
	-rm *~
	-rm *.pyc
	-rm *.png
	-rm *.gv

$(GRAPHDESC):
	python graphgen.py $(GRAPHDESC) --width 640 --height 480 --nodes 26 --debug-span $(SPANDESC)

$(SPANDESC): $(GRAPHDESC)

%.png: %.gv
	$(RENDER) $< > $@
