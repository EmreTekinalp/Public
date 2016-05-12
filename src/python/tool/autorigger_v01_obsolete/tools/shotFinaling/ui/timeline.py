"""Created on 2014/02/21
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: Widget that displays a maya timeline with buttons as keys.

"""
import shiboken
from PySide import QtCore, QtGui
from maya import cmds, OpenMayaUI
import dlayout
import dbutton


class Timeline(QtGui.QWidget):
    """Creates an interactive timeline.
    @todo: implement moving the keyframe buttons

    """
    def __init__(self, parent=None, table=None, item=None):
        super(Timeline, self).__init__(parent)
        self.table = table
        self.item = item
        self.dragged_element = None
        self.setAcceptDrops(True)
        self.cursor_position = None
        self.set_variables()
        self.init_timeline()
    # end def __init__

    def set_variables(self):
        """Sets the variables for the timeline."""
        self.timeline_height = 38
        self.btn_width = 4
        self.btn_top = 1
        self.buttons = list()
        self.frames = list()
    # end def set_variables

    def init_timeline(self):
        """Initializes the timeline widget.
        * sets the layout
        * adds a maya timeport to the widget

        """
        self.setLayout(dlayout.DragSupportLayout())
        cmds.window()
        cmds.columnLayout()
        tp = cmds.timePort(bgc=(0.45, 0.45, 0.45), gt=True)
        tp_ptr = OpenMayaUI.MQtUtil.findControl(tp)
        self.timeport = shiboken.wrapInstance(long(tp_ptr), QtGui.QWidget)
        self.layout().addWidget(self.timeport)
        self.timeport.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        for i in range(self.item.rowCount()):
            key = self.item.child(i).data(QtCore.Qt.DisplayRole)
            self.create_timeline_button(key)
        # end for i in range(self.item.rows())
    # end def init_timeline

    def create_timeline_button(self, frame):
        """Creates a timeline button at the given frame.
        @param frame: the frame where the button is to be added

        """
        btn = dbutton.DraggableButton(frame=frame, timeline=self)
        self.place_button(btn)
        self.layout().addWidget(btn)
        self.buttons.append(btn)
    # end def create_timeline_button

    def refresh_buttons(self, animcurve):
        """Refreshes all the buttons in the timeline and checks if they have been
        moved or deleted.
        @param animcurve: the animcurve on which to check for keyframes

        """
        new_keys = list()
        for key in range(animcurve.numKeys()):
            key_exists = self.item.find_keyframe(int(animcurve.time(key).value()))
            if key_exists is None:
                self.create_timeline_button(int(animcurve.time(key).value()))
            new_keys.append(int(animcurve.time(key).value()))
        # end for key in range(animcurve.numKeys())
        for btn in self.buttons:
            if btn.frame not in new_keys:
                self.remove_timeline_button(btn)
        # end for btn in self.buttons
    # end def refresh_buttons

    def remove_timeline_button(self, btn):
        """Removes the given timeline button and remove the item, holding the
        keyframe, from the item of the timeline.
        @param btn: the button that shall be deleted

        """
        self.item.remove_keyframe(btn.frame)
        index = self.buttons.index(btn)
        self.buttons.pop(index)
        btn.deleteLater()
        btn.setParent(None)
    # end def remove_timeline_button

    def place_button(self, btn):
        """Places the given button on the correct place of the timeline.
        @param btn: the button to be placed

        """
        x = self.get_frame_x_value(btn.frame)
        btn.setGeometry(x, self.btn_top, self.btn_width, self.timeline_height)
    # end def place_button

    def resize_timeline(self, width):
        """Resizes the timeline and recalculates the positions for the keyframe buttons.
        @param width: the new width of the timeline

        """
        self.resize(width, self.timeline_height)
        self.setMinimumHeight(self.timeline_height)
        self.timeport.resize(width, self.timeline_height)
        self.timeport.setMinimumWidth(width)
        for btn in self.buttons:
            self.place_button(btn)
        # end for btn in self.buttons
    # end def resize_timeline

    def get_frame_x_value(self, frame):
        """Returns the x position value of the given frame.
        @param frame: the frame to calculate the x value for
        @return: the x value of the given frame

        """
        keyspace = self.get_keyspace()
        start_frame = frame - cmds.playbackOptions(q=True, minTime=True)
        return int((start_frame * keyspace) + 5)
    # end def get_frame_x_value

    def get_next_full_frame(self, pos):
        """Returns the next integer number of the given position.
        @param pos: the position
        @return: the full integer value of the given position

        """
        keyspace = self.get_keyspace()
        frame = int(pos.x() / keyspace)
        return cmds.playbackOptions(q=True, minTime=True) + frame
    # end def get_next_full_frame

    def get_keyspace(self):
        """Returns the space between the keys.
        @return: the space between the keys

        """
        start = cmds.playbackOptions(q=True, minTime=True)
        end = cmds.playbackOptions(q=True, maxTime=True)
        total_keys = end - start
        width = self.geometry().width() - 5
        return width / (total_keys + 1)
    # end def get_keyspace

    def set_dragged_element(self, dragged_element):
        """Sets the currently dragged element
        @param dragged_element: the currently dragged element
        @type dragged_element: QWidget
        @todo: implement drag/drop feature

        """
        self.dragged_element = dragged_element
    # end def set_dragged_button

    def dropEvent(self, event):
        """Handles the drop event and places the currently active element at
        the drop position.
        @param event: the drop event
        @todo: implement drag/drop feature

        """
        self.cursor_position = event.pos()
    # end def dropEvent

    def dragEnterEvent(self, event):
        """Accepts the drag event.
        @param event: the drop event
        @todo: implement drag/drop feature

        """
        event.accept()
    # end def dragEnterEvent
# end class Timeline
