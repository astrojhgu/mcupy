#!/usr/bin/env python

import sys
from mcupy.graph import *
from mcupy.nodes import *
try:
	import pydot
except(ImportError):
	import pydot_ng as pydot

g=Graph()
A=FixedUniformNode(0.001,1-1e-5).withTag("A")
B=FixedUniformNode(0.001,1-1e-5).withTag("B")
mu=FixedUniformNode(.001,100-1e-5).withTag("mu")
sigma=FixedUniformNode(.001,100-1e-5).withTag("sigma")
for l in open('eff.txt'):
	e1,nrec1,ninj1=l.split()
	e1=float(e1)
	nrec1=float(nrec1)
	ninj1=float(ninj1)
	E=C_(e1).inGroup("E")
	ninj=C_(ninj1).inGroup("ninj")
	eff=((B-A)*PhiNode((E-mu)/sigma)+A).inGroup("eff")
	nrec=BinNode(eff,ninj).withObservedValue(nrec1).inGroup("nrec")
	g.addNode(nrec)
        
ma=g.getMonitor(A)
mb=g.getMonitor(B)

dot=pydot.Dot()
for i in g.dumpTopology():
	dot.add_edge(pydot.Edge(pydot.Node(i[1]),pydot.Node(i[0])))

dot.write("a.dot")

	
for i in range(0,30000):
	g.sample()
	print(ma.get(),mb.get())
