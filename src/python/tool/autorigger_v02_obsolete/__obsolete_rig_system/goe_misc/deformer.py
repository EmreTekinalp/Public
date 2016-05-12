'''
Created on Jul 11, 2015

@author: Emre
'''

from goe_misc import pynode
reload(pynode)

node = pynode.PyNode()

mlt = node.multiplyDivide
rmv = node.remapValue
cnd = node.condition
mdl = node.multDoubleLinear

mlt.input1X.connect(rmv.inputValue)
rmv.outValue.connect(cnd.firstTerm)
mdl.input1.connect(cnd.secondTerm)
