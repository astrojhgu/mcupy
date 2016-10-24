#!/usr/bin/env python

import sys
from mcupy.graph import *
from mcupy.nodes import *

g=Graph()
A=UniformNode(0.001,1-1e-5)
B=UniformNode(0.001,1-1e-5)
mu=UniformNode(.001,100-1e-5)
sigma=UniformNode(.001,100-1e-5)
n=0
for l in open('eff.txt'):
	e1,nrec1,ninj1=l.split()
	e1=float(e1)
	nrec1=float(nrec1)
	ninj1=float(ninj1)
	E=C_(e1)
	ninj=C_(ninj1)
	#eff=(B-A)*PhiNode((E-mu)/sigma)+A
	eff=StrNode("(B-A)*phi((E-mu)/sigma)+A",("A",A),("B",B),("mu",mu),("sigma",sigma),("E",E))
	nrec=BinNode(eff,ninj).withObservedValue(nrec1)
	g.addNode(nrec)
        
ma=g.getMonitor(A)
mb=g.getMonitor(B)

for i in range(0,30000):
	g.sample()
	print(ma.get(),mb.get())
