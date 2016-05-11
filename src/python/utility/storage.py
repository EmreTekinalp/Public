"""
@package: utility.storage
@brief: Storage module containing object oriented datahandling tools
@author: Emre Tekinalp
@contact: e.tekinalp@icloud.com
"""


class Cache(object):

    """Generic storage, allocation and retrieving class for any kind of data"""

    def __init__(self):
        """Initialize Cache class object."""
        pass
    # end def __init__

    def __setattr__(self, attr, value):
        """Override set attribute to store dynamically created attributes."""
        self.__dict__[attr] = value
    # end def __setattr__

    def __getattr__(self, attr):
        """Override get attribute to store dynamically created attributes."""
        if attr not in self.__dict__.keys():
            raise ValueError('Cache: please create attribute %s' % attr)
        # end if attr not existt
        return self.__dict__[attr]
    # end def __setattr__
# end class Cache
