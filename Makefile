GRAPHDESC=graph.gv
GRAPHIMG=graph.png
RENDER=neato -Tpng -n1 -Nshape=circle

all: $(GRAPHIMG)

clean:
	-rm $(GRAPHIMG)
	-rm $(GRAPHDESC)

spotless: clean
	-rm *~

$(GRAPHDESC):
	python main.py $(GRAPHDESC) 800 600 10 15

$(GRAPHIMG): $(GRAPHDESC)
	$(RENDER) $(GRAPHDESC) > $(GRAPHIMG)
