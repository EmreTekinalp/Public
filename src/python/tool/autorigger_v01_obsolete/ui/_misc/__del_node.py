"""
Created on 20.09.2013
@author: Paul Schweizer
"""
import math
from functools import partial
from PySide import QtGui, QtCore
from ui.manager import attributemanager
import qtutils
reload(attributemanager)
reload(qtutils)


class Node(object):
    """A basic node object from which all other nodes are inheriting.
    @todo: check this data.nodes.append(self), and maybe put that into model

    """
    def __init__(self, data):
        super(Node, self).__init__()
        self.data = data
        data.nodes.append(self)
    # end def __init__
# end class Node


class RigNode(Node, QtGui.QGraphicsItem):
    """A node object.
    @param data: The data object, that holds all the informations for the
                 object, the node represents
    @todo: get rid of stupid misplacement
    @todo: deal with nodegroups
    @todo: add functionality for corresponding maya object
    @todo: change hooks dict to hooks in data

    """
    def __init__(self, data, autorigger, nodegroup=None):
        super(RigNode, self).__init__(data)
        self.nodegroup = nodegroup
        self.hooks = {'inhook': list(), 'outhook': list()}
        self.connections = list()
        self.setPos(self.data.get_attr('tx').data(QtCore.Qt.DisplayRole),
                    self.data.get_attr('ty').data(QtCore.Qt.DisplayRole))
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptsHoverEvents(True)
        self.setZValue(0)
        self.ar = autorigger
        self.data.itemChanged.connect(partial(self.ar.attr_manager.change_event,
                                      'datamodel'))
    # end def __init__

    def remove_hook(self, hook, node):
        """Removes the given node in the given hook side.
        @todo: get rid of hook dict and solve it with the data object instead
        """
        parent = self.data.get_attr(hook, column='name')
        items = parent.findItems(node, role=QtCore.Qt.UserRole)
        if len(items) == 0:
            return False
        item = items[0]
        item.parent().takeRow(item.row())
        if node in self.hooks[hook]:
            self.hooks[hook].remove(node)
            return True
    # end def remove_hook

    def add_hook(self, node, hook):
        """Hooks up the given node to the given hook side of this node."""
        if not self.check_node(node):
            return False
        hookattr = self.data.get_attr(hook, column='name')
        index = hookattr.rowCount()
        attr = '%s%s' % (hook, index)
        self.data.add_attr(attr, hookattr)
        self.data.set_attr(attr, node)
        self.hooks[hook].append(node)
        return True
    # end def add_hook

    def add_connection(self, node, locked=True):
        """Adds a connection between this node and the given node."""
        connection = NodeConnection(self.data, self, node, locked)
        self.connections.append(connection)
        self.scene().addItem(connection)
    # end def add_connection

    def remove_connection(self, connected_node, force=False):
        """Removes a connection"""
        for i, connection in enumerate(self.connections):
            if connection.end is connected_node:
                if not connection.locked or force:
                    self.scene().removeItem(connection)
                    self.connections.pop(i)
                    return True
        # end for i, connection in enumerate(self.connections)
        return False
    # end def remove_connection

    def check_node(self, node):
        """Checks if the node can be added as in or output to this node."""
        status = True
        for hook, hooknodes in self.hooks.iteritems():
            for hooknode in hooknodes:
                if node is hooknode:
                    print 'already in hooks'
                    status = False
                    break
        if node is self:
            print 'node is self'
            status = False
        return status
    # end def check_node

    def get_painter(self, painter):
        """Sets the style of the node either to active or to inactive."""
        outline_color = self.data.get_attr('outline_color').data(QtCore.Qt.DisplayRole)
        fill_color = self.data.get_attr('fill_color').data(QtCore.Qt.DisplayRole)
        stroke_width = self.data.get_attr('stroke_width').data(QtCore.Qt.DisplayRole)
        if self.isSelected():
            pen = QtGui.QPen(qtutils.get_color(outline_color, 'active'), stroke_width)
            brush = QtGui.QBrush(qtutils.get_color(fill_color, 'active'))
        else:
            pen = QtGui.QPen(qtutils.get_color(outline_color, 'inactive'), stroke_width)
            brush = QtGui.QBrush(qtutils.get_color(fill_color, 'inactive'))
        painter.setPen(pen)
        painter.setBrush(brush)
        return painter
    # end def get_painter

    def boundingRect(self):
        """Returns the bounding rect of the node."""
        try:
            size = self.data.get_attr('size').data(QtCore.Qt.DisplayRole)
        except Exception as err:
            print err
            print self.data.get_attr('name').data()
            print self.data.rowCount()
        size = 30
        return QtCore.QRectF(0, 0, size, size)
    # end def boundingRect

    def shape(self):
        """Returns the shape of the node."""
        path = QtGui.QPainterPath()
        shape = self.data.get_attr('shape').data(QtCore.Qt.DisplayRole)
        size = self.data.get_attr('size').data(QtCore.Qt.DisplayRole)
        if shape == 'circle':
            path.addEllipse(0, 0, size, size)
        return path
    # end def shape

    def paint(self, painter, option, widget):
        """Paints the node
        @todo: put into NodeShape class
        @todo: take line width into account

        """
        self.match_to_grid()
        painter = self.get_painter(painter)
        painter.drawPath(self.shape())
    # end def paint


    def match_to_grid(self):
        """@todo: insert doc for match_to_grid"""
        try:
            x = self.round_to_value(self.pos().x())
            y = self.round_to_value(self.pos().y())
            self.setX(x)
            self.setY(y)
            #node.data.set_attr('tx', x)
            #node.data.set_attr('ty', y)
            #print node.pos().x()
        except:
            pass
        # end for node in selected
    # end def match_to_grid

    def round_to_value(self, number, roundto=50):
        return (round(number / roundto) * roundto)


    def itemChange(self, change, value):
        """@todo: connect to attribute manager for the distribution of the changes."""
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            if self.scene() is None:
                return QtGui.QGraphicsItem.itemChange(self, change, value)
            self.ar.attr_manager.change_event('navigator', self)
        return QtGui.QGraphicsItem.itemChange(self, change, value)
    # end def itemChange

    def set_node_group(self, nodegroup):
        """Sets the corresponding node group for this node.
        @todo: implement model functionality here
        @todo: use itemgroup

        """
        self.nodegroup = nodegroup
    # end def set_node_group
