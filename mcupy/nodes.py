from . import core
from . graph import StochasticNode,DeterministicNode,NodeOutput
from . import graph

AddNode=graph.AddNode
Subnode=graph.SubNode
MulNode=graph.MulNode
DivNode=graph.DivNode


class ConstNode(DeterministicNode):
	def __init__(self,v):
		DeterministicNode.__init__(self)
		self.value=v

	def getNodePtr(self):
		return core.const_node(self.value)

C_=ConstNode

class CauchyNode(StochasticNode):
	def __init__(self,*p):
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.cauchy_node()

class ChisqrNode(StochasticNode):
	def __init__(self,k):
		StochasticNode.__init__(self)
		self.k=k

	def getNodePtr(self):
		return core.chisqr_node(self.k)

class LogNormalNode(StochasticNode):
	def __init__(self,*p):
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.log_normal_node()
	
class NormalNode(StochasticNode):
	def __init__(self,*p):
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.normal_node()

class AbsNode(DeterministicNode):
	def __init__(self,x):
		DeterministicNode.__init__(self,x)

	def getNodePtr(self):
		return core.abs_node()

class BetaNode(StochasticNode):
	def __init__(self,a,b):
		StochasticNode.__init__(self)
		self.a=a
		self.b=b

	def getNodePtr(self):
		return core.beta_node(self.a,self.b)

class BernNode(StochasticNode):
	def __init__(self,*p):
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.bern_node()

	
class BinNode(StochasticNode):
	def __init__(self,*pn):
		StochasticNode.__init__(self,*pn)

	def getNodePtr(self):
		return core.bin_node()

class BvnormalNode(StochasticNode):
	def __init__(self,*p):
		"""
		mu1,mu2,sigma1,sigma2,rho
		"""
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.bvnormal_node()


class CosNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,p)

	def getNodePtr(self):
		return core.cos_node()

class DExpNode(StochasticNode):
	def __init__(self,*p):
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.dexp_node()

class ExpNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,p)

	def getNodePtr(self):
		return core.exp_node()

class SinNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,p)

	def getNodePtr(self):
		return core.sin_node()

class TanNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,p)
		
	def getNodePtr(self):
		return core.tan_node()

class LogNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,p)

	def getNodePtr(self):
		return core.log_node()	

class Log10Node(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,p)

	def getNodePtr(self):
		return core.log_node()

class SqrtNode(DeterministicNode):
	def __init__(self,p):
		DeterministicNode.__init__(self,p)

	def getNodePtr(self):
		return core.sqrt_node()

class FNode(StochasticNode):
	def __init__(self,*p):
		"""
		n,m
		"""
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.f_node()
	
class GammaNode(StochasticNode):
	def __init__(self,*p):
		"""
		r,lbd
		"""
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.gamma_node()

class GenGammaNode(StochasticNode):
	def __init__(self,*p):
		"""
		r,lbd,b
		"""
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.gen_gamma_node()

class ILogitNode(DeterministicNode):
	def __init__(self,x):
		DeterministicNode.__init__(self,x)

	def getNodePtr(self):
		return core.ilogit_node()

class LogitNode(DeterministicNode):
	def __init__(self,x):
		DeterministicNode.__init__(self,x)

	def getNodePtr(self):
		return core.logit_node()

class LogisticNode(DeterministicNode):
	def __init__(self,m,s):
		DeterministicNode.__init__(self,m,s)

	def getNodePtr(self):
		return core.logistic_node()
			
class ParetoNode(StochasticNode):
	def __init__(self,*p):
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.pareto_node()

class PhiNode(DeterministicNode):
	def __init__(self,x):
		DeterministicNode.__init__(self,x)

	def getNodePtr(self):
		return core.phi_node()

class PoissonNode(StochasticNode):
	def __init__(self,*lbd):
		StochasticNode.__init__(self,*lbd)

	def getNodePtr(self):
		return core.poisson_node()

class StepNode(DeterministicNode):
	def __init__(self,x):
		DeterministicNode.__init__(self,x)

	def getNodePtr(self):
		return core.step_node()

class FixedUniformNode(StochasticNode):
	def __init__(self,a,b):
		StochasticNode.__init__(self)
		self.a=a
		self.b=b

	def getNodePtr(self):
		return core.fixed_uniform_node(self.a,self.b)

class UniformNode(StochasticNode):
	def __init__(self,*p):
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.uniform_node()

class TNode(StochasticNode):
	def __init__(self,*p):
		StochasticNode.__init__(self,*p)

	def getNodePtr(self):
		return core.t_node()

class DiscreteUniformNode(StochasticNode):
	def __init__(self,a,b):
		StochasticNode.__init__(self)
		self.a=a
		self.b=b

	def getNodePtr(self):
		return core.discrete_uniform_node(self.a,self.b)
	
class SwitchNode(DeterministicNode):
	def __init__(self,s,*p):
		DeterministicNode.__init__(self,*(p+(s,)))

	def getNodePtr(self):
		return core.switch_node(len(self.parents)-1)

class CondNode(DeterministicNode):
	def __init__(self,s,p1,p2):
		DeterministicNode.__init__(self,s,p1,p2)

	def getNodePtr(self):
		return core.cond_node()
		
class StrNode(DeterministicNode):
	def __init__(self,expr,*args):
		parents=tuple(i[1] for i in args)
		DeterministicNode.__init__(self,*parents)
		self.expr=expr
		self.arg_names=core.str_vec(len(args))
		for i in range(len(args)):
			self.arg_names[i]=args[i][0]
		
	def getNodePtr(self):
		return core.str_node_(self.expr,self.arg_names)

