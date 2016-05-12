"""Created on 2014/01/18
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: A line edit for the model/view framework
"""
from PySide import QtCore, QtGui


class MVLineEdit(QtGui.QLineEdit):
    """A line edit for the model/view framework. Works only in conjunction with
    a NodeItemModel model.

    """
    def __init__(self, parent):
        super(MVLineEdit, self).__init__(parent=parent)
        self.editingFinished.connect(self.text_edited)
        self.model = None
        self.item = None
    # end def __init__

    def set_model(self, model, item):
        """@todo: insert doc for set_model"""
        self.model = model
        self.item = item
        self.model.add_view(self)
        self.setText(item.data())
    # end def set_model

    def unset_model(self):
        """@todo: insert doc for this def"""
        self.model.remove_view(self)
        self.model = None
        self.item = None
        self.setText('')
    # end def unset_model

    def text_edited(self):
        """@todo: insert doc for textEdited"""
        text = self.text()
        self.item.setData(text, QtCore.Qt.DisplayRole)
        self.item.setData(text, QtCore.Qt.UserRole)
    # end def text_edited

    def update(self):
        """@todo: insert doc for update"""
        self.setText(self.item.data(QtCore.Qt.DisplayRole))
    # end def update
# end class MVLineEdit
