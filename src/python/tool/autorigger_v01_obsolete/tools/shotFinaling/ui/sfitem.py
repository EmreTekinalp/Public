"""Created on 2014/02/20
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Item for the sf model

"""
from PySide import QtCore, QtGui


class SFItem(QtGui.QStandardItem):
    """The item for the sf model."""
    def __init__(self):
        super(SFItem, self).__init__()
    # end def __init__

    def type(self):
        """Returns a custom type identifier."""
        return QtGui.QStandardItem().type() + 1
    # end def type

    def find_keyframe(self, search_keyframe):
        """Searches the children of this item for the given keyframe.
        @param search_keyframe: The keyframe to be searched for
        @return: the item, holding the keyframe

        """
        return_keyframe = None
        for i in range(self.rowCount()):
            item = self.child(i)
            keyframe = item.data(QtCore.Qt.DisplayRole)
            if keyframe == search_keyframe:
                return_keyframe = item
                break
        # end for i in range(self.rowCount())
        return return_keyframe
     # end def find_keyframe

    def remove_keyframe(self, keyframe):
        """Removes the item, holding the given keyframe.
        @param keyframe: The keyframe to search for

        """
        item = self.find_keyframe(keyframe)
        self.removeRow(item.row())
     # end def remove_keyframe
# end NodeItem
