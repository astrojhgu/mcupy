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
		pass

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
		
		
class Node(metaclass=ABCMeta):
	defaultTagName="__node__"
	nodeCount=0
	
	def __init__(self,nOutputs,*parents):
		self.graph=None
		if not all([isinstance(i,Node) or isinstance(i,NodeOutput) for i in parents]):
			raise RuntimeError("all parents must be either Node or NodeOutput")
		self.parents=[NodeOutput(i) for i in parents]
		self.tagName=Node.defaultTagName
		self.tagIndex=Node.nodeCount
		self.nOutputs=int(nOutputs)
		Node.nodeCount+=1

	@abstractmethod
	def getNodePtr(self):
		pass

	@abstractmethod
	def getValue(self,i):
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
			for p in self.parents:
				na.with_parent(p.node.getTag(),p.index)

			if isinstance(self,StochasticNode):
				for i in range(0,len(self.value)):
					if self.isObserved(i):
						na.with_observed_value(i,self.getValue(i))
					else:
						na.with_value(i,self.getValue(i))
			self.graph=g
			na.done()


	def __add__(self,that):
		return AddNode(self,that)

	def __sub__(self,that):
		return SubNode(self,that)

	def __mul__(self,that):
		return MulNode(self,that)

	def __div__(self,that):
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
	def __init__(self,value,*parents):
		Node.__init__(self,len(value),*parents)
		self.value=value
		self.observed=[False for i in value]

	def getValue(self,i):
		if self.graph==None:
			return self.value[i]
		else:
			return self.graph.graph.get_value(self.getTag(),i)
			
	def setValue(self,i,v):
		if self.graph==None:
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
		return self

class DeterministicNode(Node,metaclass=ABCMeta):
	def __init__(self,nOutputs,*parents):
		Node.__init__(self,nOutputs,*parents)
		
	
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


	def getValue(self):
		return self.node.getValue(self.index)


	def __add__(self,that):
		return AddNode(self,that)

	def __sub__(self,that):
		return SubNode(self,that)

	def __mul__(self,that):
		return MulNode(self,that)

	def __div__(self,that):
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
		DeterministicNode.__init__(self,1,p1,p2)

	def getValue(self,i):
		return self.parents[0].getValue()+self.parents[1].getValue()

	def getNodePtr(self):
		return core.add_node()


class SubNode(DeterministicNode):
	def __init__(self,p1,p2):
		DeterministicNode.__init__(self,1,p1,p2)

	def getValue(self,i):
		return self.parents[0].getValue()-self.parents[1].getValue()

	def getNodePtr(self):
		return core.sub_node()

class MulNode(DeterministicNode):
	def __init__(self,p1,p2):
		DeterministicNode.__init__(self,1,p1,p2)

	def getValue(self,i):
		return self.parents[0].getValue()*self.parents[1].getValue()

	def getNodePtr(self):
		return core.mul_node()


class DivNode(DeterministicNode):
	def __init__(self,p1,p2):
		DeterministicNode.__init__(self,1,p1,p2)

	def getValue(self,i):
		return self.parents[0].getValue()/self.parents[1].getValue()

	def getNodePtr(self):
		return core.div_node()


class LtNode(DeterministicNode):
	def __init__(self,p1,p2):
		StochasticNode.__init__(self,1,p1,p2)

	def getValue(self,i):
		return float(self.parents[0].value()<parents[1].value())

	def getNodePtr(self):
		return core.lt_node()

class GtNode(DeterministicNode):
	def __init__(self,p1,p2):
		StochasticNode.__init__(self,1,p1,p2)

	def getValue(self,i):
		return float(self.parents[0].value()>parents[1].value())

	def getNodePtr(self):
		return core.gt_node()

class LeNode(DeterministicNode):
	def __init__(self,p1,p2):
		StochasticNode.__init__(self,1,p1,p2)

	def getValue(self,i):
		return float(self.parents[0].value()<=parents[1].value())

	def getNodePtr(self):
		return core.le_node()

class GeNode(DeterministicNode):
	def __init__(self,p1,p2):
		StochasticNode.__init__(self,1,p1,p2)

	def getValue(self,i):
		return float(self.parents[0].value()>=parents[1].value())

	def getNodePtr(self):
		return core.ge_node()
