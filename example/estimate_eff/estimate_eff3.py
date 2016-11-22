#!/usr/bin/env python

import sys
import math
import scipy
from random import random
from mcupy.core import *
from scipy.special import erf,loggamma

def log_factorial(n):
	y=loggamma(n+1)
	return y.real

def log_CN(m,n):
	y=log_factorial(m)-log_factorial(n)-log_factorial(m-n)
	return y.real

def phi(x):
	result=(1+erf(x/math.sqrt(2)))/2
	return result.real

def logdbin(x,p,n):
	return log_CN(n,x)+x*math.log(p)+(n-x)*math.log(1-p)
	
E=[]
nrec=[]
ninj=[]

for l in open('eff.txt'):
	e1,nrec1,ninj1=l.split()
	E.append(float(e1))
	nrec.append(float(nrec1))
	ninj.append(float(ninj1))
	
        
def logprob(x):
	logprob=0
	A=x[0]
	B=x[1]
	mu=x[2]
	sigma=x[3]

	if A<0 or A>1 or B<0 or B>1:
		#return -math.inf
		return -float('infinity')
	for i in range(0,len(E)):
		eff=A+(B-A)*phi((E[i]-mu)/sigma)
		logprob+=logdbin(nrec[i],eff,ninj[i])

	return logprob

#ensemble=[]
nensemble=100
ensemble=scipy.zeros([nensemble,4])

for i in range(nensemble):
	ensemble[i,:]=.2+random()*.2-.1,.9+random()*.2-.1,15+random()*.2-.1,12+random()*.2-.1
	#ensemble.append(x)
	
for i in range(0,1000):
	ensemble=ensemble_sample(logprob,ensemble)
	#print(ensemble[0][0],ensemble[0][1])
	print("{0} {1}".format(ensemble[0][0],ensemble[0][1]))
