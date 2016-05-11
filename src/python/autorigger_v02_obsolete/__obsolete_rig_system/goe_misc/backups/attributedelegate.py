'''
Created on Nov 1, 2014

@author: Emre
'''


from PySide import QtGui, QtCore



class AttributeDelegate(QtGui.QStyledItemDelegate):
    
    def __init__(self, parent=None):
        super(AttributeDelegate, self).__init__(parent)
        
        
        
        
        
    def paint(self, painter, option, index):
        
        if self.parent().indexWidget(index) is None:
            
            item = index.model().itemFromIndex(index)
            
            # item.locked
            
            value = index.model().itemFromIndex(index).data(QtCore.Qt.UserRole)
            
            if isinstance(value, int):
                cbx = QtGui.QLabel(str(value))
                self.parent().setIndexWidget(index, cbx)
            
            else:
                return QtGui.QStyledItemDelegate.paint(self, painter, option, index)