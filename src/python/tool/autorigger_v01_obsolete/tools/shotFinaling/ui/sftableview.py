"""Created on 2014/02/20
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The table view for the attribute pane.

"""
from PySide import QtCore, QtGui
import sfitemdelegate
reload(sfitemdelegate)


class SFTableView(QtGui.QTableView):
    def __init__(self, parent, macontroller=None):
        """A table view to display the shot finaling sculpts.
        @param parent: the parent of this widget
        @param macontroller: the controller for the interactions with maya
        @note: for some inexplicable reason, itemDelegateForColumn has to be
        called after a setItemDelegateForColumn in order for the latter to work

        """
        super(SFTableView, self).__init__(parent=parent)
        self.setHorizontalHeader(SFHeaderView(QtCore.Qt.Horizontal))
        delegate_static = sfitemdelegate.SFItemStaticDelegate()
        delegate = sfitemdelegate.SFItemDelegate(self, macontroller)
        self.setItemDelegateForColumn(0, delegate)
        self.setItemDelegateForColumn(1, delegate)
        self.setItemDelegateForColumn(2, delegate)
        self.setItemDelegateForColumn(3, delegate)
        self.setItemDelegateForColumn(4, delegate_static)
        self.setItemDelegateForColumn(5, delegate)
        self.setItemDelegateForColumn(6, delegate)
        self.itemDelegateForColumn(0)
        self.itemDelegateForColumn(1)
        self.itemDelegateForColumn(2)
        self.itemDelegateForColumn(3)
        self.itemDelegateForColumn(4)
        self.itemDelegateForColumn(5)
        self.itemDelegateForColumn(6)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
    # end def __init__

    def rowsInserted (self, parent, start, end):
        """Called after a row ha been inserted. Resets the row height and the column size.
        @param parent: the parent
        @param start: the begin of the row insertions
        @param end: the end of the row insertions

        """
        for i in range(start, end+1):
            self.setRowHeight(i, 40)
        # end for i in range(start, end+1)
        self.scale_columns()
    # end def rowsInserted

    def scale_columns(self):
        """Scales the columns to their predefined sizes."""
        self.horizontalHeader().resizeSection(0, 80)
        self.horizontalHeader().resizeSection(1, 40)
        self.horizontalHeader().resizeSection(2, 140)
        self.horizontalHeader().resizeSection(3, 60)
        self.horizontalHeader().resizeSection(4, 60)
        self.horizontalHeader().resizeSection(5, 50)
        self.horizontalHeader().resizeSection(6, 200)
        self.horizontalHeader().setResizeMode(7, QtGui.QHeaderView.Fixed)
        self.horizontalHeader().setResizeMode(7, QtGui.QHeaderView.Stretch)
    # end def scale_columns
# end class AttributeView


class SFHeaderView(QtGui.QHeaderView):
    """The header for the shotfinal table view"""
    def __init__(self, orientation):
        super(SFHeaderView, self).__init__(orientation)
        self.sectionResized.connect(self.resize)
    # end def __init__

    def resize(self, logicalIndex, oldSize, newSize):
        """Resizes the timelines when the timeline column is resized.
        @param logicalIndex: the index of the column
        @param oldSize: the old size of the column
        @param newSize: the new size of the column

        """
        if logicalIndex == 6:
            for row in range(self.model().rowCount()):
                index = self.model().index(row, 6)
                tl = self.parent().indexWidget(index)
                if tl is not None:
                    tl.resize_timeline(newSize)
            # end for row in range(self.model().rowCount())
    # end def resize
# end class SFHeaderView



