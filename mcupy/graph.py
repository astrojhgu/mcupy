from . import core
import sys
from abc import ABCMeta, abstractmethod



def Tag(*t):
	if len(t)==1 and isinstance(t[0],str):
		return tag_t(t(0))
	elif len(t)==2 and isinstance(t[0],str) and isinstance(t[1],int):
		return tag_t(t(1))
	else:
		raise RuntimeError("input param must be string and an optional int")
    
	
class Graph:
	def __init__(self):
		self.graph=core.cppgraph()
		self.nodes=set()
		pass

	def __getstate__(self):
		state=self.__dict__.copy()
		del state['graph']
		return state

	def __setstate__(self,state):
		self.__dict__.update(state)
		self.graph=core.cppgraph()
		nodes1=self.nodes.copy()
		self.nodes=set()
		for n in nodes1:
			n.addToGraph(self)

	def addNode(self,node):
		node.addToGraph(self)

	def sample(self):
		self.graph.sample()

	def getMonitor(self,n,*idx):
		if isinstance(n,NodeOutput):
			return self.graph.get_monitor(n.node.getTag(),n.index)
		elif isinstance(n,Node):
			if len(idx)==0:
				return self.graph.get_monitor(n.getTag(),0)
			else:
				return self.graph.get_monitor(n.getTag(),int(idx[0]))
		else:
			raise RuntimeException("must supply node or nodeoutput")

	def dumpTopology(self):
		result=set()		
		for i in self.nodes:
			if i.named:
				for j in i.enumerateNamedParents():
					result.add((i.tagName,j.tagName))
		return result

		
class Node(metaclass=ABCMeta):
	defaultTagName="__node__"
	nodeCount=0
	
	def __init__(self,*parents):
		self.graph=None
		if not all([isinstance(i,Node) or isinstance(i,NodeOutput) for i in parents]):
			raise RuntimeError("all parents must be either Node or NodeOutput")
		self.parents=[NodeOutput(i) for i in parents]
		self.tagName=Node.defaultTagName
		self.tagIndex=Node.nodeCount
		self.named=False
		Node.nodeCount+=1

	def withTag(self,tagName,*tagIndex):
		self.tagName=tagName
		if tagIndex:
			self.tagIndex=tagIndex
		self.named=True
		return self

	def inGroup(self,tagName):
		self.tagName=tagName
		self.named=True
		return self

	def enumerateNamedParents(self):
		result=set()
		#print("begin enumerate:",self)
		for i in self.parents:
			if i.node.named:
		#		print("find:",i.node.tagName)
				result.add(i.node)
			else:
		#		print("unnamed:",i.node)
				result.update(i.node.enumerateNamedParents())
		#print("end enumerate:",self)
		return result

	def __getstate__(self):
		state=self.__dict__.copy()
		state['graph']=None
		return state

	@abstractmethod
	def getNodePtr(self):
		pass

	def getTag(self):
		return core.tag_t(self.tagName,self.tagIndex)
	
	def getAssociatedGraph(self):
		return self.graph
	
	def addToGraph(self,g):
		if not isinstance(g,Graph):
			raise RuntimeError("not graph")

		for p in self.parents:
			if isinstance(p,Node):
				p.addToGraph(g)
			elif isinstance(p,NodeOutput):
				p.node.addToGraph(g)

		self.addSelfToGraph(g)

	def addSelfToGraph(self,g):
		if self.graph is not g:
			na=g.graph.add_node(self.getNodePtr(),self.getTag())
			g.nodes.add(self)
			for p in self.parents:
				na.with_parent(p.node.getTag(),p.index)

			if isinstance(self,StochasticNode):
				for i in range(0,len(self.value)):
					if self.getValue(i) is None:
						continue
					if self.isObserved(i):
						na.with_observed_value(i,self.getValue(i))
					else:
						na.with_value(i,self.getValue(i));
					
			self.graph=g
			na.done()


	def __add__(self,that):
		return AddNode(self,that)

	def __sub__(self,that):
		return SubNode(self,that)

	def __mul__(self,that):
		return MulNode(self,that)

	def __truediv__(self,that):
		return DivNode(self,that)

	def __lt__(self,that):
		return LtNode(self,that)

	def __gt__(self,that):
		return GtNode(self,that)

	def __le__(self,that):
		return LeNode(self,that)

	def __ge__(self,that):
		return GeNode(self,that)

