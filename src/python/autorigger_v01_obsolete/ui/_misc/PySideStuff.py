#! /opt/maya/2013.2.0/bin/mayapy

import os
import sys
#PySide import
sys.path.append('/CINE/repository/lib/python/pyside/1.1.2-qt4.6.2-cpython2.6.4/centos-6_x86-64_gcc4.4.7/lib/python2.6/site-packages')


#os.environ['LD_LIBRARY_PATH'] = '/CINE/repository/lib/python/pyside/1.1.2-qt4.6.2-cpython2.6.4/centos-6_x86-64_gcc4.4.7/lib'
#os.environ['PYTHON_PATH'] = '/CINE/repository/lib/python/site-packages/2.6/centos-6_x86-64'

#os.environ['LD_LIBRARY_PATH'] = #"$PYSIDESANDBOXPATH/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
#os.environ['PKG_CONFIG_PATH'] = '/CINE/repository/lib/python/pyside/1.1.2-qt4.6.2-cpython2.6.4/centos-6_x86-64_gcc4.4.7/lib/pkgconfig'


import PySide
from PySide import QtGui, QtCore


from PySide import QtGui, QtCore

sys.path.append('/home/schweipa/local/workspace/test')
from pysideanim import *
reload(dbutton)
reload(dwidget)


ui_filepath = os.path.join('/home/schweipa/local/workspace/test', 'demo.ui')
form_class, base_class = convenience.load_ui_type(ui_filepath)


class PySideDemo(base_class, form_class):
    """This displays a pyside window inside maya. Needs a .ui file from the qt
    designer.
    """
    def __init__(self, parent=None):
        super(PySideDemo, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry(2400, 100, 400, 300)
        self.eventfilter = EventFilter(self)
        self.installEventFilter(self.eventfilter)
        self.graphicsscene()
    # end def __init__

    def graphicsscene(self):
        # Create some test nodes
        main_node = Node()
        mid_node = Node()
        end_node = Node()
        nodes = [main_node, mid_node, end_node]

        scene = QtGui.QGraphicsScene()#self.setup_graphics_scene()
        for i, n in enumerate(nodes):
            scene.addItem(n)
        # end for i, n in enumerate(nodes)
        main_node.add_output(mid_node)
        main_node.add_output(end_node)
        mid_node.add_input(main_node)
        mid_node.add_output(end_node)
        end_node.add_input(mid_node)
        end_node.add_input(main_node)
        end_node.add_output(main_node)

        self.graphics_view.setScene(scene)
        self.graphics_view.show()
        # install the event filter
        #self.graphics_view.installEventFilter(self.eventfilter)
        #scene.installEventFilter(self.eventfilter)
    # emd def graphicsscene

    def setup_graphics_scene(self):
        """Sets up the graphics scene for the graphics view."""
        scene = NodeGraphicsScene()
        return scene
    # end def setup_graphics_scene
# end class PySideDemo()


class NodeGraphicsScene(QtGui.QGraphicsScene):
    """Sets up the graphics scene for the graphics view.
    @todo: set scene rect
    @todo: accept drops

    """
    def __init__(self):
        super(NodeGraphicsScene, self).__init__()
        self.setStickyFocus(True)
    # end def __init__
# end class NodeGraphicsScene


class Node(QtGui.QGraphicsRectItem):
    """Provides a node for the node backdrop.
    @todo: continuously redrawing
    @todo: provide different styles

    """
    def __init__(self, shape='circle', size=30):
        super(Node, self).__init__()
        self.setRect(0, 0, size, size)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.input = list()
        self.output = list()
        self.connections = list()
    # end def __init__

    def add_input(self, widget):
        """Adds an input node widget."""
        self.input.append(widget)
    # end def set_input

    def get_input(self):
        """Returns all input node widgets."""
        return self.input
    # end def get_input

    def add_output(self, widget):
        """Adds an ouptut node widget."""
        self.output.append(widget)
        self.add_connection(widget)
    # end def set_output

    def get_output(self):
        """Returns """
        return self.output
    # end def get_output

    def get_connections(self):
        """Returns """
        return self.connections
    # end def get_output

    def get_lines(self):
        """#################################################################"""
        lines = list()
        start_x = self.sceneBoundingRect().x() + (self.sceneBoundingRect().width() / 2)
        start_y = self.sceneBoundingRect().y() + (self.sceneBoundingRect().height() / 2)
        start = QtCore.QPoint(start_x, start_y)
        for node in self.get_input() + self.get_output():
            end_x = node.boundingRect().x() + (node.boundingRect().width() / 2)
            end_y = node.boundingRect().y() + (node.boundingRect().height() / 2)
            end = QtCore.QPoint(end_x, end_y)
            ln = QtCore.QLineF(start, end)
            lines.append(ln)
        return lines
    # end def get_lines

    def add_connection(self, node):
        """#################################################################"""
        connection = NodeConnection()
        self.connections.append((connection, node))
        path = self.calculate_path(connection, node)
        connection.setPath(path)
        self.scene().addItem(connection)
    # end def add_connection

    def remove_connection(self, connection):
        """#################################################################"""
        pass
    # end def remove_connection

    def calculate_path(self, connection, node):
        """#################################################################"""
        start_x = self.sceneBoundingRect().x() + (self.sceneBoundingRect().width() / 2)
        start_y = self.sceneBoundingRect().y() + (self.sceneBoundingRect().height() / 2)
        start = QtCore.QPointF(start_x, start_y)
        end_x = node.pos().x() + (node.boundingRect().width() / 2)
        end_y = node.pos().y() + (node.boundingRect().height() / 2)
        end = QtCore.QPointF(end_x, end_y)
        painterpath = QtGui.QPainterPath()
        painterpath.moveTo(start)
        painterpath.cubicTo(start, end, end)
        return painterpath
    # end def calculate_path
# end class Node


class NodeConnection(QtGui.QGraphicsPathItem):
    def __init__(self):
        """#################################################################"""
        super(NodeConnection, self).__init__()
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
    # end def __init__
# end class NodeConnection


class EventFilter(QtCore.QObject):
    def __init__(self, obj):
        """#################################################################"""
        super(EventFilter, self).__init__(obj)
        self.master = obj
    # end def __init__

    def eventFilter(self, obj, event):
        """#################################################################"""
        if event.type() == QtCore.QEvent.GraphicsSceneWheel:
            self.wheel_event(event)
            return True
        elif event.type() == QtCore.QEvent.HoverMove:
            self.paint(event)
            return True
        else:
            return QtCore.QObject.eventFilter(self, obj, event)
    # end def eventFilter

    def wheel_event(self, event):
        """#################################################################"""
        delta = event.delta()
        orientation = event.orientation()
        self.master.graphics_view.scale(1 - 0.001*delta, 1 -0.001*delta)
    # end def wheel_event

    def paint(self, event):
        """#################################################################"""
        scene = self.master.graphics_view.scene()
        for item in scene.items():
            try:
                for connection in item.get_connections():
                    path = item.calculate_path(connection[0], connection[1])
                    connection[0].setPath(path)
                    scene.update(scene.sceneRect())
            except:
                pass
    # end def paint
# end class EventFilter


def main():
    global my_win
    try:
        my_win.close()
    except:
        pass
    my_win = PySideDemo()
    my_win.show()


main()
