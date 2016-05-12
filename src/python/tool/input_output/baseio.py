"""
@package: io.baseio
@brief: Deal with input and output data and create json files
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""


import json
import logging
import pymel.core as pm
from abc import abstractmethod

from core import interface
reload(interface)

reload(logging)
logging.basicConfig(format='', level=logging.DEBUG)
logging.basicConfig(format='', level=logging.ERROR)


class BaseIO(interface.AssetInterface):
    """Base class of Inputs and Outputs which should be subclassed."""

    def __init__(self):
        """Initialize BaseIO class and subclass AssetInterface."""
        super(BaseIO, self).__init__()
    # end def __init__

    def tag_nodes(self):
        """Tag the nodes by reading the currentIO."""
        selection = pm.ls(sl=True)
        for s in selection:
            nodetype = pm.nodeType(s)
            if nodetype == 'transform':
                child = pm.listRelatives(s, c=True)
                if child:
                    s = child[0]
                    nodetype = pm.nodeType(s)
                # end if override nodetype with child shape
            # end if selection is a transform

            if (nodetype not in self.valid_nodetype()):
                msg = 'Type of selection "%s" not valid with %s' % (s, self)
                return logging.error(msg)
            # end if invalid nodetype selected
            if not pm.objExists('%s.%s' % (s, self)):
                s.addAttr(self, at='bool', dv=1)
            # end if add bool attribute
        # end for iterate current selection
    # end def tag_nodes

    @abstractmethod
    def valid_nodetype(self):
        """Abstract method returning valid io specific node type"""
        pass
    # end def valid_nodetype

    @abstractmethod
    def data(self):
        """Abstract method returning data"""
        pass
    # end def data

    def save(self):
        """Save method of BaseIO."""
        print 'saving', self.data()
    # end def save

    def load(self):
        """Load method of BaseIO."""
        print 'loading', self.data()
    # end def load

    def __repr__(self):
        """Override repr string method to return class name."""
        return self.__class__.__name__
    # end def __repr__
# end class BaseIO
