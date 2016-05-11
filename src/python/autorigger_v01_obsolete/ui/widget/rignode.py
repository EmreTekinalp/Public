"""Created on 2014/01/25
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The graphic representation of a node
"""

from PySide import QtGui, QtCore

import node
import textnode
reload(textnode)


class RigNode(node.Node, QtGui.QGraphicsItem):
    """A graphic node.
    @todo: get rid of stupid misplacement
    @todo: deal with nodegroups
    @todo: add functionality for corresponding maya object
    @todo: change hooks dict to hooks in data
    @todo: set node functionality to a manager class
    @todo: render lines scale independantly
    @todo: get render values from the model
    @todo: correctly calculate the boundingRect
    @todo: use Flags when doing things like connections and the sort

    """
    def __init__(self, model):
        super(RigNode, self).__init__(model)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable|QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        ti = textnode.TextNode(model=model, parent=self)
    # end def __init__

    def boundingRect(self):
        """@todo: insert doc for boundingRect"""
        size = 20 / self.scene().views()[0].matrix().m11()
        return QtCore.QRectF(0, 0, size, size)
    # end def boundingRect

    def paint(self, painter, option, widget):
        """Paints the node
        @todo: put into NodeShape class
        @todo: take line width into account

        """
        painter = self.get_painter(painter)
        painter.drawPath(self.shape())
    # end def paint

    def get_painter(self, painter):
        """Sets the style of the node either to active or to inactive."""
        linew = 3 / self.scene().views()[0].matrix().m11()
        pen = QtGui.QPen(QtGui.QColor(255, 240, 249), linew)
        brush = QtGui.QBrush(QtGui.QColor(255, 223, 60))
        painter.setPen(pen)
        painter.setBrush(brush)
        return painter
    # end def get_painter

    def shape(self):
        """Returns the shape of the node."""
        size = 20 / self.scene().views()[0].matrix().m11()
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, size, size)
        return path
    # end def shape

    def update(self):
        """@todo: insert doc for mouseReleaseEvent"""
        self.scene().views()[0].nativeParentWidget().nodedatamanager.attribute_changed(1, 'tx', self.scenePos().x(), self.model)
        self.scene().views()[0].nativeParentWidget().nodedatamanager.attribute_changed(1, 'ty', self.scenePos().y(), self.model)
        self.has_changed = False
    # end def mouseReleaseEvent

    def itemChange(self, change, value):
        """@todo: check if left/right changed when autoleft is on"""
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            self.has_changed = True
        return QtGui.QGraphicsItem.itemChange(self, change, value)
    # end def mouseMoveEvent
# end class RigNode