class StochasticNode(Node,metaclass=ABCMeta):
	def __init__(self,*parents):
		Node.__init__(self,*parents)
		self.value=[]
		self.observed=[]

	def getValue(self,i):
		if self.graph==None:
			return self.value[i]
		else:
			return self.graph.graph.get_value(self.getTag(),i)
			
	def setValue(self,i,v):
		if self.graph==None:
			while len(self.value)-1<i:
				self.value+=[None]
			self.value[i]=v
		else:
			self.graph.graph.set_value(self.getTag(),i,v)

	def isObserved(self,i):
		if self.graph==None:
			return self.observed[i]
		else:
			return self.graph.graph.is_observed(self.getTag(),i)

	def setObserved(self,i,o):
		if self.graph==None:
			while len(self.observed)-1<i:
				self.observed+=[False]
			self.observed[i]=o
		else:
			return self.graph.graph.set_observed(self.getTag(),i,o)


	def withObservedValue(self,*value):
		for i in range(0,len(value)):
			if value[i] is not None:
				self.setValue(i,value[i])
				self.setObserved(i,True)
		return self

	def withInitialValue(self,*value):
		for i in range(0,len(value)):
			if value[i] is not None:
				self.setValue(i,value[i])
				self.setObserved(i,False);
		return self

class DeterministicNode(Node,metaclass=ABCMeta):
	def __init__(self,*parents):
		Node.__init__(self,*parents)
		
	
class NodeOutput:
	def __init__(self,node,*idx):
		if isinstance(node,Node):
			self.node=node		
			if len(idx)==0:
				self.index=0
			elif len(idx)==1:
				self.index=int(idx(0))
			else:
				raise RuntimeError("idx can be either empty or an int")
		elif isinstance(node,NodeOutput):
			self.node=node.node
			self.index=node.index
		else:
			raise RuntimeError("first parameter must be a Node")


	def __add__(self,that):
		return AddNode(self,that)

	def __sub__(self,that):
		return SubNode(self,that)

	def __mul__(self,that):
		return MulNode(self,that)

	def __truediv__(self,that):
		return DivNode(self,that)

	def __lt__(self,that):
		return LtNode(self,that)

	def __gt__(self,that):
		return GtNode(self,that)

	def __le__(self,that):
		return LeNode(self,that)

	def __ge__(self,that):
		return GeNode(self,that)


class AddNode(DeterministicNode):
	def __init__(self,p1,p2):
		DeterministicNode.__init__(self,p1,p2)

	def getNodePtr(self):
		return core.add_node()


class SubNode(DeterministicNode):
	def __init__(self,p1,p2):
		DeterministicNode.__init__(self,p1,p2)

	def getNodePtr(self):
		return core.sub_node()

class MulNode(DeterministicNode):
	def __init__(self,p1,p2):
		DeterministicNode.__init__(self,p1,p2)

	def getNodePtr(self):
		return core.mul_node()


class DivNode(DeterministicNode):
	def __init__(self,p1,p2):
		DeterministicNode.__init__(self,p1,p2)

	def getNodePtr(self):
		return core.div_node()


class LtNode(DeterministicNode):
	def __init__(self,p1,p2):
		StochasticNode.__init__(self,p1,p2)

	def getNodePtr(self):
		return core.lt_node()

class GtNode(DeterministicNode):
	def __init__(self,p1,p2):
		StochasticNode.__init__(self,p1,p2)

	def getNodePtr(self):
		return core.gt_node()

class LeNode(DeterministicNode):
	def __init__(self,p1,p2):
		StochasticNode.__init__(self,p1,p2)

	def getNodePtr(self):
		return core.le_node()

class GeNode(DeterministicNode):
	def __init__(self,p1,p2):
		StochasticNode.__init__(self,p1,p2)

	def getNodePtr(self):
		return core.ge_node()

class MixtureNode(StochasticNode):
	def __init__(self,components,*parents):
		StochasticNode.__init__(self,*parents)
		self.components=components

	def getNodePtr(self):
		snv=core.stochastic_node_vec()
		for i in self.components:
			snv.append(core.convert_to_stochastic(i.getNodePtr()))
		return core.mixture_node(snv)
