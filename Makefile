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

$(GRAPHDESC):
	python main.py $(GRAPHDESC) 640 480 26 32 40 0.5

$(SPANDESC): $(GRAPHDESC)

%.png: %.gv
	$(RENDER) $< > $@
