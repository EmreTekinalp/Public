"""
@package: construct.generic.primitive
@brief: Base implementations of a primitive rig setup
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import pymel.core as pm
from pandoras_box.core import interface
from utility.node import node
from pandoras_box.brick.control import Control

reload(interface)


class Basic(interface.RigInterface):

    """Create a basic rig setup for general usage."""

    def __init__(self, side=None, name=None):
        """Initialize Basic class."""
        super(Basic, self).__init__()

        self.side = side
        self.name = name
    # end def __init__

    def guide(self):
        """Setup guide."""
        node.transform('Guide')
        Control('GuideBla')
    # end def guide

    def puppet(self):
        """Setup puppet."""
        node.transform('Puppet')
#         print 'puppet', self.side, self.name
    # end def puppet
# end class Basic
