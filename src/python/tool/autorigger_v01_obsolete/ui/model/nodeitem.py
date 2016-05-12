"""Created on 2014/01/16
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The item for the node editor's model/view setup; subclassed from
        QtGui.QStandardItem.

"""
from PySide import QtCore, QtGui


class NodeItem(QtGui.QStandardItem):
    """@todo: docstring for NodeDataModelItem"""
    def __init__(self, visible=True, editable=True, min=None, max=None, guide=False, mayachange=False):
        super(NodeItem, self).__init__()
        self.datadict = dict()
        self.visible = visible
        self.editable = editable
        self.min = min
        self.max = max
        self.guide = guide
        self.mayachange = mayachange
    # end def __init__

    def type(self):
        """Returns a custom type identifier."""
        return QtGui.QStandardItem().type() + 1
    # end def type

    def set_all_data(self, data):
        """Convenience method to set all data roles at once with the
        same data.

        """
        self.setData(data, QtCore.Qt.DisplayRole)
        self.setData(data, QtCore.Qt.EditRole)
        self.setData(data, QtCore.Qt.UserRole)
        self.setData(data, QtCore.Qt.ToolTipRole)
        self.setData(data, QtCore.Qt.StatusTipRole)
        self.setData(data, QtCore.Qt.WhatsThisRole)
    # end def set_all_data

    def setData(self, data, role=QtCore.Qt.UserRole, exclusive=False):
        """Sets the item's data for the given role to the specified value"""
        self.datadict[role.__int__()] = data
        if role.__int__() == QtCore.Qt.DisplayRole.__int__() and exclusive==False:
            self.datadict[QtCore.Qt.EditRole.__int__()] = data
        if role.__int__() == QtCore.Qt.EditRole.__int__() and exclusive==False:
            self.datadict[QtCore.Qt.DisplayRole.__int__()] = data
        self.emitDataChanged()
    # end def setData

    def data(self, role=QtCore.Qt.UserRole):
        """Returns the item's data for the given role, or an invalid
        PySide.QtCore.QVariant if there is no data for the role.

        """
        if role.__int__() in self.datadict.keys():
            return self.datadict[role.__int__()]
        else:
            return None
    # end def data
# end class NodeItem