# end class RigNode


class MouseNode(RigNode):
    """The mousenode represents the mousepointer when the user drags a
    connection from one node to another.
    It gets deleted on mouse release.

    """
    def __init__(self, data, autorigger):
        super(MouseNode, self).__init__(data, autorigger)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)
        self.setEnabled(False)
    # end def __init__
# end class MouseNode


class NodeConnection(Node, QtGui.QGraphicsLineItem):
    """@todo: solve position and stuff via data model queries."""
    def __init__(self, data, start, end, locked=True):
        super(NodeConnection, self).__init__(data)
        self.data = data
        self.start = start
        self.end = end
        self.locked = locked
        if not locked:
            self.unlock_connection()
        self.arrowHead = QtGui.QPolygonF()
    # end def __init__

    def lock_connection(self):
        """Locks the connection so it can't be deleted by the user."""
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)
        self.locked = True
    # end def lock_connection

    def unlock_connection(self):
        """Unlocks the connection so it can be deleted by the user."""
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.locked = False
    # end def unlock_connection

    def get_painter(self, painter):
        """Sets the style of the node connection either to active or to inactive."""
        color = self.data.get_attr('connection_color').data(QtCore.Qt.DisplayRole)
        strokesize = self.data.get_attr('connection_strokesize').data(QtCore.Qt.DisplayRole)
        if self.isSelected():
            pen = QtGui.QPen(qtutils.get_color(color, 'active'), strokesize*2)
            brush = QtGui.QBrush(qtutils.get_color(color, 'active'))
        else:
            pen = QtGui.QPen(qtutils.get_color(color, 'inactive'), strokesize)
            brush = QtGui.QBrush(qtutils.get_color(color, 'inactive'))
        painter.setPen(pen)
        painter.setBrush(brush)
        return painter
    # end def get_painter

    def shape(self):
        """Returns the shape."""
        path = QtGui.QGraphicsLineItem.shape(self)
        path.addPolygon(self.arrowHead)
        return path
    # end def shape

    def update_position(self):
        """Updates the line when the position of the start and end node
        are changed.
        @todo: rename to update_line
        @todo: implement model

        """
        line = QtCore.QLineF(self.get_pos(self.start), self.get_pos(self.end))
        self.setLine(line)
    # end def update_position

    def get_pos(self, pos):
        """Returns the position of the given position item.
        @todo: implement model

        """
        if pos is None:
            return self.views()[0].mapFromGlobal(QtGui.QCursor.pos())
        else:
            return self.mapFromItem(pos, 0, 0)
    # end def get_pos

    def paint(self, painter, option, widget=None):
        """Paints the node connection.
        @todo: get rid of arrow size, put it in model

        """
        arrow_size = 10.0
        self.get_painter(painter)
        p1 = self.get_center_point(self.end)
        p2 = self.get_center_point(self.start)
        line = QtCore.QLineF(p1, p2)
        line.setLength(line.length() - self.start.sceneBoundingRect().width() / 2)
        p1 = line.p2()
        p2 = line.p1()
        line = QtCore.QLineF(p1, p2)
        line.setLength(line.length() - self.end.sceneBoundingRect().width() / 2)
        p1 = line.p2()
        p2 = line.p1()
        line = QtCore.QLineF(p1, p2)
        self.setLine(line)

        angle = 0
        if self.line().length() != 0:
            angle = math.acos(self.line().dx() / self.line().length())
        if self.line().dy() >= 0:
            angle = (math.pi * 2.0) - angle
        arrowP1 = self.line().p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrow_size,
                                                    math.cos(angle + math.pi / 3.0) * arrow_size)
        arrowP2 = self.line().p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrow_size,
                                                    math.cos(angle + math.pi - math.pi / 3.0) * arrow_size)
        self.arrowHead.clear()
        for point in [self.line().p1(), arrowP1, arrowP2]:
            self.arrowHead.append(point)

        painter.drawLine(self.line())
        painter.drawPolygon(self.arrowHead)
    # end def paint

    def get_center_point(self, node):
        """Returns the center point of the given node.
        @todo: maybe move this method to the node

        """
        pntx = node.pos().x() + (node.sceneBoundingRect().width() / 2)
        pnty = node.pos().y() + (node.sceneBoundingRect().height() / 2)
        return QtCore.QPointF(pntx, pnty)
    # end def get_center_point
# end class NodeConnection


class NodeGroup(Node, QtGui.QGraphicsItemGroup):
    """
    """
    def __init__(self, data):
        super(NodeGroup, self).__init__(data)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
    # end def __init__
# end class NodeGroup
