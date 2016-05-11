"""
Created on 10/04/2013
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The custom graphics scene for the node system.
"""

from math import ceil
from functools import partial
from PySide import QtCore, QtGui
<<<<<<< HEAD
from ui.qtcustom import node, background, nodeconnection
=======
from ui.qtcustom import node, background, circlemenu
>>>>>>> fdc29ac57b3e705bd9bf3661cb340f2b59f7968d
from ui.manager import nodefactory
from utility import datareader, constants
reload(nodefactory)
reload(datareader)
reload(constants)
reload(node)
reload(background)
reload(circlemenu)


class NodeGraphicsScene(QtGui.QGraphicsScene):
    """Sets up the graphics scene for the graphics view.
    @todo: accept drops
    @todo: use states in the scene:
        * inactive state
        * connect state
        * pan state
        * zoom state
        * translate state
        * rotate state
        * menu state
        * display info on hovering over node clicking permanently
    @todo: use nodegroups
    @todo: bring mayas camera view inside the graphics view

    """
    def __init__(self, sceneRect):
        super(NodeGraphicsScene, self).__init__(sceneRect)
        self.setStickyFocus(True)
        self.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.mousenode = None
        self.state = constants.INACTIVE_STATE
    # end def __init__

    def add_items(self, items):
        """Adds the given items to this graphicsscene."""
        for item in items:
            self.addItem(item)
        # end for item in items
    # end def add_items

    def mousePressEvent(self, event):
        """The mouse press event decides if it should generate a mousenode under
        the current mouse position.
        @todo: if mouse moves outside node, create a mousenode
        @todo: if no mousenode and item under mouse, select this item
        @todo: more behaviour like yEd!!!

        """
        if event.button() is not QtCore.Qt.MouseButton.LeftButton:
            self.open_menu(event)
            return QtGui.QGraphicsScene.mousePressEvent(self, event)
        sel_items = self.selectedItems()
        item_at = self.itemAt(event.scenePos().x(), event.scenePos().y())
        if (len(sel_items) == 0 and item_at is not None and
            type(item_at) is not background.Background):
            self.add_mousenode(event)
        return QtGui.QGraphicsScene.mousePressEvent(self, event)
    # end def mousePressEvent

    def mouseReleaseEvent(self, event):
        """If a mousenode is active, it gets released.
        @todo: more behaviour like yEd!!!

        """
        if event.button() is not QtCore.Qt.MouseButton.LeftButton:
            return False
        if self.mousenode is not None:
            self.remove_mousenode(event)
        return QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
    # end def mouseReleaseEvent

    def contextMenuEvent(self, event):
        """"""
        self.open_menu(event)
    # end def contextMenuEvent

    def open_menu(self, event):
        """"""

        ########################################################################
        # self.state = constants.MENU_STATE
        # wid = QtGui.QWidget()
        # wid.setLayout(QtGui.QVBoxLayout())
        # btn = QtGui.QPushButton('gggggg')
        # wid.layout().addWidget(btn)

        # wid.setAutoFillBackground(False)

        # wid.move(event.scenePos().x(), event.scenePos().y())

        # wid.layout().setContentsMargins(50, 50, 50, 50)

        # proxy = self.addWidget(wid)

        # print proxy
        # proxy.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # proxy.setWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)
        # proxy.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        # #(QtCore.Qt.)

        # wid.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # #wid.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        # m = circlemenu.CircleMenu()
        # m.addAction('ggg')


        # btn = QtGui.QPushButton()
        # m.setLayout(QtGui.QHBoxLayout())
        # m.layout().addWidget(btn)
        # m.layout().setContentsMargins(50, 50, 50, 50)
        # m.exec_(QtGui.QCursor.pos())

        # return


        items = self.selectedItems()
        if len(items) == 0:
            return False

        menu = QtGui.QMenu(self.views()[0])

        nodes = self.get_selected_node_items()
        if len(nodes) == 2:
            connect_action = menu.addAction('Connect')
            connect_action.triggered.connect(partial(self.connect_nodes,
                                             nodes[0], nodes[1]))
            disconnect_action = menu.addAction('Disconnect')
            disconnect_action.triggered.connect(partial(self.disconnect_nodes,
                                                nodes[0], nodes[1]))
        delete_action = menu.addAction('Delete')
        delete_action.triggered.connect(partial(self.delete_nodes, items))


        # # QWidget *myWidget = new QWhateverWidget();
        # # myWidget->setAutoFillBackground(false);
        # # QPixmap pixmap = QPixmap::grabWidget(myWidget);
        # # myWidget->setMask(pixmap.createHeuristicMask();


        # btn = QtGui.QPushButton()
        # menu.setLayout(QtGui.QHBoxLayout())
        # menu.layout().addWidget(btn)
        # # menu.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        # # menu.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # menu.setWindowFlags(menu.windowFlags())
        # menu.layout().setContentsMargins(50, 50, 50, 50)
        # #menu.overrideWindowFlags(QtCore.Qt.FramelessWindowHint)
        # #menu.overrideWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)

        # # menu.setAutoFillBackground(False)
        # # pixmap = QtGui.QPixmap().grabWidget(menu)
        # # menu.setMask(pixmap.createHeuristicMask())


        menu.exec_(QtGui.QCursor.pos())
    # end def open_menu

    def connect_nodes(self, src, tgt, locked=False):
        """Connects the two given nodes."""
        if not src.add_hook(tgt, 'inhook'):
            return False
        tgt.add_hook(src, 'outhook')
        tgt.add_connection(src, locked)
        return True
    # end def connect_nodes

    def disconnect_nodes(self, node1, node2, force=False):
        """Disconnects the nodes."""
        removed1 = node1.remove_connection(node2, force)
        removed2 = node2.remove_connection(node1, force)
        if removed1 or removed2:
            node1.remove_hook('outhook', node2)
            node1.remove_hook('inhook', node2)
            node2.remove_hook('outhook', node1)
            node2.remove_hook('inhook', node1)
    # end def disconnect_nodes

    def delete_nodes(self, deletenodes):
        """Deletes the given nodes"""
        if not isinstance(deletenodes, list):
            deletenodes = [deletenodes]
        for deletenode in deletenodes:
            if isinstance(deletenode, node.NodeConnection):
                self.disconnect_nodes(deletenode.start, deletenode.end)
            if isinstance(deletenode, node.RigNode) or isinstance(deletenode, node.MouseNode):
                for hook in ['inhook', 'outhook']:
                    hooks = deletenode.data.get_attr(hook, column='name')
                    for i in range(hooks.rowCount()):
                        hooknode = deletenode.data.get_attr('%s%s' % (hook, i)).data()
                        self.disconnect_nodes(deletenode, hooknode, True)
                    # end for i in range(hooks.rowCount())
                # end for hook in ['inhook', 'outhook']
                self.removeItem(deletenode)
        # end for deletenode in deletenodes
    # end def delete_nodes

    def add_mousenode(self, event):
        """Adds a temporary mousenode and connects it to its source node."""
        self.state = constants.CONNECT_STATE
        x = event.scenePos().x()
        y = event.scenePos().y()
        srcnode = self.itemAt(x, y)
        mousenode = nodefactory.NodeFactory().create_mousenode(srcnode.ar, x, y)
        mousenode.add_hook(srcnode, 'inhook')
        srcnode.add_connection(mousenode, False)
        self.mousenode = mousenode
        self.addItem(self.mousenode)
    # end def add_mousenode

    def remove_mousenode(self, event):
        """Removes the mousenode and either creates a connection and hookup with
        the target node or just removes the mousenode if no valid target node
        can be found under the mouse.

        """
        if self.mousenode is None:
            return
        for item in self.items(event.scenePos()):
            if (item is not self.mousenode and item is not None and
                isinstance(item, node.RigNode)):
                innode = self.mousenode.hooks['inhook'][0]
                self.connect_nodes(item, innode)
                break
        # end for item in self.items(event.scenePos())
        self.delete_nodes(self.mousenode)
        self.mousenode = None
        self.state = constants.INACTIVE_STATE
    # end def remove_mousenode

    def mouseMoveEvent(self, event):
        """The mouse move event places the mousenode to the current mouse
        position, if the mousenode is currently active.

        """
        if self.mousenode is not None:
            self.mousenode.setPos(event.scenePos())
        return QtGui.QGraphicsScene.mouseMoveEvent(self, event)
    # end def mouseMoveEvent

    def get_selected_node_items(self, nodetype=node.RigNode):
        """Returns all selected items of the given type."""
        items = self.selectedItems()
        nodeitems = list()
        for item in items:
            if isinstance(item, nodetype):
                nodeitems.append(item)
        # end for item in items
        return nodeitems
    # end def get_selected_node_items

    def get_non_selected_node_items(self, nodetype=node.RigNode):
        """Returns all selected items of the given type."""
        items = self.selectedItems()
        nodeitems = list()
        non_selected_items = [item for item in self.items() if item not in items]
        for non_selected_item in non_selected_items:
            if isinstance(non_selected_item, nodetype):
                nodeitems.append(non_selected_item)
        # end for non_selected_item in non_selected_items
        return nodeitems
    # end def get_non_selected_node_items
# end class NodeGraphicsScene
