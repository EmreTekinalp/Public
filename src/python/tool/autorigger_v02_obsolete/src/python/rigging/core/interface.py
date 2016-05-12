"""
@package: core.interface
@brief: RigInterface implementations of the rig interfaces
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import pymel.core as pm
from rigging.core import base
from abc import abstractmethod
__all__ = ['RigInterface']


class RigInterface(base.Base):

    """Rigging Interface which needs to be subclassed for each rig setup."""

    def __init__(self, side=None, name=None):
        """Class constructor function."""
        super(RigInterface, self).__init__(side, name)
        self.elements = list()
    # end def __init__

    @property
    def element(self):
        """Read only, add a type object as element to the element list."""
        return self.elements
    # end def element

    @element.setter
    def element(self, element):
        """Write only, add a type object as element to the element list."""
        self.__dict__['%s%s' % (element.side.lower(), element.name)] = element
        self.elements.append(element)
    # end def element

    def create_guide(self, elements=None):
        """Create guides from stored elements."""
        if not self.elements:
            if not elements:
                return self.guide()
            # end if elements not given
        # end if elements not given
        for element in self.elements:
            if not element.element:
                element.guide()
            else:
                element.guide()
                self.create_guide(element.element)
            # end if recursively check element
        # for iterate elements
    # end def create_guide

    def create_puppet(self, elements=None):
        """Create puppet from stored elements."""
        if not self.elements:
            if not elements:
                return self.puppet()
            # end if elements not given
        # end if elements not given
        for element in self.elements:
            if not element.element:
                element.puppet()
            else:
                element.puppet()
                self.create_puppet(element.element)
            # end if recursively check elements
        # for iterate elements
    # end def create_puppet

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
        print self.__dict__.keys()
        if attr in self.__dict__.keys():
            print 'YES'
    # end def __getattr__

    def __rshift__(self, child, parent):
        """Override rshift >> operator to connect child to parent."""
        print '%s is connected to %s' % (child, parent)
    # end def __rshift__
# end class RigInterface


class Constructor(RigInterface):

    """Constructor class"""

    def __init__(self, side=None, name=None):
        """Class constructor function."""
        super(Constructor, self).__init__(side, name)
    # end def __init__

    def guide(self):
        """Create guide"""
        print '%s guide' % self.name
    # end def guide

    def puppet(self):
        """Create puppet"""
        print '%s puppet' % self.name
    # end def puppet
# end class Constructor


class ControlInterface(object):

    """Core ControlInterface class setting up fundamental control attributes.

    @requires pymel usage is needed. This class is based on pymel only.

    """

    __metaclass__ = base.Meta

    def __init__(self):
        """Initialize Control class"""
        # vars
        self._shape = None
        self._transform = None
        self._group = None
    # end def __init__

    @property
    def shape(self):
        """Read only getter function of the shape"""
        if not self._shape:
            raise ValueError('Please set a shape first!')
        # end if no shape
        return self._shape
    # end def shape

    @shape.setter
    def shape(self, shape):
        """Write only setter function of the shape"""
        self._shape = shape
    # end def shape

    @property
    def transform(self):
        """Read only getter function of the transform"""
        if not self._transform:
            raise ValueError('Please set a transform first!')
        # end if no transform
        return self._transform
    # end def transform

    @transform.setter
    def transform(self, transform):
        """Write only setter function of the transform"""
        self._transform = transform
    # end def transform

    @property
    def group(self):
        """Read only getter function of the group"""
        if not self._group:
            raise ValueError('Please set a group first!')
        # end if no group
        return self._group
    # end def group

    @group.setter
    def group(self, group):
        """Write only setter function of the group"""
        self._group = group
    # end def group

    def tag(self, tag):
        """Add a boolean attribute to the transform of the control."""
        if not pm.objExists('%s.%s' % (self._transform, tag)):
            self._transform.addAttr(tag, at='bool', dv=1)
            self._transform.attr(tag).lock()
        # end if tag not exists
    # end def tag

    def position(self, space='world'):
        """Return worldSpace position values."""
        return self._transform.getTranslation(space)
    # end def position

    def rotation(self, space='world'):
        """Return worldSpace rotation values."""
        return self._transform.getRotation(space)
    # end def rotation
# end class ControlInterface
