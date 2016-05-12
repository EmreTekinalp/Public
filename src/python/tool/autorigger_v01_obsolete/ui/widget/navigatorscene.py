"""Created on 2014/01/19
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: QGraphicsScene used in the navigator
"""

from PySide import QtCore, QtGui


class NavigatorScene(QtGui.QGraphicsScene):
    """@todo: insert doc for NavigatorScene
    @todo: accept drops
    @todo: bring mayas camera view inside the graphics view
    @todo: use states in the scene:
        * inactive state
        * connect state
        * pan state
        * zoom state
        * translate state
        * rotate state
        * menu state
        * display info on hovering over node clicking permanently

    """
    def __init__(self):
        super(NavigatorScene, self).__init__()
        self.selectionChanged.connect(self.selection_changed)
        self.init_drawing()
    # end def __init__

    def init_drawing(self):
        """@todo: construct the pixmap from scratch without the jpg.
        @todo: provide different sizes and resolutions of the pixmap and connect them to different scale factors

        """
        pixmap_left = QtGui.QPixmap('C:\PROJECTS\AutoRigger\ui\\resource\\pattern_left.jpg')
        pixmap_right = QtGui.QPixmap('C:\PROJECTS\AutoRigger\ui\\resource\\pattern_right.jpg')
        self.brush_left = QtGui.QBrush()
        self.brush_left.setTexture(pixmap_left)
        self.brush_right = QtGui.QBrush()
        self.brush_right.setTexture(pixmap_right)
    # end def init_drawing

    def drawBackground(self, painter, rect):
        """Draws the background.
        The left side of the scene will be drawn red, as it represents the right
        side of the figure.
        The right side will be drawn blue and represents the left side of the
        figure that is to be rigged.
        @todo: provide possibility to switch colors and sides

        """
        # left side
        painter.setPen(QtGui.QColor(0, 0, 0, 0))
        scnrct = self.views()[0].sceneRect()
        x = scnrct.x() if rect.x() > scnrct.x() else rect.x()
        y = scnrct.y() if rect.y() > scnrct.y() else rect.y()
        w = scnrct.width()*0.5 if rect.width()*0.5 < scnrct.width()*0.5 else rect.width()*0.5
        h = scnrct.height() if rect.height() < scnrct.height() else rect.height()
        painter.setBrush(self.brush_left)
        painter.drawRect(x, y, w, h)
        # right side
        x = 0
        painter.setBrush(self.brush_right)
        painter.drawRect(x, y, w, h)
    # end def drawBackground

    def dropEvent(self, event):
        """"""
        rignodes = self.views()[0].nativeParentWidget().create_node(event.mimeData().text())
        for rignode in rignodes:
            if rignode.model.moduletype() != 'compound':
                rignode.moveBy(event.scenePos().x(), event.scenePos().y())



        print 'drop event occured :) at %s / %s with the key: %s' %(event.scenePos().x(), event.scenePos().y(), event.mimeData().text())
        # position = e.pos()
        # self.btn.move(position)
        # e.setDropAction(QtCore.Qt.MoveAction)
        # e.accept()
    # end def dropEvent

    def dragMoveEvent(self, event):
        """@todo: insert doc for dragMoveEvent"""
        # print 'dragMoveEvent occured :) at %s - %s' %(event.scenePos().x(), event.scenePos().y())
    # end def dragMoveEvent

    def mouseReleaseEvent(self, event):
        """"""
        for item in self.selectedItems():
            if item.has_changed:
                item.update()
        # end for item in self.selectedItems()
        QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
    # end def mouseReleaseEvent

    def selection_changed(self):
        """@todo: insert doc for selectionChanged"""
        self.views()[0].nativeParentWidget().nodedatamanager.selection_changed(self.selectedItems())
    # end def selectionChanged
# end class NavigatorScene
