"""Created on 01/24/2014
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: A draggable button
"""

from PySide import QtGui, QtCore


class DButton(QtGui.QPushButton):
    """Custom QToolButton that can be dragged and dropped.
    @param spawn_offspring: specifies whether the button shall be duplicated on drag.
    @type spawn_offspring: Boolean
    @todo: add right click menu
    @todo: add icon
    """
    def __init__(self, parent=None, rigmodule=None):
        super(DButton, self).__init__()
        self.rigmodule = rigmodule
    # end def __init__

    def mouseMoveEvent(self, event):
        """@todo: insert doc for mouseMoveEvent"""
        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        mimeData.setText(self.rigmodule)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        dropAction = drag.start(QtCore.Qt.MoveAction)
    # end def mouseMoveEvent
# end class DButton
