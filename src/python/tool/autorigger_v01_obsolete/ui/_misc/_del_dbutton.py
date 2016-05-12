"""
Created on 17.09.2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: A draggable PySide button.
"""

from PySide import QtGui, QtCore
import dwidget, nodebackdrop


class DraggableButton(QtGui.QToolButton):
    """Custom QToolButton that can be dragged and dropped.
    @param spawn_offspring: specifies whether the button shall be duplicated on drag.
    @type spawn_offspring: Boolean
    @todo: add right click menu
    @todo: add icon
    """
    def __init__(self, spawn_offspring=True):
        super(DraggableButton, self).__init__()
        self.spawn_offspring = spawn_offspring
        self.mouse_offset = None
    # end def __init__

    def mouseMoveEvent(self, event):
        """#################################################################"""
        if event.buttons() != QtCore.Qt.MiddleButton:
            return
        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        dropAction = drag.start(QtCore.Qt.CopyAction)
    # end def mouseMoveEvent
# end class DraggableButton
