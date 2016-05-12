"""
Created on 10/04/2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The NodeGraphicsView for the AutoRigger system.
"""

import math
import os
from PySide import QtGui, QtCore, QtOpenGL
from utility import path
import nodegraphicsscene
reload(nodegraphicsscene)


class NodeGraphicsView(QtGui.QGraphicsView):
    """#####################################################################"""
    def __init__(self):
        super(NodeGraphicsView, self).__init__()
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        scene = nodegraphicsscene.NodeGraphicsScene(QtCore.QRectF(-500, -500, 1000, 1000))
        self.setScene(scene)
        self.scale(0.5, 0.5)
        self.scale_factor = 0.5
    # end def __init__

    def keyPressEvent(self, event):
        """#################################################################"""
        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            self.scaleView(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.scaleView(1 / 1.2)
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)
    # end def keyPressEvent

    def mousePressEvent(self, event):
        """#################################################################"""
        if event.button() == QtCore.Qt.MouseButton.MiddleButton:
            print 'todo: Enter translate mode.'
        return QtGui.QGraphicsView.mousePressEvent(self, event)
    # end def mousePressEvent

    def wheelEvent(self, event):
        """#################################################################"""
        self.scale_view(math.pow(2.0, event.delta() / 240.0))
    # end def wheelEvent

    def drawBackground(self, painter, rect):
        """#################################################################"""
        bg_img = QtGui.QPixmap(os.path.join(path.Path().resource(),
                               'navigator_bg.jpg'))
        return
        #print self.scene().sceneRect().width(), rect.width()

        w = rect.width()
        h = rect.height()
        x = rect.x()
        y = rect.y()
        # add_width = self.scene().sceneRect().width() - w
        # if add_width > 0:
        #     w += add_width
        # add_height = self.scene().sceneRect().height() - h
        # if add_height > 0:
        #     h += add_height
        bg_img = bg_img.scaled(w, h)


        # if rect.width() < self.scene().sceneRect().width():
        #     dx = (self.scene().sceneRect().width() - rect.width())
        #     print dx


        painter.drawPixmap(x, y, bg_img)

    # end def drawBackground

    def scale_view(self, scale_factor):
        """#################################################################"""
        factor = self.matrix().scale(scale_factor, scale_factor)
        factor = factor.mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if factor < 0.01 or factor > 2:
            return
        self.scale(scale_factor, scale_factor)
        self.scale_factor = factor
    # end def scale_view
# end class NodeGraphicsView
