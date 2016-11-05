#!/usr/bin/env python

from mcupy import *
from mcupy.graph import *
from mcupy.nodes import *
from mcupy.jagsparser import *
import math

g=Graph()

data=parseJagsDataFile("8.5.R")

dataLength=len(data['z'])

lgfclus0=NormalNode(C_(0),C_(10))
alpha=NormalNode(C_(0),C_(10))
beta=NormalNode(C_(0),C_(10))
gamma=NormalNode(C_(0),C_(10))
zeta=NormalNode(C_(0),C_(10))
ilogitlgfclus0=ILogitNode(lgfclus0)
g.addNode(ilogitlgfclus0)

for i in range(0,dataLength):
	nbkg=FixedUniformNode(1,1e7)
	fbkg=BetaNode(1,1)
	nclus=FixedUniformNode(1,1e7)

	obsnbkg=PoissonNode(nbkg).withObservedValue(data["obsnbkg"][i])
	g.addNode(obsnbkg)

	obsbluebkg=BinNode(fbkg,obsnbkg).withObservedValue(data["obsnbluebkg"][i])
	g.addNode(obsbluebkg)

	obsntot=PoissonNode(nbkg/C_(data["C"][i])+nclus).withObservedValue(data["obsntot"][i])
	g.addNode(obsntot)

	fclus=ILogitNode(lgfclus0+alpha*C_(math.log(data["r200"][i]/0.25))+beta*C_(data["lgM"][i]-11)+gamma*C_(data["z"][i]-0.3)+zeta*C_((data["lgM"][i]-11)*(data["z"][i]-0.3)))
	f=(fbkg*nbkg/C_(data["C"][i])+fclus*nclus)/(nbkg/C_(data["C"][i])+nclus)
	
	obsnbluetot=BinNode(f,obsntot).withObservedValue(data["obsnbluetot"][i])
	g.addNode(obsnbluetot)


malpha=g.getMonitor(alpha)
mbeta=g.getMonitor(beta)
for i in range(0,1000):
	g.sample()
	print(malpha.get(),mbeta.get())
