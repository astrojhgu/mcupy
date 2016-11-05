#!/usr/bin/env python

from mcupy.graph import *
from mcupy.nodes import *

g=Graph()

l1=FixedUniformNode(1e-6,100)
l2=FixedUniformNode(1e-6,100)
y=DiscreteUniformNode(0,113)

for line in open('coal.dat'):
	year,accid=line.split()
	year=int(year)
	accid=int(accid)
	y1=C_(year)
	#l=switch((y>const(year,("y",cnt))),(l1,l2),("lambda",cnt))
	
	#l=func("cond(y1<y,l1,l2)",("y1","y","l1","l2"),(y1,y,l1,l2),("l",cnt))
	l=CondNode(y1<y,l1,l2)
	
	a=PoissonNode(l).withObservedValue(accid)
	g.addNode(a)
            
			
ml1=g.getMonitor(l1)
ml2=g.getMonitor(l2)
my=g.getMonitor(y)

for i in range(0,10000):
	g.sample()
	print(ml1.get(),ml2.get(),my.get())
