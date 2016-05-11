from PySide import QtGui, QtCore
from goe_misc.backups import attributedelegate



class AttributeTable(QtGui.QTableView):
    
    def __init__(self):
        delegate = attributedelegate.AttributeDelegate()
        self.setItemDelegate(delegate)
        