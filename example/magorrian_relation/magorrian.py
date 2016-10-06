#!/usr/bin/env python

import sys

from mcupy.nodes import *
from mcupy.graph import *

g=Graph()

xx=ConstNode(0)
yy=ConstNode(1)
a=TNode(ConstNode(0),ConstNode(1),ConstNode(1)).withInitialValue(1)
b=NormalNode(ConstNode(0),ConstNode(100)).withInitialValue(0)
scat=GammaNode(ConstNode(1e-2),ConstNode(1e-2)).withInitialValue(1e-2)
intrscat=ConstNode(1)/SqrtNode(scat)
for line in open('magorrian.dat'):
	x1,errx1,y1,erry1=[float(i) for i in line.split()]
	x=UniformNode(-1e4,1e4).withInitialValue(x1)
	obsx=NormalNode(x,ConstNode(errx1)).withObservedValue(x1)
	y=NormalNode(b+a*(x-ConstNode(2.3)),intrscat).withInitialValue(y1)
	obsy=NormalNode(y,ConstNode(erry1)).withObservedValue(y1)
	g.addNode(obsx)
	g.addNode(obsy)

ma=g.getMonitor(a)
mb=g.getMonitor(b)
ms=g.getMonitor(scat)

for i in range(0,10000):
	g.sample()
	print(ma.get(),mb.get(),ms.get())
