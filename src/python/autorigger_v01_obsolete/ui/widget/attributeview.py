"""Created on 2014/01/18
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The table view for the attribute pane.

"""
from PySide import QtCore, QtGui
from model import nodeitemdelegate
reload(nodeitemdelegate)


class AttributeView(QtGui.QTableView):
    """The table view for the attribute pane."""
    def __init__(self, parent):
        """@note: for some inexplicable reason, itemDelegateForColumn has to be
        called after a setItemDelegateForColumn in order for the latter to work

        """
        super(AttributeView, self).__init__(parent=parent)
        delegate = nodeitemdelegate.NodeItemDelegate(self)
        self.setItemDelegateForColumn(0, delegate)
        self.setItemDelegateForColumn(1, delegate)
        self.itemDelegateForColumn(0)
        self.itemDelegateForColumn(1)
    # end def __init__
# end class AttributeView


