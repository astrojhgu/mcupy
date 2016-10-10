#!/usr/bin/env python


import pyparsing

ident=pyparsing.Regex("[a-zA-Z_][a-zA-Z_0-9]*")

number=pyparsing.Regex("[+-]?[0-9]+\.?[0-9]*([Ee][+-]?[0-9]+)?").setParseAction(lambda t:float(t[0]))

numberList=number+pyparsing.ZeroOrMore(pyparsing.Literal(",").suppress()+number)

rList=pyparsing.Literal("c").suppress()+pyparsing.Literal("(").suppress()+numberList+pyparsing.Literal(")").suppress()

assignment=ident.setResultsName("var")+pyparsing.Literal("<-").suppress()+(pyparsing.Group(rList)|number).setResultsName("data")

jagsdatafile=pyparsing.OneOrMore(pyparsing.Group(assignment))

def result2list(r):
	return [i for i in r]

def parseJagsDataFile(f):
	if isinstance(f,str):
		jfile=open(f)
	else:
		jfile=f
		
	
	result={i.var:result2list(i.data) for i in jagsdatafile.parseFile(jfile)}
	return result
