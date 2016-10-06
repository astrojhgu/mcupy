from . import core
from . graph import StochasticNode,DeterministicNode,NodeOutput
from . import graph

AddNode=graph.AddNode
Subnode=graph.SubNode
MulNode=graph.MulNode
DivNode=graph.DivNode


class ConstNode(DeterministicNode):
	def __init__(self,v):
		DeterministicNode.__init__(self,1)
		self.value=v

	def getValue(self,i):
		return self.value

	def getNodePtr(self):
		return core.const_node(self.value)

class NormalNode(StochasticNode):
	def __init__(self,m,s):
		StochasticNode.__init__(self,[NodeOutput(m).getValue()],m,s)

	def getNodePtr(self):
		return core.normal_node()

class AbsNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,1,p)

	def getNodePtr(self):
		return core.abs_node()

	def getValue(self,i):
		return abs(parents[0].getValue())


class BetaNode(DeterministicNode):
	def __init__(self,a,b):
		StochasticNode.__init__(self,[0.5])
		self.a=a
		self.b=b

	def getNodePtr(self):
		return core.beta_node(self.a,self.b)

class BinNode(StochasticNode):
	def __init__(self,p,n):
		StochasticNode.__init__(self,[NodeOutput(p).value()*NodeOutput(n).value()],p,n)

	def getNodePtr(self):
		return core.bin_node()

class BvnormalNode(StochasticNode):
	def __init__(self,mu1,mu2,sigma1,sigma2,rho):
		StochasticNode.__init__(self,[NodeOutput(mu1).value(),NodeOutput(mu2).value()],mu1,mu2,sigma1,sigma2,rho)

	def getNodePtr(self):
		return core.bvnormal_node()


class CosNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,1,p)

	def getNodePtr(self):
		return core.cos_node()

	def getValue(self,i):
		import math
		return math.cos(parents[0].getValue())

class SinNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,1,p)

	def getNodePtr(self):
		return core.sin_node()

	def getValue(self,i):
		import math
		return math.sin(parents[0].getValue())

class TanNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,1,p)
		
	def getNodePtr(self):
		return core.tan_node()

	def getValue(self,i):
		import math
		return math.tan(parents[0].getValue())

class LogNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,1,p)

	def getNodePtr(self):
		return core.log_node()	

	def getValue(self,i):
		import math
		return math.log(parents[0].getValue())

class Log10Node(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,1,p)

	def getNodePtr(self):
		return core.log_node()

	def getValue(self,i):
		import math
		return math.log10(parents[0].getValue())

class SqrtNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,1,p)

	def getNodePtr(self):
		return core.sqrt_node()

	def getValue(self,i):
		import math
		return math.sqrt(parents[0].getValue())

	
class GammaNode(StochasticNode):
	def __init__(self,r,lbd):
		StochasticNode.__init__(self,[NodeOutput(r).value()/NodeOutput(lbd).value()],r,lbd)

	def getNodePtr(self):
		return core.gamma_node()

class ILogitNode(DeterministicNode):
	def __init__(self,x):
		DeterministicNode.__init__(self,1,x)

	def getNodePtr(self):
		return core.ilogit_node()

	def getValue(self,i):
		import math
		def ilogit(x):
			return 1.0/(1+math.exp(-x))
		return ilogit(parents[0].value())

class LogitNode(DeterministicNode):
	def __init__(self,x):
		DeterministicNode.__init__(self,1,x)

	def getNodePtr(self):
		return core.logit_node()

	def getValue(self,i):
		import math
		def logit(x):
			return math.log(x/(1-x))

		return logit(parents[0].value())

			
class ParetoNode(StochasticNode):
	def __init__(self,c,a):
		StochasticNode.__init__(self,[NodeOutput(c).value()],c,a)

	def getNodePtr(self):
		return core.pareto_node()

class PhiNode(DeterministicNode):
	def __init__(self,x):
		StochasticNode.__init__(self,1,x)

	def getNodePtr(self):
		return core.phi_node()
		
	def getValue(self,i):
		import math
		def erf(x):
			a1 = 0.0705230784
			a2 = 0.0422820123
			a3 = 0.0092705272
			a4 = 0.0001520143
			a5 = 0.0002765672
			a6 = 0.0000430638
			return 1-1/(1+a1*x+a2*x**2+
						a3*x**3+
						a4*x**4+
						a5*x**5+
						a6*x**6)**16
		def phi(x):
		  SQRT2=2**0.5
		  return (1+erf(x/SQRT2))/2
		return phi(self.parents[0].value())

	
class PoissonNode(StochasticNode):
	def __init__(self,lbd):
		StochasticNode.__init__(self,[NodeOutput(lbd).value()],lbd)

	def getNodePtr(self):
		return core.poisson_node()

def StepNode(DeterministicNode):
	def __init__(self,x):
		DeterministicNode.__init__(self,1,x)

	def getValue(self,i):
		if self.parents[0].value()>=0:
			return 1.0
		else:
			return 0.0

	def getNodePtr(self):
		return core.step_node()

def UniformNode(StochasticNode):
	def __init__(self,a,b):
		StochasticNode.__init__(self,[(a+b)/2])
		self.a=a
		self.b=b

	def getNodePtr(self):
		return core.uniform_node(a,b)

class TNode(StochasticNode):
	def __init__(self,m,s,k):
		StochasticNode.__init__(self,[NodeOutput(m).getValue()],m,s,k)

	def getNodePtr(self):
		return core.t_node()

class DiscreteUniformNode(StochasticNode):
	def __init__(self,a,b):
		StochasticNode.__init__(self,[int((a+b)/2)])
		self.a=a
		self.b=b

	def getNodePtr(self):
		return core.discrete_uniform_node(a,b)
	
class SwitchNode(DeterministicNode):
	def __init__(self,s,*p):
		StochasticNode.__init__(self,1,*(p+(s,)))

	def getNodeKey(self):
		return core.switch_node(len(parents)-1)
		
