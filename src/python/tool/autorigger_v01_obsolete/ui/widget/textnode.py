"""Created on 2014/02/23
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The graphic representation of a node
"""

from PySide import QtGui, QtCore

import node


class TextNode(node.Node, QtGui.QGraphicsTextItem):
    """@todo: insert doc for TextNode"""
    def __init__(self, model=None, parent=None):
        super(TextNode, self).__init__(model=model)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setParentItem(parent)
        self.setDefaultTextColor(QtGui.QColor(255, 255, 255))
    # end def __init__

    def paint(self, painter, option, widget):
        """Paints the node."""
        font = QtGui.QFont()
        font.setPointSizeF(10 / self.scene().views()[0].matrix().m11())
        self.setFont(font)
        self.setPlainText(self.model.name())
        self.setX(20 / self.scene().views()[0].matrix().m11())
        self.setY(-10 / self.scene().views()[0].matrix().m11())
        return QtGui.QGraphicsTextItem.paint(self, painter, option, widget)
    # end def paint
# end class TextNode
