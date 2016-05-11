'''
@author:  etekinalp
@date:    Sep 7, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates pandoras box
'''

import os

from PySide import QtGui
from PySide import QtCore

from maya import cmds
from goe_ui.pandoras_box.contents import content
reload(content)

window_title  = "GOE PandorasBox"
window_object = "goe_pandorasBox"
dock_title = "PandorasBox"
dock_object = window_object + "_dock"


class PandorasBox(QtGui.QDialog):
    def __init__(self, parent=content.get_maya_window()):
        super(PandorasBox, self).__init__(parent)

        #--- vars
        self.project_path    = None
        self.project_info    = list()
        self.projects        = list()
        self.types           = list()

        self.current_project = None
        self.current_type    = None
        self.current_asset   = None
        self.current_res     = None

        self.guide_data      = list()
        self.framelist       = list()

        #--- methods
        self.__create()
    #END __init__()

    def __setup_ui(self):
        self.setWindowTitle(window_title)
        self.setObjectName(window_object)
        self.setGeometry(600,300,450,750)
        self.setMinimumWidth(460)
        self.setMaximumWidth(470)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    #END __setup_ui()

    def __create_labels(self):
        icons_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "icons")
        assert os.path.exists(icons_path), "Path does not exist: " + `icons_path`
        #--- header image
        header_pic = QtGui.QPixmap(os.path.join(icons_path, "header.jpg"))
        self.header_pic = QtGui.QLabel()
        self.header_pic.setPixmap(header_pic)

        #--- pandorasBox project path
        self.project_name_txt = QtGui.QLabel("Project Name:")
        self.asset_type_txt = QtGui.QLabel("Asset Type:")
        self.asset_name_txt = QtGui.QLabel("Asset Name:")
        self.asset_res_txt = QtGui.QLabel("Asset Resolution:")

        self.type_txt = QtGui.QLabel("genericProp:")
        self.side_txt = QtGui.QLabel("L")
        self.mod_txt = QtGui.QLabel("swordHandle")
    #END __create_labels()

    def __create_buttons(self):
        #--- generate script button
        self.generate_btn = QtGui.QPushButton("Generate Script")
    #END __create_buttons()

    def __create_combo_boxes(self):
        #--- project name
        self.project_name = ['...']
        self.project_name_cbox = QtGui.QComboBox()
        self.project_name_cbox.addItems(self.project_name)
        self.project_name_cbox.setEditable(False)

        #--- asset types
        self.asset_types = []
        self.asset_type_cbox = QtGui.QComboBox()
        self.asset_type_cbox.addItems(self.asset_types)
        self.asset_type_cbox.setEditable(False)

        #--- asset names
        self.asset_names = []
        self.asset_name_cbox = QtGui.QComboBox()
        self.asset_name_cbox.addItems(self.asset_names)
        self.asset_name_cbox.setEditable(False)

        #--- asset resolution
        self.asset_res = ['Hi','Mid','Lo']
        self.asset_res_cbox = QtGui.QComboBox()
        self.asset_res_cbox.addItems(self.asset_res)
    #END __create_combo_boxes()

    def __create_project_settings(self):
        self.project_layout = QtGui.QVBoxLayout()
        vboxa = QtGui.QVBoxLayout()
        vboxb = QtGui.QVBoxLayout()
        vboxc = QtGui.QVBoxLayout()
        vboxd = QtGui.QVBoxLayout()
        vboxe = QtGui.QVBoxLayout()

        hboxa = QtGui.QHBoxLayout()
        hboxb = QtGui.QHBoxLayout()

        #--- project name
        vboxa.addWidget(self.project_name_txt)
        vboxa.addWidget(self.project_name_cbox)
        hboxa.addLayout(vboxa)

        #--- asset type
        vboxb.addWidget(self.asset_type_txt)
        vboxb.addWidget(self.asset_type_cbox)
        hboxb.addLayout(vboxb)

        #--- asset name
        vboxc.addWidget(self.asset_name_txt)
        vboxc.addWidget(self.asset_name_cbox)
        hboxb.addLayout(vboxc)

        #--- asset resolution
        vboxd.addWidget(self.asset_res_txt)
        vboxd.addWidget(self.asset_res_cbox)
        hboxb.addLayout(vboxd)

        #--- add layouts
        vboxe.addLayout(hboxa)
        vboxe.addLayout(hboxb)
        self.project_layout.addLayout(vboxe)
    #END __create_project_settings()

    def __create_guide_group(self):
        #--- create layouts
        self.group_layout = QtGui.QVBoxLayout()
        self.frame_layout = QtGui.QVBoxLayout()
        self.move_layout = QtGui.QHBoxLayout()
        #--- create group box
        self.group_box = QtGui.QGroupBox('Guides')
        self.group_box.setMinimumSize(50,30)
        #--- create buttons
        self.create_guide_btn = content.CreateGuideButton(self, 'Create Guide')
        self.up_guide_btn = content.MoveButton(self, 'Move up', 1)
        self.down_guide_btn = content.MoveButton(self, 'Move down', 0)
        #--- add widgets to layout
        self.group_layout.addWidget(self.create_guide_btn)
        self.group_layout.addLayout(self.frame_layout)
        self.move_layout.addWidget(self.up_guide_btn)
        self.move_layout.addWidget(self.down_guide_btn)
        self.group_layout.addLayout(self.move_layout)
        self.group_layout.addStretch()
        #--- set layout
        self.group_box.setLayout(self.group_layout)
    #END __create_guide_group()

    def __create_puppet_group(self):
        #--- create layouts
        self.puppet_layout = QtGui.QVBoxLayout()
        self.puppet_frame_layout = QtGui.QVBoxLayout()
        self.puppet_move_layout = QtGui.QHBoxLayout()
        #--- create group box
        self.puppet_group_box = QtGui.QGroupBox('Puppets')
        self.puppet_group_box.setMinimumSize(50,30)
        #--- create buttons
        self.create_puppet_btn = content.CreatePuppetButton(self, 'Create Puppet')
        self.up_puppet_btn = content.MoveButton(self, 'Move up', 1)
        self.down_puppet_btn = content.MoveButton(self, 'Move down', 0)
        #--- add widgets to layout
        self.puppet_layout.addWidget(self.create_puppet_btn)
        self.puppet_layout.addLayout(self.puppet_frame_layout)
        self.puppet_move_layout.addWidget(self.up_puppet_btn)
        self.puppet_move_layout.addWidget(self.down_puppet_btn)
        self.puppet_layout.addLayout(self.puppet_move_layout)
        self.puppet_layout.addStretch()
        #--- set layout
        self.puppet_group_box.setLayout(self.puppet_layout)
    #END __create_guide_group()

    def __setup_layout(self):
        #--- create layouts
        main_layout  = QtGui.QVBoxLayout()
        scrollLayout = QtGui.QVBoxLayout()
        scrollArea = QtGui.QScrollArea()
        scrollWidget = QtGui.QWidget()

        #--- add layouts, widgets and stretches
        main_layout.addWidget(self.header_pic)
        main_layout.addLayout(self.project_layout)
        main_layout.addWidget(self.group_box)
        main_layout.addWidget(self.puppet_group_box)
        main_layout.addStretch(1)
        main_layout.addWidget(self.generate_btn)

        scrollWidget.setLayout(main_layout)
        scrollArea.setWidget(scrollWidget)
        scrollLayout.addWidget(scrollArea)

        #--- set layout
        self.setLayout(main_layout)
    #END __setup_layout'

    def __create(self):
        #--- setup ui specifics
        self.__setup_ui()

        #--- create labels
        self.__create_labels()

        #--- create buttons
        self.__create_buttons()

        #--- create combo boxes
        self.__create_combo_boxes()

        #--- create project settings
        self.__create_project_settings()

        #--- create guide prop
        self.__create_guide_group()

        #--- create puppet prop
        self.__create_puppet_group()

        #--- setup layout
        self.__setup_layout()
    #END __create()
#END SetupManager()


def main(*args, **kwargs):
    if cmds.window(window_object, query=True, exists=True):
        cmds.deleteUI(window_object)
#     if cmds.window(ui_guide.guide_object, query=True, exists=True):
#         cmds.deleteUI(ui_guide.guide_object)
    if cmds.dockControl(dock_object, exists=True):
        cmds.deleteUI(dock_object)

    win = PandorasBox(content.get_maya_window())

    cmds.dockControl(dock_object, area="right", allowedArea=["left", "right"], 
                     width=430, content=window_object, label=dock_title)
    print win.objectName(), ' successfully loaded'
#END main()

# main()