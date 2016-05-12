"""
@package: construct.constructor
@brief: Assembly class to construct several rig objects
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""

from pandoras_box.core import interface
reload(interface)


class Constructor(interface.RigInterface):

    """Constructor class"""

    def __init__(self):
        """Class constructor function."""
        super(Constructor, self).__init__()
    # end def __init__

    def guide(self):
        """Create guide"""
        pass
    # end def guide

    def puppet(self):
        """Create puppet"""
        pass
    # end def puppet
# end class Constructor
