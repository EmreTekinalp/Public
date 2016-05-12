'''
Created on Aug 23, 2015

@author: Emre
'''

from src.python.core import interface
reload(interface)


class Arm(interface.RigInterface):

    """Arm class"""

    def __init__(self, side=None, name=None):
        """Class constructor function."""
        super(Arm, self).__init__(side, name)
    # end def __init__

    def guide(self):
        """Create guide"""
        print '%s guide' % self.name
    # end def guide

    def puppet(self):
        """Create puppet"""
        print '%s puppet' % self.name
    # end def puppet
# end class Arm
