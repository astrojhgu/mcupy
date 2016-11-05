
##Example
Check ![example/estimate_eff/estimate_eff.py](example/estimate_eff/estimate_eff1.py).<br/>
This is an example given in thie book ![BAYESIAN METHODS FOR THE PHYSICAL SCIENCES](http://www.brera.mi.astro.it/~andreon/BayesianMethodsForThePhysicalSciences/) section 8.2.

First let's import necessary packages


```python
import sys
from mcupy.graph import *
from mcupy.nodes import *
from mcupy.utils import *
try:
    import pydot
except(ImportError):
    import pydot_ng as pydot
```

Create a graph object, which is used to hold nodes.


```python
g=Graph()
```

Create some nodes


```python
A=FixedUniformNode(0.001,1-1e-5).withTag("A")
B=FixedUniformNode(0.001,1-1e-5).withTag("B")
mu=FixedUniformNode(.001,100-1e-5).withTag("mu")
sigma=FixedUniformNode(.001,100-1e-5).withTag("sigma")
```

And some more nodes


```python
for l in open('eff.txt'):
    e1,nrec1,ninj1=l.split()
    e1=float(e1)
    nrec1=float(nrec1)
    ninj1=float(ninj1)
    E=C_(e1).inGroup("E")
    ninj=C_(ninj1).inGroup("ninj")
    eff=((B-A)*PhiNode((E-mu)/sigma)+A).inGroup("eff")
    nrec=BinNode(eff,ninj).withObservedValue(nrec1).inGroup("nrec")
    g.addNode(nrec)
```

Then let us check the topology of graph


```python
display_graph(g)
```


![png](output_9_0.png)


It's correct.<br/>
Then we'd like to perform several sampling and record the values.<br/>

Before sampling, we need to decide which variables we need to monitor.


```python
mA=g.getMonitor(A)
mB=g.getMonitor(B)
mSigma=g.getMonitor(sigma)
mMu=g.getMonitor(mu)
```

We need a variable to hold the results


```python
result=[]
```

Then we perform the sampling for 1000 time for burning


```python
for i in log_progress(range(1000)):
    g.sample()    
```

Then we perform 30000 sampling and record the results


```python
for i in log_progress(range(30000)):
    g.sample()
    result.append([mA.get(),mB.get(),mMu.get(),mSigma.get()])
```

Then we plot the results.


```python
%matplotlib inline
import seaborn
import scipy
result=scipy.array(result)
seaborn.jointplot(result[:,0],result[:,1],kind='hex')
```

    /usr/lib/python3.5/site-packages/matplotlib/__init__.py:878: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))
    /usr/lib/python3.5/site-packages/matplotlib/__init__.py:898: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))





    <seaborn.axisgrid.JointGrid at 0x7ff35c029780>




![png](output_19_2.png)



```python
seaborn.jointplot(result[:,0],result[:,2],kind='hex')
```

    /usr/lib/python3.5/site-packages/matplotlib/__init__.py:898: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))





    <seaborn.axisgrid.JointGrid at 0x7ff34df0ae80>




![png](output_20_2.png)



```python
seaborn.jointplot(result[:,0],result[:,3],kind='hex')
```

    /usr/lib/python3.5/site-packages/matplotlib/__init__.py:898: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))





    <seaborn.axisgrid.JointGrid at 0x7ff32e041c18>




![png](output_21_2.png)



```python
seaborn.jointplot(result[:,1],result[:,2],kind='hex')
```

    /usr/lib/python3.5/site-packages/matplotlib/__init__.py:898: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))





    <seaborn.axisgrid.JointGrid at 0x7ff32dd9b908>




![png](output_22_2.png)



```python
seaborn.jointplot(result[:,1],result[:,3],kind='hex')
```

    /usr/lib/python3.5/site-packages/matplotlib/__init__.py:898: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))





    <seaborn.axisgrid.JointGrid at 0x7ff32db1d898>




![png](output_23_2.png)



```python
seaborn.jointplot(result[:,2],result[:,3],kind='hex')
```

    /usr/lib/python3.5/site-packages/matplotlib/__init__.py:898: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))





    <seaborn.axisgrid.JointGrid at 0x7ff32d89d780>




![png](output_24_2.png)



```python

```
