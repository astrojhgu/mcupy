#!/usr/bin/env python

import sys
from mcupy.graph import *
from mcupy.nodes import *
import mcupy.core
try:
	import pydot
except(ImportError):
	import pydot_ng as pydot

g=Graph()
A=FixedUniformNode(0.001,1-1e-5).withTag("A")
B=FixedUniformNode(0.001,1-1e-5).withTag("B")
mu=FixedUniformNode(.001,100-1e-5).withTag("mu")
sigma=FixedUniformNode(.001,100-1e-5).withTag("sigma")
n=0
for l in open('eff.txt'):
	e1,nrec1,ninj1=l.split()
	e1=float(e1)
	nrec1=float(nrec1)
	ninj1=float(ninj1)
	E=C_(e1).inGroup("E")
	ninj=C_(ninj1).inGroup("ninj")
	#eff=(B-A)*PhiNode((E-mu)/sigma)+A
	eff=StrNode("(B-A)*phi((E-mu)/sigma)+A",("A",A),("B",B),("mu",mu),("sigma",sigma),("E",E)).inGroup("eff")
	nrec=BinNode(eff,ninj).withObservedValue(nrec1).inGroup("nrec")
	g.addNode(nrec)
        
dot=pydot.Dot()
for i in g.dumpTopology():
	dot.add_edge(pydot.Edge(pydot.Node(i[1]),pydot.Node(i[0])))

em=mcupy.core.ensemble_type()
for i in range(0,30000):
	g.ensemble_sample(em)
	if i>100 and i%2==0:
		print(em[0][0],em[0][1])
	
#print(len(em))
