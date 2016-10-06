#!/usr/bin/env python

from mcupy.core import arms
import math

x=0
for i in range(0,10000):
    x=arms(lambda x:(-x*x),-100,100,x)
    print(x)
    
