"""Created on 11.21.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Custom item delegate for node items

"""
from functools import partial
from PySide import QtCore, QtGui
from widget import rignode, compoundnode
import nodeitemmodel
import enum
reload(enum)


class NodeItemDelegate(QtGui.QStyledItemDelegate):
    """The QStyledItemDelegate for the node items."""
    def __init__(self, parent=None):
        super(NodeItemDelegate, self).__init__(parent)
    # end def __init__

    def paint(self, painter, option, index):
        """A button will be drawn or RigNodes and CompoundNodes."""
        # Hide the row if the item is set to invisible
        if not index.model().itemFromIndex(index).visible:
            if not self.parent().isRowHidden(index.row()):
                self.parent().setRowHidden(index.row(), True)
            return
        elif (isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), rignode.RigNode) or
              isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), compoundnode.CompoundNode)):
            if self.parent().indexWidget(index) is None:
                btn = QtGui.QToolButton()
                btn.setText(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole).model.name())
                btn.clicked.connect(partial(self.select_item, index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), index))
                self.parent().setIndexWidget(index, btn)
        elif isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), bool):
            if self.parent().indexWidget(index) is None:
                cbx = QtGui.QCheckBox()
                cbx.setChecked(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole))
                cbx.stateChanged.connect(partial(self.set_bool_data, cbx, index.model(), index))
                self.parent().setIndexWidget(index, cbx)
        else:
            return QtGui.QStyledItemDelegate.paint(self, painter, option, index)
    # end def paint

    def createEditor(self, parent, option, index):
        """Creates a special editor for list items"""
        # the name of the attribute
        if index.column() == 0:
            return
        elif isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), enum.Enum):
            return QtGui.QComboBox(parent=parent)
        elif isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), bool):
            cbx = QtGui.QCheckBox(parent=parent)
            return cbx
        elif isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), list):
            lineedit = QtGui.QLineEdit(parent=parent)
            return lineedit
        else:
            return QtGui.QStyledItemDelegate.createEditor(self, parent, option, index)
    # end def createEditor

    def select_item(self, item, index):
        """Selects the given item."""
        item.scene().clearSelection()
        item.setSelected(True)
    # end def select_item

    def setEditorData(self, editor, index):
        """Checks the data type of the item. If it is a list, the editor is set
        to display the item's Qt.DisplayRole as the current item in the comboBox.
        For all other data types, the normal behavior is returned.

        """
        if isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), enum.Enum):
            values = index.model().data(index, QtCore.Qt.UserRole).values
            for value in values:
                editor.addItem(value)
            # end for value in values
            current = index.model().data(index, QtCore.Qt.UserRole).current_index
            editor.setCurrentIndex(current)
        elif isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), list):
            editor.setText(index.model().itemFromIndex(index).data(QtCore.Qt.DisplayRole))
        else:
            return QtGui.QStyledItemDelegate.setEditorData(QtGui.QStyledItemDelegate(), editor, index)
    # end def setEditorData

    def setModelData(self, editor, model, index):
        """Checks the data type of the item. If it is a list, the item's
        Qt.DisplayRole is set to the  current text of the comboBox.
        For all other data types, the normal behavior is returned.

        """
        if isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), enum.Enum):
            current_text = editor.currentText()
            item = model.itemFromIndex(index)
            item.data(QtCore.Qt.UserRole).set_current(current_text)
            item.setData(current_text, QtCore.Qt.DisplayRole, exclusive=True)
        elif isinstance(index.model().itemFromIndex(index).data(QtCore.Qt.UserRole), list):
            text = eval(editor.text())
            item = model.itemFromIndex(index)
            item.setData(text, QtCore.Qt.UserRole)
            item.setData(str(text), QtCore.Qt.DisplayRole, exclusive=True)
        else:
            return QtGui.QStyledItemDelegate.setModelData(QtGui.QStyledItemDelegate(),
                                                          editor, model, index)
    # end def setModelData

    def set_bool_data(self, editor, model, index, state):
        """Sets the data for boolean values."""
        checked = editor.isChecked()
        item = model.itemFromIndex(index)
        item.setData(checked, QtCore.Qt.UserRole)
        item.setData(checked, QtCore.Qt.DisplayRole)
    # end def set_bool_data

    def data_type(self, data):
        pass
    # end def data_type
# end NodeItemDelegate
