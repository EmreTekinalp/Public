from functools import partial
from PySide import QtGui, QtCore
from maya import cmds
import timeline


class DraggableButton(QtGui.QToolButton):
    """Custom QToolButton that can be dragged and dropped.
    @param frame: the frame, the button represents
    @type frame: int
    @todo: remove frame
    @todo: rework on this

    """
    def __init__(self, frame, timeline, color='red', value=1):
        super(DraggableButton, self).__init__()
        self.frame = frame
        self.timeline = timeline
        self.mouse_offset = None
        self.setAutoRaise(True)
        self.color = color
        self.value = value
        self.set_stylesheet(value)
        self.clicked.connect(partial(self.mouseDoubleClickEvent, None))
        #self.setup_popup_menu()
    # end def __init__()

    def set_stylesheet(self, value):
        """Sets the stylesheet for the button."""
        if self.color == 'green':
            r = 10 + (value * 128)
            g = 120 + (value * 135)
            b = 10 + (value * 128)
            color = 'rgb(%s, %s, %s)' % (r, g, b)
            color_hover = 'rgb(210, 255, 210)'
        if self.color == 'red':
            r = 50 + (value * 205)
            g = 10 + (value * 128)
            b = 10 + (value * 128)
            color = 'rgb(%s, %s, %s)' % (r, g, b)
            color_hover = 'rgb(255, 210, 210)'
        self.setStyleSheet('QToolButton{background-color:%s;}'
                           'QToolButton:hover{border:0; background-color:%s;}'
                           % (color, color_hover))
    # end def set_stylesheet()

    def setup_popup_menu(self):
        """Sets up the popup menu"""
        m = QtGui.QMenu()
        for action in ['Remove']:
            act = m.addAction(action)
            act.triggered.connect(self.remove_frame)
        # end for action in ['Remove', 'GoTo']
        self.setMenu(m)
        self.clicked.connect(self.showMenu)
    # end def setup_popup_menu()

    def remove_frame(self):
        """Removes the frame."""
        print 'todo: remove this frame at %s' % self.frame
    # end def goto()

    def mouseDoubleClickEvent(self, event):
        """The mouse double click event"""
        cmds.currentTime(self.frame)
    # end def mouseDoubleClickEvent()

    def mouseMoveEvent(self, event):
        """The mouse move event."""
        if event.buttons() == QtCore.Qt.RightButton:
            self.showMenu()
            return
        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        dropAction = drag.start(QtCore.Qt.MoveAction)
        self.mouse_offset = event.pos()
        self.place_button()
    # end def mouseMoveEvent()

    def mousePressEvent(self, event):
        """The mouse press event."""
        QtGui.QToolButton.mousePressEvent(self, event)
    # end def mousePressEvent()

    def place_button(self):
        """Places the given button at the current position of the cursor."""
        return
        target_widget = self.get_widget_at_mouse().parent()
        if type(target_widget) != timeline.Timeline:
            return
        pos = target_widget.cursor_position
        self.frame = self.timeline.get_next_full_frame(pos)
        self.timeline.place_button(self)
    # end def place_button()

    def get_focus_widget(self):
        """Get the currently focused widget"""
        return QtGui.qApp.focusWidget()
    # end def get_focus_widget()

    def get_widget_at_mouse(self):
        """Get the widget under the mouse"""
        currentPos = QtGui.QCursor().pos()
        widget = QtGui.qApp.widgetAt(currentPos)
        return widget
    # end def get_widget_at_mouse()
# end class DraggableButton()
