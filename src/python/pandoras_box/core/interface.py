"""
@package: core.interface
@brief: RigInterface implementations of the rig interfaces
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import pymel.core as pm
from pandoras_box.core import base
from abc import abstractmethod
from utility.node import node
from pandoras_box.brick import control
__all__ = ['RigInterface']

reload(control)
reload(base)


# constants
STAGE_ASSET_LOAD = 0
STAGE_GUIDE = 1
STAGE_GUIDE_LOAD = 2
STAGE_PUPPET = 3
STAGE_FINALIZE = 4



class RigInterface(base.Base):

    """Rigging Interface which needs to be subclassed for each rig setup."""

    def __init__(self):
        """Class constructor function."""

        # private vars
        self._elements = list()
    # end def __init__

    @property
    def element(self):
        """Read only, add a type object as element to the element list."""
        return self._elements
    # end def element

    @element.setter
    def element(self, element):
        """Write only, add a type object as element to the element list."""
        self.__dict__['%s%s' % (element.side.lower(), element.name)] = element
        self._elements.append(element)
    # end def add_element

    def construct(self, STAGE):
        """Construct rig setup."""
        self.load_asset()
        if STAGE:
            self.create_guide()
        if STAGE >= 2:
            self.load_guide_data()
        if STAGE >= 3:
            self.create_puppet()
            self.load_skinweights()
        if STAGE == 4:
            self.finalize()
    # end def construct

    def load_asset(self):
        """Load by importing the asset into the scene."""
        pass
    # end def load_asset

    def create_guide(self):
        """Create guide"""
        for element in self._elements:
            if element.element:
                element.construct(STAGE_GUIDE)
            # end if create construct
            control.master = element
            node.master = element
            element.guide()
        # end for iterate elements
    # end def create_guide

    def load_guide_data(self):
        """Load asset guide data from file."""
        pass
    # end def load_guide_data

    def create_puppet(self):
        """Create puppet from stored elements."""
        for element in self._elements:
            if element.element:
                element.construct(STAGE_PUPPET)
            # end if create construct
            control.master = element
            node.master = element
            element.puppet()
        # end for iterate elements
    # end def create_puppet

    def load_skinweights(self):
        """Load asset skinweights data from file."""
        pass
    # end def load_skinweights

    def finalize(self):
        """Setup finale touches and make rig publish ready."""
        pass
    # end def finalize

    @abstractmethod
    def guide(self):
        """Abstract method which needs to be implemented when subclassed."""
        pass
    # end def guide

    @abstractmethod
    def puppet(self):
        """Abstract method which needs to be implemented when subclassed."""
        pass
    # end def puppet

    def __getattr__(self, attr):
        """Override getattr function"""
        if attr in self.__dict__.keys():
            print 'YES'
    # end def __getattr__

    def __rshift__(self, child, parent):
        """Override rshift >> operator to connect child to parent."""
        print '%s is connected to %s' % (child, parent)
    # end def __rshift__
# end class RigInterface
