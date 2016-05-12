"""
@package: brick.control
@brief: Base implementations of the control class
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import pymel.core as pm
from pandoras_box.core import base
from utility.node import node
from utility import storage

reload(base)
reload(storage)


# constants
side = None
master = None


class ControlInterface(base.Base):

    """Core ControlInterface class setting up fundamental control attributes.

    @requires pymel usage is needed. This class is based on pymel only.
    """

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

    def position(self, space='world'):
        """Return worldSpace position values."""
        return self._transform.getTranslation(space)
    # end def position

    def rotation(self, space='world'):
        """Return worldSpace rotation values."""
        return self._transform.getRotation(space)
    # end def rotation
# end class ControlInterface


class Control(ControlInterface):

    """
    Control class inheriting BaseInterface which returns a control object.
    """

    def __init__(self, name=None, size=1, shape=1, orientation=0,
                  offset=[0, 0, 0], color=None, gimbal=True, annotation=True):
        """Initialize Control class.

        @DONE check if args[0] is class object!
        """
        # args
        self.side = side
        self.name = name
        self.master = master
        # vars
        self.gimbal = None
        self.buffer = list()
        self.control_type = 'locator'
        self._storage = list()

        # methods
        self._create(name=name, size=size, shape=shape, orientation=orientation,
                     offset=offset, color=color, gimbal=gimbal,
                     annotation=annotation)
    # end def __init__

    def _create(self, name=None, size=1, shape=1, orientation=0,
                offset=[0, 0, 0], color=None, gimbal=True, annotation=True):
        """Create a control object."""
        if self.control_type == 'locator':
            self._locator(name=name, size=size, shape=shape,
                          orientation=orientation, offset=offset,
                          color=color, gimbal=gimbal, annotation=annotation)
        # end if create locator control
    # end def create

    def _locator(self, name=None, size=1, shape=1, orientation=0,
                  offset=[0, 0, 0], color=None, gimbal=True, annotation=True):
        """Create and return a locator based control shape."""
        node.suffix = 'CTL'
        self.shape = node.locator(name)
        self.group = node.group(name)
        self.transform = self.shape.getParent()

        if gimbal:
            self.gimbal = storage.Cache()
            gimbalname = 'gimbal'
            if name:
                gimbalname = '%sGimbal' % name
            # end if
            node.suffix = 'CTL'
            self.gimbal.shape = node.locator(gimbalname)
            self.gimbal.transform = self.gimbal.shape.getParent()
            self.gimbal.transform.setParent(self.transform)
            self.transform.addAttr('unleashGimbal', at='short', min=0, max=1)
            self.transform.attr('unleashGimbal').set(cb=True)
            self.transform.attr('unleashGimbal') >> self.gimbal.shape.v
        # end if gimbal

        self.transform.setParent(self.group)
        self.shape.ove.set(1)

        if not self.shape.ovc.get():
            if not color:
                self.shape.ovc.set(self._get_color())
            else:
                self.shape.ovc.set(color)
            # end if no color given
        # end if no color specified

        if annotation:
            self._annotation(self.transform)
        # end if annotation given
    # end def _locator

    def _get_color(self):
        """Based on the given side return the proper maya color."""
        if self.side in ['C', 'c', 'Center', 'center']:
            return 17
        elif self.side in ['L', 'l', 'Left', 'left']:
            return 6
        elif self.side in ['R', 'r', 'Right', 'right']:
            return 13
        # end if return maya color value
    # end def _get_color

    def _annotation(self, name):
        """Implement annotation shape and merge with control shape."""
        self.transform.addAttr('label', at='short', min=0, max=1, dv=0, k=True)
        if self.gimbal:
            ano = pm.annotate(self.gimbal.transform, text=name)
        else:
            ano = pm.annotate(self.transform, text=name)
        # end if gimbal is given
        trn = ano.getParent()
        if '_' in name:
            splitname = '%s' % (name.split('_')[1])
            ano.rename('%s_%s_ANOShape' % (self.side, splitname))
            trn.rename(ano.replace('ANOShape', 'ANO'))
        # end if proper naming convention
        ano.ove.set(1)
        ano.ovdt.set(2)
        trn.tz.set(self.transform.sy.get() * 2)
        if self.gimbal:
            trn.setParent(self.gimbal.transform)
        else:
            trn.setParent(self.transform)
        # end if parent anno transform under control
        self.transform.label >> ano.v
    # end def _annotation

    def add_buffer(self, name=None):
        """Add a buffer transform inbetween the transform and the group."""
        if not self.transform:
            return
        # end if no transform
        index = 0
        if self.buffer:
            index = len(self.buffer)
        # end if buffer list
        if name is None:
            name = '%sBuffer%s' % (self._name, index)
        # end if no name given
        buffer = node.transform(name)
        buffer.t.set(self.transform.getTranslation('world'))
        buffer.r.set(self.transform.getRotation('world'))
        self.transform.setParent(buffer)
        buffer.setParent(self.group)
        if self.buffer:
            buffer.setParent(self.buffer[-1])
        # end if buffer
        self.buffer.append(buffer)
        setattr(self, 'buffer%s' % index, buffer)
    # end def add_buffer

    def tag(self, tag):
        """Add a boolean attribute to the transform of the control."""
        if not pm.objExists('%s.%s' % (self.transform, tag)):
            self.transform.addAttr(tag, at='bool', dv=1)
            self.transform.attr(tag).lock()
        # end if tag not exists
    # end def tag

    def position(self, space='world'):
        """Return worldSpace position values."""
        return self.transform.getTranslation(space)
    # end def position

    def rotation(self, space='world'):
        """Return worldSpace rotation values."""
        return self.transform.getRotation(space)
    # end def rotation

    def __add__(self, other):
        """Override + operator so it is useful in usage with __add__."""
        self._storage += [self, other]
        return self
    # end def __add__

    def __or__(self, other):
        """Override | operator so we can parent the group under the object.

        @DONE Do a type check of the other object and make it more versatile
        """
        if not self._storage:
            if isinstance(other, self.__class__):
                if other.gimbal:
                    self.group.setParent(other.gimbal.transform)
                else:
                    self.group.setParent(other.transform)
                # end if gimbal is given
            else:
                self.group.setParent(other)
            # end if other is control class object
            return
        # end if
        for value in set(self._storage):
            if not value:
                continue
            # end if no value given
            if isinstance(value, self.__class__):
                if isinstance(other, self.__class__):
                    if other.gimbal:
                        value.group.setParent(other.gimbal.transform)
                    else:
                        value.group.setParent(other.transform)
                    # end if gimbal is given
                else:
                    value.group.setParent(other)
                # end if other object / non object
            else:
                if isinstance(other, self.__class__):
                    if other.gimbal:
                        value.setParent(other.gimbal.transform)
                    else:
                        value.setParent(other.transform)
                    # end if gimbal is given
                else:
                    value.setParent(other)
                # end if other object / non object
            # end if value object/ non object
        # end for iterate singleton class
        self._storage = []
    # end def __or__
# end class Control
