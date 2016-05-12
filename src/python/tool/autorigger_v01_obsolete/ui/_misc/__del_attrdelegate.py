"""
Created on 11.21.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The attr delegate"""

from PySide import QtCore, QtGui

"""NOT USED ???"""


class AttrDelegate(QtGui.QStyledItemDelegate):
    """docstring for AttrDelegate"""
    def __init__(self, parent):
        super(AttrDelegate, self).__init__(parent)
        self.setItemEditorFactory(QtGui.QItemEditorFactory())
    # end def __init__

    def paint(self, painter, option, index):
        """"""
        # self.combo = QtGui.QComboBox(self.parent())
        # self.connect(self.combo, QtCore.SIGNAL("currentIndexChanged(int)"), self.parent().currentItemChanged)
        if index.column() == 0:
            return QtGui.QStyledItemDelegate.paint(self, painter, option, index)
        if index.column() == 1:
            item = index.model().item(index.row(), 0)
            data = item.data()
            datatype = type(data)
            factory = self.itemEditorFactory().defaultFactory()
            editor = factory.createEditor(datatype, self.parent())
            self.init_data(editor, datatype, data)
            if not self.parent().indexWidget(index):
                self.parent().setIndexWidget(index, editor)
            return QtGui.QStyledItemDelegate.paint(self, painter, option, index)
    # end def paint

    def init_data(self, editor, datatype, data):
        """"""
        if isinstance(data, int) or isinstance(data, float):
            editor.setValue(data)
        elif isinstance(data, basestring):
            editor.setText(data)
    # end def init_data
# end AttrDelegate



class ListEditor(QtGui.QItemEditorCreatorBase):
    def __init__(self):
        super(ListEditor, self).__init__()
    # end def __init__

    def createWidget(self, parent):
        print 'ffff'
        return QtGui.QPushButton(parent=parent)

    def valuePropertyName(self):
        print 'rrrrr'

# end class ListEditor
