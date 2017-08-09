"""
import sys
sys.path.append('C:\PROJECTS\python\maya\shotFinaling')
import shotfinalingui
reload(shotfinalingui)

shotfinalingui.main()
"""

import os
import sys
import webbrowser
from functools import partial
from PySide import QtGui, QtCore
from maya import cmds, OpenMaya, OpenMayaAnim
sf_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(sf_path)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import SFTOOL02_UPDATE as shotfinaling
reload(shotfinaling)
from shotFinaling.ui import pysideconvenience
from shotFinaling.ui import uifunctions
from shotFinaling.ui import floatslidergroup
from shotFinaling.ui import timeline
from shotFinaling.ui import dwidget
reload(timeline)

uifilepath = os.path.join(os.path.dirname(__file__), 'ui', 'shotfinaling.ui')
form_class, base_class = pysideconvenience.load_ui_type(uifilepath)


class ShotfinalingUI(base_class, form_class):
    """This displays a ui for the shot finaling tools.
    @todo: remove tab when nothing is inside
    @todo: jump from keyframe to keyframe arrows(not important)
    @todo: create a button to activate keyframeAtFrame, which creates one keyFrame
           on the current frame and keyframes on the frame before and after, but they are zeroed out.
    @todo: maybe a button to show timeline, turn it on or off??? Not sure
    """
    def __init__(self, parent=pysideconvenience.get_maya_window()):
        super(ShotfinalingUI, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry(560, 25, 800, 410)
        #self.resize(300, 410)
        self.setup_widgets()
        self.setup_variables()
        if cmds.objExists('SHOTFINALING'):
            self.recreate_engineerstools()
        self.add_callbacks()
    # end def __init__

    def setup_widgets(self):
        """Sets up all widget connections and attributes."""
        self.action_wiki.triggered.connect(self.help)
        self.sf_wid.setLayout(self.sf_vlay)
        self.abc_wid.setLayout(self.abc_vlay)
        self.sf_tabw = self.create_tab_widget()
        self.sf_vlay.insertWidget(0, self.sf_tabw)
        self.sf_btn.clicked.connect(partial(self.switch_content, 'sf'))
        self.sf_btn.setIcon(QtGui.QIcon(":/sculptRelax.png"))
        self.abc_btn.clicked.connect(partial(self.switch_content, 'abc'))
        self.switch_content('sf')
        self.follow_cam_btn.clicked.connect(self.follow_cam)
        self.follow_cam_btn.setIcon(QtGui.QIcon(":/cameraAimUp.png"))
        self.remove_follow_cam_btn.clicked.connect(self.remove_follow_cam)
        self.shot_cam_btn.clicked.connect(self.shot_cam)
        self.shot_cam_btn.setIcon(QtGui.QIcon(":/camera.svg"))
        self.sf_create_btn.clicked.connect(self.create_shot_final)
        self.abc_update_btn.clicked.connect(self.update_alembic)
        self.pan_btn.clicked.connect(self.pan)
        self.pan_btn.setIcon(QtGui.QIcon(":/camPanZoom.png"))
        self.zoom_btn.clicked.connect(self.zoom)
        self.zoom_btn.setIcon(QtGui.QIcon(":/zoom.png"))
        self.reset_pan_zoom_btn.clicked.connect(self.reset_pan_zoom)
        self.reset_pan_zoom_btn.setIcon(QtGui.QIcon(":/menuIconReset.png"))
        # alembic info table
        self.abc_info_twid.setHorizontalHeaderLabels(['current alembics',
                                                      'updated alembics', ''])
        self.abc_info_twid.horizontalHeader().resizeSection(0, 530)
        self.abc_info_twid.horizontalHeader().resizeSection(1, 530)
    # end def setup_widgets

    def setup_variables(self):
        """Sets up general variables."""
        self.column_number = 0
        self.column_name = 1
        self.column_select_button = 2
        self.column_blendvalue = 3
        self.column_visibility = 4
        self.column_frame = 5
        self.column_remove = 6
        self.column_timeline = 7
        self.callback = None
        self.SF = 'SF'
        self.CHAR = 'CHAR'
        self.CTL = 'CTL'
        self.SF_CTL_GRP = 'CTL_GRP'
        self.SF_TOP_GRP = 'SHOTFINALING'
        self.SF_BLS_GRP = 'SF_BLENDSHAPES'
        self.SF_GRP = 'SF_CONTROLS'
        self.SF_TOOLS_TOP_GRP = 'SHOTFINALING_TOOLS'
        self.SF_TOOL_TOP_GRP = 'CTL_GRP'
        self.SF_TOOLS_GRP = 'TOOLS'
        self.SF_TOOL_GRP = 'TOOL'
        self.ENVELOPE = 'ENVELOPE'
        self.tabs = dict()
        self.sculpts = dict()
        self.columns = ['#', 'Name', 'Keys', 'Blend Value', 'Visibility',
                        'Frame', 'Remove', 'Timeline', '']
        self.edit_item_text = None
        self.timelines = list()
        self.uif = uifunctions.UIFunctions()
        self.callbacks = list()
        self.blendvalue_callback_id = None
        self.key_callback_id = None
    # end def setup_variables

    def switch_content(self, content):
        """Switches the contents between shotfinaling and alembic by enabling,
        disabling the widgets and setting their maximum heights.
        @param content: the content to switch to
        @type content: String
        """
        if content == 'sf':
            self.abc_wid.setEnabled(False)
            self.sf_wid.setEnabled(True)
            self.abc_wid.setMaximumHeight(0)
            self.sf_wid.setMaximumHeight(16777215)
        if content == 'abc':
            self.abc_wid.setEnabled(True)
            self.sf_wid.setEnabled(False)
            self.sf_wid.setMaximumHeight(0)
            self.abc_wid.setMaximumHeight(16777215)
            self.check_current_alembic()
    # end def switch_content

    def add_callbacks(self):
        """Adds the on time change callback."""
        self.blendvalue_callback_id = OpenMaya.MDGMessage().addTimeChangeCallback(self.blend_value_callback)
        self.key_callback_id = OpenMayaAnim.MAnimMessage().addAnimKeyframeEditedCallback(self.key_callback)
    # end def add_callback

    def blend_value_callback(self, func, clientData):
        """The function that gets called when the callback is executed on time
        change. It updates the values of the spinboxes according to the
        blendValues of the corresponding sculpts.
        """
        try:
            for grp in cmds.listRelatives(self.SF_GRP, c=True):
                if grp == self.SF_BLS_GRP:
                    continue
                for sf_tool in cmds.listRelatives(grp, c=True):
                    obj_name = sf_tool.split('SF_CHAR_')[1].split('_CTL_GRP')[0]

                    tool_grp = '%s_%s' % (obj_name, self.SF_TOOL_GRP)
                    sf_tool_grp = '%s_%s' % (obj_name, self.SF_TOOL_TOP_GRP)
                    grp = '%s|%s|%s|%s' % (self.SF_TOP_GRP, self.SF_GRP,
                                           sf_tool_grp, tool_grp)
                    table = self.tabs[obj_name][1]
                    sculpts = cmds.listRelatives(sf_tool, c=True)
                    if sculpts is None:
                        continue
                    for sculpt in sculpts:
                        # get the row
                        sculpt = sculpt.split('SF_CHAR_')[1].split('_CTL')[0]
                        item = table.findItems(sculpt, QtCore.Qt.MatchExactly)
                        row = item[0].row()
                        # get the spinbox
                        cellwidget = table.cellWidget(row, self.column_blendvalue)
                        spn = self.get_blend_value_widget(cellwidget,
                                                          QtGui.QDoubleSpinBox)
                        sld = self.get_blend_value_widget(cellwidget, QtGui.QSlider)
                        # get the value
                        trans = self.get_transform_dag_path(obj_name, sculpt)
                        value = cmds.getAttr('%s.blendValue' % trans)
                        spn.valueChanged.disconnect()
                        sld.valueChanged.disconnect()
                        # set the spinbox value
                        spn.setValue(value)
                        sld.setValue(value * float(sld.maximum()))
                        spn.valueChanged.connect(partial(self.change_blend_value,
                                                         spn))
                        spn.valueChanged.connect(partial(self.change_float_slider,
                                                         spn, sld))
                        sld.valueChanged.connect(partial(self.change_float_slider,
                                                         sld, spn))
                    # end for sculpt in sculpts
                # end for obj in cmds.listRelatives(grp, c=True)
            # end for grp in cmds.listRelatives(self.SF_TOP_GRP, c=True)
        except Exception as err:
            print err
    # end def blend_value_callback

    def key_callback(self, attributes, clientData):
        """Everything is put into a try statement for general safety reasons
        @param attributes: edited attributes
        @param clientData: additionalData, not used by the onionSkin, so always
                           defaults to None
        @type clientData: None
        """
        # try:
        for i in range(attributes.length()):
            attribute = attributes[i]
            keyframe_delta = OpenMayaAnim.MFnKeyframeDelta(attribute)
            animcurve = OpenMayaAnim.MFnAnimCurve(keyframe_delta.paramCurve())
            object_name = cmds.listConnections(animcurve.name())[0]
            trans_name = object_name
            obj = None
            for c in cmds.listConnections(object_name):
                if '_BSP' in c:
                    obj = c.split('_BSP')[0].split('CHAR_')[1]
                    break
            if obj is None:
                return
            table = self.tabs[obj][1]
            trans_name = trans_name.split('SF_CHAR_')[1].split('_CTL')[0]
            item = table.findItems(trans_name, QtCore.Qt.MatchExactly)
            key_timeline = None
            for c in table.cellWidget(item[0].row(), self.column_timeline).children():
                if type(c) is dwidget.DragSupportWidget:
                    for tl in self.timelines:
                        if tl.timeline is c:
                            key_timeline = tl
                    # end for tl in self.timelines
            # end for c in table.cellWidget(item[0].row(), self.column_timeline).children()
            if key_timeline is not None:
                key_timeline.refresh_buttons(animcurve)
            # end for key in range(animcurve.numKeys())
        # end for i in range(attributes.length()-1)
        # except Exception as err:
        #     print err
    # end def key_callback

    def get_blend_value_widget(self, cellwidget, comparewidget):
        """Returns the blend value slider from the given cellwidget."""
        returnwidget = None
        for i in range(cellwidget.layout().count()):
            innerwidget = cellwidget.layout().itemAt(i).widget()
            if type(innerwidget) == comparewidget:
                returnwidget = innerwidget
                break
            else:
                if innerwidget.layout() is not None:
                    for j in range(innerwidget.layout().count()):
                        second_innerwidget = innerwidget.layout().itemAt(j).widget()
                        if type(second_innerwidget) == comparewidget:
                            returnwidget = second_innerwidget
                            break
                    # end for j in range(innerwidget.layout().count())
        # end for i in range(cellwidget.layout().count()
        return returnwidget
    # end def get_blend_value_widget

    def update_alembic(self):
        """Updates the alembics in the scene."""
        abc = finaling.AlembicUpdate()
        abc.update()
        self.check_update_alembic()
    # end def update_alembic()

    def check_current_alembic(self):
        """Checks the current alembics and displays infos about them."""
        abc = finaling.AlembicUpdate()
        abc.currentAlembicInfo()
        version = abc.abcNode[0].split('_')[7][1:]
        abc.getLatestAlembics()
        cur_vers = int(abc.abcNode[0].split('_')[7][1:])
        latest_vers = int(abc.latestDir[-3:])
        if cur_vers == latest_vers:
            status = 'Status: Up to date!'
        else:
            status = 'Status: Your Version: %s, Latest Version: %s, Please Update!' % (cur_vers, latest_vers)
        path = os.path.join(abc.alembicPath[0],
                            '%s%s' % (abc.latestDir[:-3], version))
        self.abc_version_lbl.setText('Version: %s' % version)
        self.abc_status_lbl.setText(status)
        self.abc_path_lbl.setText('Path: %s' % path)
        self.abc_folder_btn.clicked.connect(partial(self.open_abc_folder, path))
        rows = self.abc_info_twid.rowCount()
        for i, abc_node in enumerate(abc.abcNode):
            if i >= rows:
                self.abc_info_twid.insertRow(i)
            item = QtGui.QTableWidgetItem(abc_node)
            self.abc_info_twid.setItem(i, 0, item)
        # end for i, abc_node in enumerate(abcNode)
        self.abc_info_lbl.setText('Shot: %s' % abc.shot)
    # end def check_current_alembic

    def check_update_alembic(self):
        """Checks the updated alembics and displays infos about them."""
        abc = finaling.AlembicUpdate()
        abc.updatedAlembicInfo()
        version = 'Version: %s' % abc.latestDir.split("_")[-1][1:]
        status = 'Status: Up to date!'
        path = os.path.join(abc.alembicPath[0], abc.latestDir)
        self.abc_version_lbl.setText(version)
        self.abc_status_lbl.setText(status)
        self.abc_path_lbl.setText('Path: %s' % path)
        self.abc_folder_btn.clicked.connect(partial(self.open_abc_folder, path))

        rows = self.abc_info_twid.rowCount()
        for i, abc_node in enumerate(cmds.ls(type = "AlembicNode")):
            # check were the corresponding alembic resides
            parts = abc_node.split('_')
            upd_abc = '%s_%s_%s_%s_%s_%s_%s' % (parts[0], parts[1], parts[2],
                                                parts[3], parts[4], parts[5],
                                                parts[6])
            row = None
            for j in range(rows):
                parts = self.abc_info_twid.item(j, 0).text().split('_')
                cur_abc = '%s_%s_%s_%s_%s_%s_%s' % (parts[0], parts[1], parts[2],
                                                    parts[3], parts[4], parts[5],
                                                    parts[6])
                if cur_abc == upd_abc:
                    row = j
            # end for j in range(rows)
            if row is None:
                row = self.abc_info_twid.rowCount()
                self.abc_info_twid.insertRow(row)
            item = QtGui.QTableWidgetItem(abc_node)
            self.abc_info_twid.setItem(row, 1, item)
        # end for i, abc_node in enumerate(cmds.ls(type=""AlembicNode))
    # end def check_update_alembic

    def open_abc_folder(self, path):
        """Opens the given folder in a browser window."""
        webbrowser.open(path)
    # end def open_abc_folder

    def follow_cam(self):
        """Calls the follow cam script."""
        follow_cam = finaling.followCam(remove=False)
        cmds.lookThru(follow_cam, 'perspView')
    # end def follow_cam

    def remove_follow_cam(self):
        """Calls the follow cam script to remove the followCam."""
        finaling.followCam(remove=True)
    # end def remove_follow_cam

    def shot_cam(self):
        """Calls the look through left cam script."""
        finaling.lookThroughLeftShotCam()
    # end def shot_cam

    def create_shot_final(self):
        """Creates a new shot finaling sculpt for the selected object.
        * Creates the necessary tabs and table widgets
        * Creates a row in the table widget
        """
        sf = shotfinaling.ShotFinalMain()
        mesh = sf.mesh
        sculpt_tool = '%s%s' % (sf.mesh, sf.target_index)
        if mesh not in self.tabs:
            self.create_object_tab(mesh)
        self.switch_tab(mesh)
        self.add_row(self.tabs[mesh][1], sculpt_tool)
    # end def create_shot_final

    def create_object_tab(self, mesh):
        """Creates a tab for the given mesh."""
        wid = QtGui.QWidget()
        table = self.create_table_widget()
        top_tools = self.create_top_tools(mesh)
        wid.setLayout(QtGui.QVBoxLayout())
        wid.layout().addLayout(top_tools)
        wid.layout().addWidget(table)
        tab = self.create_tab(mesh, self.sf_tabw, wid)
        self.tabs[mesh] = [tab, table]
        self.sf_tabw.setCurrentIndex(tab)
    # end def create_object_tab

    def create_tab_widget(self, parent=None):
        """Creates a tab widget and parents it under the given parent, if a
        parent is given.
        """
        twid = QtGui.QTabWidget()
        if parent is not None:
            parent.addWidget(twid)
        return twid
    # end def create_tab_widget

    def create_tab(self, label, tab_widget, content):
        """Creates a tab in the given tab widget with the given content."""
        return tab_widget.addTab(content, label)
    # end def create_tab

    def create_table_widget(self):
        """Creates a table widget."""
        table = QtGui.QTableWidget(0, len(self.columns))
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.setHorizontalHeaderLabels(self.columns)
        table.horizontalHeader().sectionResized.connect(self.resize_timeline_column)
        table.itemDoubleClicked.connect(self.save_item_state)
        table.itemChanged.connect(self.rename_item)
        table.horizontalHeader().resizeSection(0, 30)
        table.horizontalHeader().resizeSection(1, 80)
        table.horizontalHeader().resizeSection(2, 40)
        table.horizontalHeader().resizeSection(3, 140)
        table.horizontalHeader().resizeSection(4, 60)
        table.horizontalHeader().resizeSection(5, 60)
        table.horizontalHeader().resizeSection(6, 50)
        table.horizontalHeader().resizeSection(7, 200)
        table.horizontalHeader().setResizeMode(6, QtGui.QHeaderView.Fixed)
        table.horizontalHeader().setResizeMode(8, QtGui.QHeaderView.Stretch)
        return table
    # end def create_table_widget

    def resize_timeline_column(self, logicalIndex, oldSize, newSize):
        """Resizes the timeline."""
        if logicalIndex == self.column_timeline:
            for tl in self.timelines:
                tl.resize_timeline()
            # end for tl in self.timelines
    # end def resize_timeline_column

    def create_top_tools(self, mesh):
        """Creates the tools on top of the table.
        * Select object button
        * Envelope slider
        """
        lay = QtGui.QHBoxLayout()
        btn = QtGui.QToolButton()
        btn.setText('Select Original')
        btn.clicked.connect(partial(self.select_object, mesh))
        lbl = QtGui.QLabel('Envelope:')
        fsg = floatslidergroup.FloatSliderGroup()
        fsg.set_minimum(0)
        fsg.set_maximum(1)
        fsg.set_decimals(3)
        fsg.set_value(1)
        fsg.spinbox.valueChanged.connect(partial(self.edit_envelope,
                                                 fsg.spinbox))
        lay.addWidget(btn)
        lay.addWidget(lbl)
        lay.addWidget(fsg)
        lay.addStretch()

        return lay
    # end def create_top_tools

    def add_row(self, table, name, frame=None, checked=True):
        """Adds a new row in the given table.
        * Name
        * Blend value slider
        * Frame number
        * Remove button
        """
        self.disconnect_table_signals(table)
        if frame is None:
            frame = str(int(cmds.currentTime(q=True)))
        # row
        row = table.rowCount()
        table.insertRow(row)
        table.setRowHeight(row, 40)
        # number
        row_number = self.item_text_margined(str(row+1))
        item = QtGui.QTableWidgetItem(row_number)
        table.setItem(row, self.column_number, item)
        # name
        item = QtGui.QTableWidgetItem(name)
        table.setItem(row, self.column_name, item)
        # select button
        select_btn = QtGui.QToolButton()
        select_btn.setText('Show')
        table.setCellWidget(row, self.column_select_button, select_btn)
        select_btn.clicked.connect(partial(self.select_sculpt_transform,
                                           select_btn))
        # slider
        sld_wid = QtGui.QWidget()
        sld_wid.setLayout(QtGui.QHBoxLayout())
        sld_wid.layout().setSpacing(0)
        fsg = floatslidergroup.FloatSliderGroup()
        fsg.set_minimum(0)
        fsg.set_maximum(1)
        fsg.set_decimals(4)
        fsg.set_value(1)
        fsg.setMinimumHeight(36)
        fsg.layout().setSpacing(0)
        fsg.spinbox.valueChanged.connect(partial(self.change_blend_value,
                                                 fsg.spinbox))
        key_btn = QtGui.QToolButton()
        key_btn.setIcon(QtGui.QIcon(":/setKeySmall.png"))
        key_btn.clicked.connect(partial(self.set_keyframe, key_btn))
        sld_wid.layout().addWidget(fsg)
        sld_wid.layout().addWidget(key_btn)
        table.setCellWidget(row, self.column_blendvalue, sld_wid)

        # button
        btn = QtGui.QToolButton()
        btn.setText('Sculpt')
        btn.setCheckable(True)
        btn.setStyleSheet('QToolButton{color:#000;}')
        table.setCellWidget(row, self.column_visibility, btn)
        btn.clicked.connect(partial(self.change_visibility, btn, frame))
        btn.setChecked(checked)
        self.change_visibility(btn, frame)

        # frame
        ws = 8 - (len(frame)/2)
        frame_item = QtGui.QTableWidgetItem((' ' * ws) + frame)
        table.setItem(row, self.column_frame, frame_item)

        # remove btn
        rem_btn = QtGui.QToolButton()
        rem_btn.setText('X')
        rem_btn.setStyleSheet('QToolButton{background-color:#900; color:#fff;}'
                              'QToolButton:hover{background-color:#c00;}'
                              'QToolButton:pressed{background-color:#f00;}')
        rem_btn.clicked.connect(partial(self.remove_row, rem_btn))
        table.setCellWidget(row, self.column_remove, rem_btn)
        # timeline
        timeline_wid = QtGui.QWidget()
        timeline_wid.setLayout(QtGui.QHBoxLayout())
        timeline_wid.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                                     QtGui.QSizePolicy.Expanding))
        h = table.rowHeight(row)
        w = table.columnWidth(self.column_timeline)
        timeline_wid.resize(w, h)
        table.setCellWidget(row, self.column_timeline, timeline_wid)
        tl = timeline.Timeline(timeline_wid.layout(), timeline_wid)
        self.timelines.append(tl)
        tl.create_timeline_button(int(frame), 'green', 1)
        obj = self.uif.get_object_tab(table)
        trans = self.get_transform_dag_path(obj[1], name)
        start = cmds.playbackOptions(q=True, minTime=True)
        end = cmds.playbackOptions(q=True, maxTime=True)
        keys = cmds.keyframe('%s.blendValue' % trans,
                             time=(start, end), query=True, timeChange=True,
                             valueChange=True)
        if keys is not None:
            i = 0
            while i < len(keys):
                tl.create_timeline_button(int(keys[i]), 'red', keys[i+1])
                i = i+2
            # end while i < len(keys)
        # connect signals
        self.connect_table_signals(table)
        table.sortByColumn(self.column_number, QtCore.Qt.AscendingOrder)
        return row
    # end def add_row

    def resizeEvent(self, event):
        """Resizes the timeline when the window gets resized."""
        for timeline in self.timelines:
            timeline.resize_timeline()
    # end def resizeEvent

    def set_keyframe(self, btn):
        """Sets a keyframe on the current frame on the blend value of it's
        sculpt.
        """
        table = self.uif.get_object_table(btn)
        obj = self.uif.get_object_tab(table)
        row, column = self.uif.get_row_column(btn)
        trans = self.get_transform_dag_path(obj[1], table.item(row,
                                            self.column_name).text())
        attribute = '%s_BlendValue' % obj[1]
        cmds.select(trans, r=True)
        cmds.setKeyframe(trans, at=attribute)
    # end def set_keyframe

    def change_float_slider(self, src, target, value):
        """Changes the values of the spinbox and the slider of a float slider.
        @param src: the gui element that was edited by the user
        @param target: The gui element that has to be updated
        @param value: The value of the edited gui element
        @type src: QSlider or QDoubleSpinBox
        @type target: QSlider or QDoubleSpinBox
        @type value: int or float
        """
        if type(src) == QtGui.QSlider:
            value = float(src.value()) / float(src.maximum())
        else:
            value *= target.maximum()
        target.setValue(value)
    # end def change_float_slider

    def edit_envelope(self, slider, value):
        """Edits the envelope value."""
        obj = self.uif.get_object_tab(slider)
        char_grp = '%s_%s_%s' % (self.SF, self.CHAR, self.SF_CTL_GRP)
        obj_grp = '%s_%s_%s_%s' % (self.SF, self.CHAR, obj[1], self.SF_CTL_GRP)
        final_grp = '|%s|%s|%s|%s' % (self.SF_TOP_GRP, self.SF_GRP, char_grp, obj_grp)
        cmds.setAttr('%s.%s' % (final_grp, self.ENVELOPE), value)
        if value < 1:
            table = self.tabs[obj[1]][1]
            for row in range(table.rowCount()):
                btn = table.cellWidget(row, self.column_visibility)
                frame = table.item(row, self.column_frame).text()
                btn.setChecked(False)
                self.change_visibility(btn, frame)
            # end for row in range(table.rowCount())
    # end def edit_envelope

    def select_object(self, mesh):
        """Selects the given mesh."""
        cmds.select(mesh, r=True)
    # end def select_object

    def select_sculpt_transform(self, select_btn):
        """Selects the transform of the sculpt."""
        row, column = self.uif.get_row_column(select_btn)
        table = self.uif.get_object_table(select_btn)
        obj = self.uif.get_object_tab(select_btn)[1]
        sculpt = table.item(row, self.column_name).text()
        trans = self.get_transform_dag_path(obj, sculpt)
        cmds.select(trans, r=True)
    # end def select_sculpt_transform

    def save_item_state(self, item):
        """Saves the text of the clicked item in a variable to be able to use
        it's old value in the rename process.
        """
        self.edit_item_text = item.text()
    # end def rename_item_state

    def rename_item(self, item):
        """Renames the given item and the corresponding transform"""
        table = item.tableWidget()
        self.disconnect_table_signals(table)
        if self.edit_item_text is None:
            return
        if item.column() == self.column_name:
            obj = self.uif.get_object_tab(item.tableWidget())
            obj_grp = '%s_%s' % (obj[1], self.SF_TOOLS_GRP)
            item_name = ''.join(c for c in item.text() if c.isalnum() or c in '_')
            new_name = '%s' % (item_name)
            old_name = '%s' % (self.edit_item_text)
            old_dag_path = self.get_transform_dag_path(obj[1], old_name)
            cmds.rename(old_dag_path, new_name)
            item.setText(item_name)
        else:
            item.setText(self.edit_item_text)
        self.connect_table_signals(table)
    # end def rename_item

    def change_blend_value(self, spinbox, value):
        """Changes the blend value of the given slider."""
        table = self.uif.get_object_table(spinbox)
        obj = self.uif.get_object_tab(table)
        row, column = self.uif.get_row_column(spinbox.parent())
        trans = self.get_transform_dag_path(obj[1], table.item(row, self.column_name).text())
        cmds.setAttr('%s.blendValue' % trans, spinbox.value())
        btn = table.cellWidget(row, self.column_visibility)
        frame = table.item(row, self.column_frame).text()
        if value < 1:
            btn.setChecked(False)
        self.change_visibility(btn, frame)
        cmds.select(trans, r=True)
    # end def change_blend_value

    def change_visibility(self, btn, frame):
        """Changes the visibility of the sculpts."""
        table = self.uif.get_object_table(btn)
        obj = self.uif.get_object_tab(table)
        btn_row, btn_column = self.uif.get_row_column(btn)
        show = False
        for row in range(table.rowCount()):
            button = table.cellWidget(row, btn_column)
            if row == btn_row:
                if not button.isChecked():
                    button.setText('Original')
                    button.setStyleSheet('QToolButton{color:#ddd;}')
                    self.show_hide_sculpt(table, row, False)
                    show = True
                else:
                    button.setText('Sculpt')
                    button.setStyleSheet('QToolButton{color:#000;}')
                    self.show_hide_sculpt(table, row, True)
            else:
                button.setChecked(False)
                button.setText('Original')
                button.setStyleSheet('QToolButton{color:#ddd;}')
                self.show_hide_sculpt(table, row, False)
        # end for row in range(table.rowCount())
        self.show_original(obj[1], show)
        if not show:
            cmds.currentTime(frame)
            sculpt = table.item(btn_row, self.column_name).text()
            trans = self.get_transform_dag_path(obj[1], sculpt)
            if len(cmds.ls(sl=True, l=True)) > 0:
                if cmds.ls(sl=True, l=True)[0] != trans:
                    cmds.select(trans, r=True)
    # end def change_visiblity

    def show_original(self, obj, value):
        """Shows the original mesh of the given obj of the given character"""
        cmds.setAttr('%s_%s_%s_%s.%s' % (self.SF, self.CHAR, obj,
                     self.SF_CTL_GRP, obj), value)
    # end def show_original

    def show_hide_sculpt(self, table, row, show):
        """Hides the sculpt in the given row of the given table."""
        obj = self.uif.get_object_tab(table)
        #char = self.uif.get_character_tab(table)
        sculpt = table.item(row, self.column_name).text()
        trans = self.get_transform_dag_path(obj[1], sculpt)
        cmds.setAttr('%s.sculpt' % trans, show)
    # end def show_hide_sculpt

    def switch_tab(self, mesh):
        """Switches to the given character tab and to the given object tab."""
        index = self.tabs[mesh][0]
        self.sf_tabw.setCurrentIndex(index)
    # end def switch_tab

    def help(self):
        """Opens the Trixter documentation in the user's default webbrowser."""
        print 'Help will come soon ...'
        #webbrowser.open('http://wiki.trixter.intern/Animation/Tools/OnionSkin')
    # end def help

    def remove_row(self, remove_btn):
        """Removes the given row.
        @todo: remove tabs if empty
        """
        table = self.uif.get_object_table(remove_btn)
        table.sortByColumn(self.column_number, QtCore.Qt.AscendingOrder)
        self.disconnect_table_signals(table)
        row, column = self.uif.get_row_column(remove_btn)
        obj = self.uif.get_object_tab(table)
        trans = self.get_transform_dag_path(obj[1],
                                            table.item(row, self.column_name).text())
        sculpt = cmds.listConnections('%s.sculpt' % trans )[0]
        bls = self.get_blendshape_dag_path(obj[1], sculpt)
        cmds.select(bls, r=True)
        shotfinaling.RemoveShotFinal()
        number = int(table.item(row, self.column_number).text())
        # Remove timeline from list to avoid null pointer exception on window resize.
        tl = table.cellWidget(row, self.column_timeline)
        for i, timel in enumerate(self.timelines):
            if tl is timel.timeline.parent():
                self.timelines.pop(i)
                break
        # end for i, timel in enumerate(self.timelines)
        highest_number = table.rowCount()
        for row_number in reversed(range(number, highest_number+1)):
            item_text = self.item_text_margined(str(row_number))
            item = QtGui.QTableWidgetItem(item_text)
            table.setItem(row_number, self.column_number, item)
        # end for row_number in reversed(range(number, highest_number+1))
        table.removeRow(row)
        self.connect_table_signals(table)
    # end def remove_row

    def disconnect_table_signals(self, table):
        """Disconnects the table signals and the sorting ability."""
        table.setSortingEnabled(False)
        table.itemDoubleClicked.disconnect()
        table.itemChanged.disconnect()
    # def disconnect_table_signals

    def connect_table_signals(self, table):
        """Connects the table signals and re-enables the sorting ability."""
        table.setSortingEnabled(True)
        table.itemDoubleClicked.connect(self.save_item_state)
        table.itemChanged.connect(self.rename_item)
    # end def connect_table_signals

    def item_text_margined(self, text):
        """Returns the input text with the right margin for it to be centered
        in the column.
        """
        ws = 3 - (len(text) / 2)
        return (' ' * ws) + text
    # end def item_text_margin

    def get_transform_dag_path(self, obj, sculpt):
        """Returns the full dag path to the sculpt object."""
        top_tool_grp = '%s_%s_%s' % (self.SF, self.CHAR, self.SF_TOOL_TOP_GRP)
        tool_grp = '%s_%s_%s_%s' % (self.SF, self.CHAR, obj, self.SF_TOOL_TOP_GRP)
        obj_grp = '%s_%s_%s_%s' % (self.SF, self.CHAR, sculpt, self.CTL)
        return '|%s|%s|%s|%s|%s' % (self.SF_TOP_GRP, self.SF_GRP, top_tool_grp, tool_grp, obj_grp)
    # end def get_transform_dag_path

    def get_blendshape_dag_path(self, obj, sculpt):
        """Returns the full dag path to the blendshape object."""
        sf_grp = '%s_%s' % (obj, self.SF_GRP)
        bsp_grp = '%s_%s_BSP_GRP' % (self.SF, self.CHAR)
        sculpts_grp = '%s_%s_SCULPTS' % (self.SF, self.CHAR)
        return '|%s|%s|%s|%s|%s' % (self.SF_TOP_GRP, self.SF_BLS_GRP, bsp_grp,
                                sculpts_grp, sculpt)
    # end def get_blendshape_dag_path

    def recreate_engineerstools(self):
        """Checks if the engineerstools are already in the scene and
        reconstructs the ui from the elements in the scene.
        """
        return
        for grp in cmds.listRelatives(self.SF_TOP_GRP, c=True):
            if grp == self.SF_BLS_GRP:
                continue
            for sf_tool in cmds.listRelatives(grp, c=True):
                obj_name = sf_tool.split('_%s' % self.SF_TOOL_TOP_GRP)[0].split('_')[1]
                sf_tool_grp = '%s_%s_%s' % (self.SF, obj_name, self.SF_CTL_GRP)
                #tool_grp = '%s_%s_%s' % (self.SF, char_name, self.SF_TOOL_GRP)
                sf_grp = '%s|%s|%s' % (self.SF_TOP_GRP, self.SF_GRP,
                                       sf_tool_grp)
                self.create_object_tab(obj_name)

                for part in cmds.listRelatives(sf_grp, c=True):
                    sculpts = cmds.listRelatives(part, c=True)
                    if sculpts is None:
                        continue
                    for sculpt in sculpts:
                        frame = str(int(cmds.getAttr('%s.frameNumber' % sculpt)))
                        table = self.tabs[obj_name][1]
                        row = self.add_row(table, sculpt, frame, False)
                        btn = table.cellWidget(row, self.column_visibility)
                        btn.setChecked(False)
                        self.change_visibility(btn, frame)
                    # end for sculpt in sculpts
            # end for obj in cmds.listRelatives(grp, c=True)
        # end for grp in cmds.listRelatives()
    # end def recreate_engineerstools

    def pan(self):
        """Enters the pan tool."""
        cmds.PanZoomTool()
        cmds.panZoomCtx('PanZoomContext', e=True, panMode=True)
    # end def pan

    def zoom(self):
        """Enters the zoom tool."""
        cmds.PanZoomTool()
        cmds.panZoomCtx('PanZoomContext', e=True, zoomMode=True)
    # end def zoom

    def reset_pan_zoom(self):
        """Resets the pan and zoom attribute of all cameras."""
        for camera in cmds.ls(ca=True):
            cmds.setAttr('%s.panZoomEnabled' % camera, 0)
        cmds.SelectTool()
    # end def reset_pan_zoom

    def closeEvent(self, event):
        """Removes the callback when the shotfinaling window gets closed."""
        try:
            message = OpenMaya.MMessage()
            anm = OpenMayaAnim.MAnimMessage()
            anm.removeCallback(self.key_callback_id)
            print 'shotfinaling: deleted keyframe callback.'
            message.removeCallback(self.blendvalue_callback_id)
            print 'shotfinaling: deleted blend value slider callback.'
        except Exception as err:
            print err
    # end def closeEvent
# end class ShotfinalUI


def main():
    if cmds.objExists('SF_ENGINEERS_TOOLBOX'):
        cmds.confirmDialog(title='Old tools detected!',
                           message="""'The old shotfinaling tool has been detected in the scene.\nTo avoid any clashes and disfunctions\nplease use the old shotfinaling method from:\n\nTools/Finaling/Engineerstools'""")
        return
    global sf_win
    try:
        sf_win.close()
    except:
        pass
    sf_win = ShotfinalingUI()
    sf_win.show()
# end def main
