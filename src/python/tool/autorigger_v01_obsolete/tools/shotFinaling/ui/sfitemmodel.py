"""Created on 2014/02/20
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The data model for shotfinaling items

"""
from PySide import QtCore, QtGui


class SFItemModel(QtGui.QStandardItemModel):
    """The data model for shotfinaling items."""
    def __init__(self):
        super(SFItemModel, self).__init__()
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels(['Name',
                                       'Keys',
                                       'Blend Value',
                                       'Visibility',
                                       'Frame',
                                       'Remove',
                                       'Timeline',
                                       ''])
    # end def __init__

    def name(self, row):
        """Returns the name of the sculpt by retrieving the item data of the first
        column of the given row.
        @param row: the row from where to retrieve the name
        @return: the name of the sculpt

        """
        return self.item(row, 0).data(QtCore.Qt.DisplayRole)
    # end def name
# end class NodeItemModel
