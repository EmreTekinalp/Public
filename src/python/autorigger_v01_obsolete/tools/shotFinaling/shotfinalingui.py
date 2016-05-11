"""Created on 2014/02/20
@author: Paul Schweizer
@email: paulschweizer@gmx.net
@brief: The main ui for the shotfinaling tool

"""
import os
import sys
import webbrowser
from functools import partial
from PySide import QtGui, QtCore
from maya import cmds, OpenMaya, OpenMayaAnim
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shotFinaling'))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import SFTOOL02_UPDATE as shotfinaling
from shotFinaling.ui import pysideconvenience
from shotFinaling.ui import floatslidergroup
from shotFinaling.ui import sftableview
from shotFinaling.ui import sfitemmodel
from shotFinaling.ui import sfitem
from shotFinaling.ui import macontroller
uifilepath = os.path.join(os.path.dirname(__file__), 'ui', 'shotfinaling.ui')
form_class, base_class = pysideconvenience.load_ui_type(uifilepath)

reload(sftableview)
reload(macontroller)


class ShotfinalingUI(base_class, form_class):
    """The UI for the shot finaling tool.
    @param parent: the parent widget
    @todo: remove tab when nothing is inside
    @todo: jump from keyframe to keyframe arrows(not important)

    """
    def __init__(self, parent=pysideconvenience.get_maya_window()):
        super(ShotfinalingUI, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry(1400, -250, 900, 330)
        self.macontroller = macontroller.MaController(self)
        self.setup_widgets()
        self.setup_css()
        self.setup_variables()
        if len(cmds.ls('SF_INFO_NODE*')) > 0:
            self.recreate()
        self.init_callbacks()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    # end def __init__

    def setup_widgets(self):
        """Sets up all widget connections and attributes."""
        self.sf_create_btn.clicked.connect(self.create_shot_final)
        self.pan_btn.clicked.connect(self.macontroller.pan)
        self.pan_btn.setIcon(QtGui.QIcon(":/camPanZoom.png"))
        self.zoom_btn.clicked.connect(self.macontroller.zoom)
        self.zoom_btn.setIcon(QtGui.QIcon(":/zoom.png"))
        self.reset_pan_zoom_btn.clicked.connect(self.macontroller.reset_pan_zoom)
        self.reset_pan_zoom_btn.setIcon(QtGui.QIcon(":/menuIconReset.png"))
    # end def setup_widgets

    def setup_css(self):
        """Sets up the css for Pandora's Box"""
        css_file = os.path.join(os.path.dirname(__file__), 'ui', 'style.css')
        with open(css_file, 'r') as f:
            css = f.read()
            f.close()
        self.setStyleSheet(css)
    # end def setup_css

    def setup_variables(self):
        """Sets up general variables."""
        self.tabs = dict()
        self.sculpts = dict()
        self.timelines = list()
        self.blendvalue_callback_id = None
        self.key_callback_id = None
    # end def setup_variables

    def init_callbacks(self):
        """Initializes the blendvalue and key callback."""
        self.blendvalue_callback_id = OpenMaya.MDGMessage().addTimeChangeCallback(self.macontroller.blend_value_callback)
        self.key_callback_id = OpenMayaAnim.MAnimMessage().addAnimKeyframeEditedCallback(self.macontroller.key_callback)
    # end def init_callback

    def create_shot_final(self):
        """Creates a new shot finaling sculpt for the selected object and the
        necessary ui widgets such as a new tab and table widget in case there is
        no tab for the selected object yet. Also creates new row for this sculpt.

        """
        triplekey = self.triplekey_chk.isChecked()
        triplekey_offset = self.triplekey_spn.value()
        sf = shotfinaling.ShotFinalMain(triplekey, triplekey_offset)
        if sf.mesh not in self.tabs:
            self.create_tab(sf.mesh)
        self.switch_tab(sf.mesh)
        self.add_row(self.tabs[sf.mesh][1], sf.sf_mesh_ctl, str(int(cmds.currentTime(q=True))))
    # end def create_shot_final

    def create_tab(self, mesh):
        """Creates a tab for the given mesh and adds a table view widget to it.
        Also initializes the model for the table view.
        @param mesh: the mesh the tab is created for.

        """
        wid = QtGui.QWidget()
        table = sftableview.SFTableView(self, self.macontroller)
        model = sfitemmodel.SFItemModel()
        table.setModel(model)
        top_tools = self.create_top_tools(mesh, table)
        wid.setLayout(QtGui.QVBoxLayout())
        wid.layout().addLayout(top_tools)
        wid.layout().addWidget(table)
        tab = self.sf_tabw.addTab(wid, mesh)
        self.tabs[mesh] = [tab, table]
        self.sf_tabw.setCurrentIndex(tab)
    # end def create_object_tab

    def create_top_tools(self, mesh, table):
        """Creates the tools on top of the table, consisting of a button to
        select the original mesh and a floatslidergroup for the envelope.
        @param mesh: the mesh
        @param: the table
        @return: returns the layout in which the widgets reside

        """
        lay = QtGui.QHBoxLayout()
        btn = QtGui.QToolButton()
        btn.setText('Select Original')
        btn.clicked.connect(partial(self.macontroller.select_object, mesh))
        lbl = QtGui.QLabel('Envelope:')
        fsg = floatslidergroup.FloatSliderGroup()
        fsg.set_minimum(0)
        fsg.set_maximum(1)
        fsg.set_decimals(3)
        fsg.set_value(1)
        fsg.spinbox.valueChanged.connect(partial(self.macontroller.edit_envelope, fsg.spinbox, mesh, table))
        lay.addWidget(btn)
        lay.addWidget(lbl)
        lay.addWidget(fsg)
        lay.addStretch()
        return lay
    # end def create_top_tools

    def add_row(self, table, name, frame, keys=None, checked=True, change_visibility=True):
        """Adds a new row to the given table. A row consists of the following columns:
        * name: the name of the sculpt
        * show keys button: the button that shows the keys for the sculpt in the timeline
        * visibility: the button to switch between displaying the original or the sculpt
        * frame: the frame on which the sculpt has been initialized
        * remove: button that removes the sculpt
        * timeline: the timeline that shows the keys for this sculpt
        @param table: the table view widget where the row is to be added to
        @param name: the name of the sculpt
        @param frame: the frame at which the sculpt has been initialized
        @param keys: the keys for the sculpt
        @param checked: whether the visibility button shall be checked or not
        @param change_visibility: if true, all sculpts are set to original except the new one

        """
        name_item = sfitem.SFItem()
        name_item.setData(name, QtCore.Qt.DisplayRole)
        show_keys_btn_item = sfitem.SFItem()
        show_keys_btn_item.setData('Show Keys', QtCore.Qt.DisplayRole)
        blendvalue_item = sfitem.SFItem()
        blendvalue_item.setData('blend value slider', QtCore.Qt.DisplayRole)
        visibility_item = sfitem.SFItem()
        visibility_item.setData(checked, QtCore.Qt.DisplayRole)
        frame_item = sfitem.SFItem()
        frame_item.setData(frame, QtCore.Qt.DisplayRole)
        remove_item = sfitem.SFItem()
        remove_item.setData('Remove', QtCore.Qt.DisplayRole)
        # timeline
        timeline_item = sfitem.SFItem()
        timeline_item.setData('Timeline (coming soon ...)', QtCore.Qt.DisplayRole)
        if keys is None:
            self.add_keys(timeline_item, [frame])
        else:
            self.add_keys(timeline_item, keys)
        table.model().appendRow([name_item,
                                show_keys_btn_item,
                                blendvalue_item,
                                visibility_item,
                                frame_item,
                                remove_item,
                                timeline_item])
        if change_visibility:
            self.macontroller.change_visibility(table.model().indexFromItem(visibility_item), table)
    # end def add_row

    def add_keys(self, item, keys):
        """Adds the given keys to the given item in the form of child items.
        @param item: the item, the keys shall be added to
        @param keys: the keys to be added

        """
        for key in keys:
            keyitem = sfitem.SFItem()
            keyitem.setData(int(key), QtCore.Qt.DisplayRole)
            item.appendRow(keyitem)
        # end for key in keys
    # end def add_keys

    def switch_tab(self, mesh):
        """Switches to the tab of the given mesh.
        @param mesh: the mesh

        """
        index = self.tabs[mesh][0]
        self.sf_tabw.setCurrentIndex(index)
    # end def switch_tab

    def help(self):
        """Opens the help page for the shotfinaling tool."""
        print 'Help will come soon ...'
        #webbrowser.open('http://wiki.trixter.intern/Animation/Tools/OnionSkin')
    # end def help

    def recreate(self):
        """Reconstructs the ui from the elements found in the scene."""
        for info in cmds.ls('SF_INFO_NODE*', type='transform'):
            for sculpt in cmds.listAttr(info, ud=True):
                sculpt = cmds.listConnections('%s.%s' % (info, sculpt))[0]
                bls = cmds.listConnections('%s.blendValue' % sculpt, type='blendShape')[0]
                ma_obj = cmds.listConnections('%s.outputGeometry[0]' % bls)[0]
                if ma_obj not in self.tabs:
                    self.create_tab(ma_obj)
                self.switch_tab(ma_obj)
                checked = cmds.getAttr('%s.sculpt' % sculpt)
                self.add_row(self.tabs[ma_obj][1], sculpt,
                             cmds.getAttr('%s.frameNumber' % sculpt),
                             keys=cmds.keyframe(sculpt, q=True),
                             checked=checked,
                             change_visibility=False)
            # end for sculpt in cmds.listAttr(info, ud=True)
        # end for info in cmds.ls('SF_INFO_NODE*', type='transform')
    # end def recreate

    def closeEvent(self, event):
        """Removes the callback when the shotfinaling window gets closed.
        @param event: the Qt event for closing a window

        """
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
    global sf_win
    try:
        sf_win.close()
        sf_win.deleteLater()
    except:
        pass
    sf_win = ShotfinalingUI()
    sf_win.show()
# end def main

