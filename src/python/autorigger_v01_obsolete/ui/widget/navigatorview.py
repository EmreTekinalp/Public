"""Created on 2014/01/19
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: QGraphicsView used for the navigator
"""

import math
from PySide import QtGui, QtCore
import navigatorscene
reload(navigatorscene)


class NavigatorView(QtGui.QGraphicsView):
    """
    states:
        0: default, user has not touched the view
        1: view is being moved
        2: view is being scaled
        3: items are being dragged
    @todo: give a possibility to expand the sceneRect
    @todo: maybe only use True/False test instead of states???

    """
    def __init__(self, parent=None):
        super(NavigatorView, self).__init__(parent=parent)
        self.setScene(navigatorscene.NavigatorScene())
        self.STATE = 0
        self.prev_translate = QtCore.QPointF()
        self.scale_factor = 0.2
        self.scale_view(0.7)
    # end def __init__

    def keyPressEvent(self, event):
        """@todo: insert doc for keyPressEvent"""
        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            self.scale_view(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.scale_view(1 / 1.2)
        else:
            return QtGui.QGraphicsView.keyPressEvent(event)
    # end def keyPressEvent

    def mousePressEvent(self, event):
        """@todo: insert doc for mousePressEvent"""
        if event.button() == QtCore.Qt.MouseButton.MiddleButton:
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            self.STATE = 1
            event = self.fake_left_mouse_button_event(event)
        return QtGui.QGraphicsView.mousePressEvent(self, event)
    # end def mousePressEvent

    def fake_left_mouse_button_event(self, event):
        """Constructs an event that simulates that the left mouse button has
        been pressed. This event is used to work around the flaw that, the
        ScrollHandDrag  mode only works with a pressed left mouse button.
        This way any mouse button can trigger the scrolling.

        """
        event = QtGui.QMouseEvent(event.type(), event.pos(),
                                  event.globalPos(), QtCore.Qt.MouseButton.LeftButton,
                                  event.buttons(), event.modifiers())
        return event
    # end def fake_left_mouse_button_event

    def mouseReleaseEvent(self, event):
        """@note: somehow the dragMode has to be set to NoDrag before being set
                  to either RubberBandDrag or ScrollHandDrag.

        """
        if self.STATE == 1:
            self.setCursor(QtCore.Qt.DragMoveCursor)
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            self.STATE = 0
            event = self.fake_left_mouse_button_event(event)
        return QtGui.QGraphicsView.mouseReleaseEvent(self, event)
    # end def mouseReleaseEvent

    def mouseMoveEvent(self, event):
        """@todo: insert doc for mouseMoveEvent"""
        return QtGui.QGraphicsView.mouseMoveEvent(self, event)
    # end def mouseMoveEvent

    def contextMenuEvent(self, event):
        """@todo: insert doc for contextMenuEvent"""
        return QtGui.QGraphicsView.contextMenuEvent(self, event)
    # end def contextMenuEvent

    def wheelEvent(self, event):
        """Scales the view"""
        self.scale_view(math.pow(2.0, event.delta() / 240.0))
        return QtGui.QGraphicsView.wheelEvent(self, event)
    # end def wheelEvent

    def scale_view(self, scale_factor):
        """Scales the view.
        @param scale_factor: How far the view will be scaled

        """
        factor = self.matrix().scale(scale_factor, scale_factor)
        factor = factor.mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if factor < 0.01 or factor > 10:
            return
        self.scale(scale_factor, scale_factor)
        self.scale_factor = scale_factor
    # end def scale_view
# end class NavigatorView
