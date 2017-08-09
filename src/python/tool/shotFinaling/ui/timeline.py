import shiboken
from PySide import QtGui
from maya import cmds, OpenMayaUI
import pysideconvenience, dlayout, dbutton, dwidget, uifunctions
reload(pysideconvenience)
reload(dlayout)
reload(dbutton)
reload(dwidget)
reload(uifunctions)


class Timeline():
    """Creates an interactive timeline.
    @todo: move button
    """
    def __init__(self, timeline_layout, parent_widget):
        self.timeline_layout = timeline_layout
        self.parent_widget = parent_widget
        self.uif = uifunctions.UIFunctions()
        self.set_variables()
        self.create_timeline()
    # end def __init__()

    def set_variables(self):
        """Sets the variables of the timeline.
        @todo: maybe provide these as inputs
        """
        self.timeline_height = 32
        self.btn_width = 4
        self.btn_top = 1
        self.buttons = list()
        self.frames = list()
    # end def set_variables()

    def create_timeline(self):
        """Creates a timeline widget."""
        self.timeline = dwidget.DragSupportWidget()
        self.timeline.setLayout(dlayout.DragSupportLayout())
        self.timeline_layout.addWidget(self.timeline)
        cmds.window()
        cmds.columnLayout()
        tp = cmds.timePort(bgc=(0.45, 0.45, 0.45), gt=True)
        tp_ptr = OpenMayaUI.MQtUtil.findControl(tp)
        self.timeport = shiboken.wrapInstance(long(tp_ptr), QtGui.QWidget)
        self.timeline.layout().addWidget(self.timeport)
        self.timeport.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.resize_timeline()
    # end def create_timeline()

    def refresh_buttons(self, animcurve):
        """Refreshes all the buttons in the timeline and checks if they have
        moved or deleted."""
        new_keys = list()
        for key in range(animcurve.numKeys()):
            self.create_timeline_button(int(animcurve.time(key).value()),
                                        'red', animcurve.value(key))
            new_keys.append(int(animcurve.time(key).value()))
        # end for key in range(animcurve.numKeys())
        for btn in self.buttons:
            if btn.frame not in new_keys:
                self.remove_timeline_button(btn)
        # end for btn in self.buttons
    # end def refresh_buttons()

    def create_timeline_button(self, frame, color, value):
        """Creates a timeline button at the given frame."""
        for btn in self.buttons:
            if frame == btn.frame:
                btn.set_stylesheet(value)
        if frame in self.frames:
            return
        self.frames.append(frame)
        btn = dbutton.DraggableButton(frame=frame, timeline=self, color=color,
                                      value=value)
        self.place_button(btn)
        self.timeline.layout().addWidget(btn)
        self.buttons.append(btn)
    # end def create_timeline_button()

    def remove_timeline_button(self, btn):
        """Removes the given timeline button"""
        index = self.buttons.index(btn)
        self.buttons.pop(index)
        btn.deleteLater()
        btn.setParent(None)
    # end def remove_timeline_button()

    def place_button(self, btn):
        """Places the given button on the correct place of the timeline."""
        x = self.get_frame_x_value(btn)
        btn.setGeometry(x, self.btn_top, self.btn_width, self.timeline_height)
    # end def place_button()

    def resize_timeline(self):
        """
        * Resizes the timeline.
        * Recalculates all the positions for all the buttons.
        """
        row, column = self.uif.get_row_column(self.parent_widget)
        width = self.parent_widget.geometry().width() - 20
        height = self.timeline_height
        self.timeline.resize(width, height)
        self.timeline.setMinimumHeight(self.timeline_height)
        self.timeport.resize(width, height)
        self.timeport.setMinimumWidth(width)
        for btn in self.buttons:
            self.place_button(btn)
        # end for btn in self.buttons
    # end def resize_timeline()

    def get_frame_x_value(self, btn):
        """Returns the x position value of the given frame"""
        keyspace = self.get_keyspace()
        start_frame = btn.frame - cmds.playbackOptions(q=True, minTime=True)
        return int((start_frame * keyspace) + 5)
    # end def get_frame_x_value()

    def get_next_full_frame(self, pos):
        """Returns the next full of the given position.
        """
        keyspace = self.get_keyspace()
        frame = int(pos.x() / keyspace)
        return cmds.playbackOptions(q=True, minTime=True) + frame
    # end def get_next_full_frame()

    def get_keyspace(self):
        """Returns the space between the keys."""
        start = cmds.playbackOptions(q=True, minTime=True)
        end = cmds.playbackOptions(q=True, maxTime=True)
        total_keys = end - start
        width = self.timeline.geometry().width() - 5
        return width / (total_keys+1)
    # end def get_keyspace()
# end class Timeline()
