#!/usr/bin/env python

import sys

from mcupy.nodes import *
from mcupy.graph import *

g=Graph()

xx=C_(0)
yy=C_(1)
a=TNode(C_(0),C_(1),C_(1)).withInitialValue(1)
b=NormalNode(C_(0),C_(100)).withInitialValue(0)
scat=GammaNode(C_(1e-2),C_(1e-2)).withInitialValue(1e-2)
intrscat=C_(1)/SqrtNode(scat)
for line in open('magorrian.dat'):
	x1,errx1,y1,erry1=[float(i) for i in line.split()]
	x=FixedUniformNode(-1e4,1e4).withInitialValue(x1)
	obsx=NormalNode(x,C_(errx1)).withObservedValue(x1)
	y=NormalNode(b+a*(x-C_(2.3)),intrscat).withInitialValue(y1)
	obsy=NormalNode(y,C_(erry1)).withObservedValue(y1)
	g.addNode(obsx)
	g.addNode(obsy)

ma=g.getMonitor(a)
mb=g.getMonitor(b)
ms=g.getMonitor(scat)

for i in range(0,10000):
	g.sample()
	print(ma.get(),mb.get(),ms.get())
