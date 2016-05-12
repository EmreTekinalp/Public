'''
Created on Aug 23, 2015

@author: Emre
'''

from src.python.core import interface


class Spine(interface.RigInterface):

    """Spine class"""

    def __init__(self, side=None, name=None):
        """Class constructor function."""
        super(Spine, self).__init__(side, name)
    # end def __init__

    def guide(self):
        """Create guide"""
        print '%s guide' % self.name
    # end def guide

    def puppet(self):
        """Create puppet"""
        print '%s puppet' % self.name
    # end def puppet
# end class Spine
