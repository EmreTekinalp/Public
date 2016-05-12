"""
Created on 11.18.2013
@author: Paul
"""
import os
from utility import path
from PySide import QtGui, QtCore


class Background(QtGui.QGraphicsRectItem):
    def __init__(self):
        super(Background, self).__init__()
        self.setRect(-1000, -1000, 2000, 2000)
        self.setEnabled(False)
        self.setActive(False)
        self.setZValue(-1)
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        self.bg_img = QtGui.QPixmap(os.path.join(path.Path().resource(), 'navigator_bg.jpg'))
    # end def __init__

    def paint(self, painter, option, widget):
        """Paints the background
        """
        painter.drawPixmap(-1000, -1000, self.bg_img)
    # end def paint
# end class Background
