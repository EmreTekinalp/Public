"""Created on 2014/02/23
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: An enum attribute for the attribute view

"""


class Enum():
    """@todo: insert doc for Enum"""
    def __init__(self, values=list()):
        self.values = values
        self.current_value = None
        self.current_index = None
    # end def __init__

    def set_current(self, value):
        """@todo: insert doc for set_current"""
        self.current_value = self.values[self.values.index(value)]
        self.current_index = self.values.index(value)
    # end def set_current
# end class Enum
