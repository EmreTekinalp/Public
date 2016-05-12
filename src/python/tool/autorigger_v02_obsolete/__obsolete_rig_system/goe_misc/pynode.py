'''
Created on Oct 31, 2014

@author: Emre
'''

import pymel.core as pm


class PyNode(object):

    """Node class which returns a PyNode object"""

    def __init__(self):
        """Class constructor function"""
        self._nodes = pm.allNodeTypes()
    # end def __init__

    def __getattr__(self, name):
        """Override getattr function and return pynode"""
        if name not in self._nodes:
            raise TypeError('Node does not exist: %s' % name)
        else:
            return pm.createNode(name)
        # end if create and return pynode
    # end def __getattr__
# end class PyNode
