"""Created on 2014/01/25
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The graphic representation of a node

"""
from PySide import QtGui, QtCore
import node


class CompoundNode(node.Node, QtGui.QGraphicsPathItem):
    """@todo: insert doc for CompoundNode"""
    def __init__(self, model):
        super(CompoundNode, self).__init__(model)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.inner_nodes = list()
        self.setZValue(0)
        self.setPath(self.shape())
    # end def __init__

    def add_inner_node(self, node):
        """"""
        self.inner_nodes.append(node)
    # end def add_inner_node

    def remove_inner_node(self, node):
        """"""
        self.inner_nodes.remove(node)
    # end def remove_inner_node

    def boundingRect(self):
        """@todo: insert doc for boundingRect"""
        r = QtGui.QGraphicsPathItem.boundingRect(self)
        d = 20 / self.scene().views()[0].matrix().m11()
        return QtCore.QRect(r.x()-d, r.y()-d, r.width()+(d*2), r.height()+(d*2))
    # end def boundingRect

    def paint(self, painter, option, widget):
        """Paints the node
        @todo: put into NodeShape class
        @todo: take line width into account

        """
        linew = 20 / self.scene().views()[0].matrix().m11()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(255, 159, 0))
        pen.setWidth(linew)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.setPen(pen)
        self.setPath(self.shape())
        painter.setPen(pen)
        return QtGui.QGraphicsPathItem.paint(self, painter, option, widget)
    # end def paint

    def shape(self):
        """Returns the shape of the node."""
        path = QtGui.QPainterPath()
        if len(self.inner_nodes) == 0:
            path.addRect(0, 0, 0, 0)
            return path
        for i, innode in enumerate(self.inner_nodes):
            if i == 0:
                start = innode
            else:
                path.addPath(self.add_path(start, innode))
                start = innode
        # end for i, innode in enumerate(self.inner_nodes)
        return path
    # end def shape

    def add_path(self, start, end):
        """@todo: insert doc for add_rect"""
        path = QtGui.QPainterPath()
        path.moveTo(self.get_center(start))
        path.lineTo(self.get_center(end))
        return path
    # end def add_rect

    def get_center(self, item):
        """@todo: insert doc for get_btm_left"""
        pos = item.scenePos()
        br = item.boundingRect()
        x = pos.x() + (br.topRight().x() * 0.5)
        y = pos.y() + (br.bottomRight().y() * 0.5)
        return QtCore.QPointF(x, y)
    # end def get_btm_left

    def get_btm_left(self, item):
        """@todo: insert doc for get_btm_left"""
        pos = item.scenePos()
        y = pos.y() + item.boundingRect().bottomLeft().y()
        return QtCore.QPointF(pos.x(), y)
    # end def get_btm_left

    def get_btm_right(self, item):
        """@todo: insert doc for get_btm_left"""
        pos = item.scenePos()
        br = item.boundingRect()
        x = pos.x() + br.bottomRight().x()
        y = pos.y() + br.bottomRight().y()
        return QtCore.QPointF(x, y)
    # end def get_btm_left

    def get_top_left(self, item):
        """@todo: insert doc for get_btm_left"""
        pos = item.scenePos()
        return QtCore.QPointF(pos.x(), pos.y())
    # end def get_btm_left
# end class CompoundNode
