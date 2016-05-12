"""
@package: core.interface
@brief: RigInterface implementations of the rig interfaces
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

import string
from abc import ABCMeta


class Meta(ABCMeta):

    """Create Meta class inheriting from ABCMeta, providing abstractmethods."""

    def __init__(self, name, bases, namespace):
        """Initialize Meta class."""
        nodocs = list()
        # check if docstring has been implemented
        for key, value in namespace.items():
            if not hasattr(value, '__call__'):
                continue
            # end if not class or function
            if type(value).__name__ == 'function':
                if not getattr(value, '__doc__'):
                    nodocs.append({self: key})
                # end if no docstring
            # end if value is function
        # end for iterate namespace dictionary
        if nodocs:
            raise TypeError('%s has no docstring! Please implement!' % nodocs)
        # end if nodocs
        type.__init__(self, name, bases, namespace)
    # end def __init__
# end class Meta


class Base(object):

    """Base setting up side and name attributes.

    Integration of custom meta class, which provides abstractmethods and
    docstring existence checks for all the functions.

    """

    __metaclass__ = Meta

    def __init__(self, side, name):
        """Initialize BaseInterface class."""
        # args
        self._side = side
        self._name = name
    # end def __init__

    @property
    def side(self):
        """Read only getter function for side attribute."""
        if self._side is None:
            self._side = 'C'
        # end if side is none
        return self._side
    # end def side

    @side.setter
    def side(self, side):
        """Write only setter function for side attribute."""
        valids = ['C', 'c', 'Center', 'center',
                  'L', 'l', 'Left', 'left',
                  'R', 'r', 'Right', 'right']
        if side not in valids:
            raise ValueError('side is not valid! Valid is %s' % valids)
        # end if side not valid
        self._side = side
    # end def side

    @property
    def name(self):
        """Read only getter function for name attribute."""
        if self._name is None:
            self._name = self.__class__.__name__
        # end if name is none
        return self._name
    # end def name

    @name.setter
    def name(self, name):
        """Write only setter function for name attribute."""
        if [n for n in name if n in string.punctuation]:
            raise ValueError('name contains invalid characters %s' % name)
        # end if name has invalid characters
        self._name = name
    # end def name
# end class Base
