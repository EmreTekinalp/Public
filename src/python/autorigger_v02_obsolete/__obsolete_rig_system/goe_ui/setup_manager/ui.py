'''
@author:  etekinalp
@date:    Sep 7, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates the file browser ui
'''

import os

from PySide import QtGui
from PySide import QtCore

from maya import cmds
from goe_ui.setup_manager.contents import content
reload(content)

window_title  = "GOE SetupManager"
window_object = "goe_setupManager"


class SetupManager(QtGui.QDialog):
    def __init__(self, parent=content.get_maya_window()):
        super(SetupManager, self).__init__(parent)

        #--- vars
        self.project_path   = None
        self.project_info   = list()
        self.projects       = list()
        self.types          = list()

        self.current_project = None
        self.current_type    = None
        self.current_asset   = None
        self.current_res     = None

        #--- methods
        self.__create()
    #END __init__()

    def __setup_ui(self):
        self.setWindowTitle(window_title)
        self.setObjectName(window_object)
        self.setGeometry(600,300,300,100)
        self.setFixedSize(320,290)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    #END __setup_ui()

    def __create_labels(self):
        icons_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'icons')
        if not os.path.exists(icons_path):
            raise Exception("Path does not exist: " + `icons_path`)
        #--- header image
        header_pic = QtGui.QPixmap(os.path.join(icons_path, "goe_header.jpg"))
        self.header_pic = QtGui.QLabel()
        self.header_pic.setPixmap(header_pic)

        #--- plus project image
        release_pic = QtGui.QPixmap(os.path.join(icons_path, "plus.png"))
        pressed_pic = QtGui.QPixmap(os.path.join(icons_path, "plusPress.png"))
        self.plus_project_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.plus_project_pic.setPixmap(release_pic)

        #--- plus type image
        self.plus_type_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.plus_type_pic.setPixmap(release_pic)

        #--- plus asset image
        self.plus_asset_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.plus_asset_pic.setPixmap(release_pic)

        #--- minus project image
        release_pic = QtGui.QPixmap(os.path.join(icons_path, "minus.png"))
        pressed_pic = QtGui.QPixmap(os.path.join(icons_path, "minusPress.png"))
        self.minus_project_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.minus_project_pic.setPixmap(release_pic)
        self.minus_project_pic.setHidden(True)

        #--- minus type image
        self.minus_type_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.minus_type_pic.setPixmap(release_pic)
        self.minus_type_pic.setHidden(True)

        #--- minus asset image
        self.minus_asset_pic = content.ExtendedQLabel(self, pressed_pic, release_pic)
        self.minus_asset_pic.setPixmap(release_pic)
        self.minus_asset_pic.setHidden(True)

        #--- change image
        release_pic = QtGui.QPixmap(os.path.join(icons_path, "refresh.png"))
        pressed_pic = QtGui.QPixmap(os.path.join(icons_path, "refreshPress.png"))
        plus = [self.plus_project_pic, self.plus_type_pic, self.plus_asset_pic]
        minus = [self.minus_project_pic, self.minus_type_pic, self.minus_asset_pic]
        self.change_pic = content.ExtendedQLabel(self, pressed_pic, release_pic,
                                                 plus, minus)
        self.change_pic.setPixmap(release_pic)

        #--- pandorasBox project path
        self.path_txt = QtGui.QLabel("PandorasBox Project Path (MAYA_PLUGIN_PATH):")
        self.project_name_txt = QtGui.QLabel("Project Name:")
        self.asset_type_txt = QtGui.QLabel("Asset Type:")
        self.asset_name_txt = QtGui.QLabel("Asset Name:")
        self.asset_res_txt = QtGui.QLabel("Asset Resolution:")
    #END __create_labels()

    def __create_buttons(self):
        self.create_btn = QtGui.QPushButton("Create")
    #END __create_buttons()

    def __create_line_edits(self):
        self.browse_edit = QtGui.QLineEdit()
        self.browse_edit.setReadOnly(True)
    #END __create_line_edits()

    def __create_combo_boxes(self):
        #--- project name
        self.project_name = ['...']
        self.project_name_cbox = QtGui.QComboBox()
        self.project_name_cbox.addItems(self.project_name)
        self.project_name_cbox.setFixedSize(150,20)
        self.project_name_cbox.setEditable(False)

        #--- asset types
        self.asset_types = []
        self.asset_type_cbox = QtGui.QComboBox()
        self.asset_type_cbox.addItems(self.asset_types)
        self.asset_type_cbox.setFixedSize(150,20)
        self.asset_type_cbox.setEditable(False)

        #--- asset names
        self.asset_names = []
        self.asset_name_cbox = QtGui.QComboBox()
        self.asset_name_cbox.addItems(self.asset_names)
        self.asset_name_cbox.setFixedSize(150,20)
        self.asset_name_cbox.setEditable(False)

        #--- asset resolution
        self.asset_res = ['Hi','Mid','Lo']
        self.asset_res_cbox = QtGui.QComboBox()
        self.asset_res_cbox.addItems(self.asset_res)
        self.asset_res_cbox.setFixedSize(150,20)
    #END __create_combo_box()

    def __setup_layout(self):
        #--- create layouts
        vbox  = QtGui.QVBoxLayout()
        vboxa = QtGui.QVBoxLayout()
        hboxa = QtGui.QHBoxLayout()
        hboxb = QtGui.QHBoxLayout()
        hboxc = QtGui.QHBoxLayout()
        hboxd = QtGui.QHBoxLayout()
        hboxe = QtGui.QHBoxLayout()
        hboxf = QtGui.QHBoxLayout()
        hboxg = QtGui.QHBoxLayout()
        hboxh = QtGui.QHBoxLayout()

        #--- add widgets to layouts
        hboxa.addWidget(self.header_pic)
        hboxb.addWidget(self.path_txt)
        hboxc.addWidget(self.browse_edit)
        hboxd.addWidget(self.project_name_txt)
        hboxd.addStretch()
        hboxd.addWidget(self.project_name_cbox)
        hboxd.addWidget(self.plus_project_pic)
        hboxd.addWidget(self.minus_project_pic)
        hboxe.addWidget(self.asset_type_txt)
        hboxe.addStretch()
        hboxe.addWidget(self.asset_type_cbox)
        hboxe.addWidget(self.plus_type_pic)
        hboxe.addWidget(self.minus_type_pic)
        hboxf.addWidget(self.asset_name_txt)
        hboxf.addStretch()
        hboxf.addWidget(self.asset_name_cbox)
        hboxf.addWidget(self.plus_asset_pic)
        hboxf.addWidget(self.minus_asset_pic)
        hboxg.addWidget(self.asset_res_txt)
        hboxg.addStretch()
        hboxg.addWidget(self.asset_res_cbox)
        hboxg.addWidget(self.change_pic)
        hboxh.addWidget(self.create_btn)

        #--- add layouts and stretches
        vboxa.addLayout(hboxb)
        vboxa.addLayout(hboxc)
        vboxa.addStretch()
        vboxa.addLayout(hboxd)
        vboxa.addLayout(hboxe)
        vboxa.addLayout(hboxf)
        vboxa.addLayout(hboxg)
        vboxa.addStretch()
        vboxa.setStretch(1,2)

        self.group_box = QtGui.QGroupBox()
        self.group_box.setLayout(vboxa)

        vbox.addLayout(hboxa)
        vbox.addWidget(self.group_box)
        vbox.addLayout(hboxh)

        #--- set layout
        self.setLayout(vbox)
    #END __setup_layout

    def __check_project_path(self):
        path = os.getenv('MAYA_PLUG_IN_PATH')
        envs = path.split(':')
        for i in envs:
            if 'PandorasBox' in i:
                self.project_path = i
        self.browse_edit.setText(self.project_path)

        #--- get project info
        self.project_info = content.get_project_info(self.project_path)

        #--- set project info
        self.__set_project_info()
    #END __check_project_path()

    def __set_project_info(self):
        #--- set project info
        if not self.project_info:
            return
        self.projects = [i.keys()[0] for i in self.project_info]
        self.project_name_cbox.clear()
        if self.projects:
            self.projects.sort()
            self.projects.insert(0, '...')
            self.project_name_cbox.addItems(self.projects)
        else:
            self.project_name_cbox.addItem('...')
    #END __set_project_info()

    def __update_project_info(self):
        self.current_project = self.project_name_cbox.currentText()
        self.asset_type_cbox.clear()
        for d in self.project_info:
            for i in d.items():
                if not self.current_project == i[0]:
                    continue
                self.types = i[1].keys()
                if self.types:
                    self.types.sort()
                    self.asset_type_cbox.addItems(self.types)
    #END __update_project_info()

    def __update_type_info(self):
        if not self.types:
            return
        self.current_project = self.project_name_cbox.currentText()
        self.current_type = self.asset_type_cbox.currentText()
        self.asset_name_cbox.clear()
        for d in self.project_info:
            for i in d.items():
                if not self.current_project == i[0]:
                    continue
                for t in i[1].items():
                    if not self.current_type == t[0]:
                        continue
                    self.assets = t[1]
                    if self.assets:
                        self.assets.sort()
                        self.asset_name_cbox.addItems(self.assets)
    #END __update_type_info()

    def __add_project(self):
        result = self.__add_prompt_dialog()
        if result:
            count = self.project_name_cbox.count()
            self.project_name_cbox.addItem(result)
            self.project_name_cbox.setCurrentIndex(count)
    #END __add_project()

    def __add_type(self):
        if self.project_name_cbox.currentIndex():
            result = self.__add_prompt_dialog()
            if result:
                count = self.asset_type_cbox.count()
                self.asset_type_cbox.addItem(result)
                self.asset_type_cbox.setCurrentIndex(count)
    #END __add_type()

    def __add_asset(self):
        if self.asset_type_cbox.currentText():
            result = self.__add_prompt_dialog()
            if result:
                count = self.asset_name_cbox.count()
                self.asset_name_cbox.addItem(result)
                self.asset_name_cbox.setCurrentIndex(count)
    #END __add_asset()

    def __add_prompt_dialog(self):
        text = None
        result = cmds.promptDialog(title='Create new...',
                                   message='Enter Name:',
                                   button=['OK', 'Cancel'],
                                   defaultButton='OK',
                                   cancelButton='Cancel',
                                   dismissString='Cancel')
        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
        return text
    #END __add_prompt_dialog()

    def __add_asset_structure(self):
        self.current_project = self.project_name_cbox.currentText()
        self.current_type = self.asset_type_cbox.currentText()
        self.current_asset = self.asset_name_cbox.currentText()
        self.current_res = self.asset_res_cbox.currentText()
        if self.current_project == '...':
            if not self.current_type:
                return
            else:
                if not self.current_asset:
                    return
        if self.current_project:
            if not self.current_type:
                return
            else:
                if not self.current_asset:
                    return
        #--- create new structure
        content.set_new_structure(self.project_path,
                                  self.current_project, 
                                  self.current_type, 
                                  self.current_asset, 
                                  self.current_res)
        #--- store the previous current states
        project = self.project_name_cbox.currentIndex()
        types = self.asset_type_cbox.currentIndex()
        asset = self.asset_name_cbox.currentIndex()
        res = self.asset_res_cbox.currentIndex()
        #--- update setup manager
        self.__check_project_path()
        #--- set the previous states
        self.project_name_cbox.setCurrentIndex(project)
        self.asset_type_cbox.setCurrentIndex(types)
        self.asset_name_cbox.setCurrentIndex(asset)
        self.asset_res_cbox.setCurrentIndex(res)
    #END __add_asset_structure()

    def __remove_project(self):
        current = self.project_name_cbox.currentText()
        result = self.__remove_prompt_dialog(current)
        if result == current:
            self.__remove_asset_structure(element=0)
    #END __remove_project()

    def __remove_type(self):
        current = self.asset_type_cbox.currentText()
        result = self.__remove_prompt_dialog(current)
        if result == current:
            self.__remove_asset_structure(element=1)
    #END __remove_type()

    def __remove_asset(self):
        current = self.asset_name_cbox.currentText()
        current += '_' + self.asset_res_cbox.currentText()
        result = self.__remove_prompt_dialog(current)
        if result == current:
            self.__remove_asset_structure(element=2)
    #END __remove_asset()

    def __remove_prompt_dialog(self, element):
        text = None
        result = cmds.promptDialog(title='Remove existing...',
                                   message='Remove following element:',
                                   text = element,
                                   button=['Remove', 'Cancel'],
                                   defaultButton='Remove',
                                   cancelButton='Cancel',
                                   dismissString='Cancel')
        if result == 'Remove':
            text = cmds.promptDialog(query=True, text=True)
        return text
    #END __remove_prompt_dialog()

    def __remove_asset_structure(self, element=2):
        self.current_project = self.project_name_cbox.currentText()
        self.current_type = self.asset_type_cbox.currentText()
        self.current_asset = self.asset_name_cbox.currentText()
        self.current_res = self.asset_res_cbox.currentText()
        if self.current_project == '...':
            if not self.current_type:
                return
            else:
                if not self.current_asset:
                    return
        if self.current_project:
            if not self.current_type:
                return
            else:
                if not self.current_asset:
                    return
        #--- remove structure
        result = content.remove_structure(self.project_path,
                                          self.current_project, 
                                          self.current_type, 
                                          self.current_asset, 
                                          self.current_res,
                                          element)
        if result:
            if not element:
                index = self.project_name_cbox.currentIndex()
                self.project_name_cbox.removeItem(index)
            elif element == 1:
                index = self.asset_type_cbox.currentIndex()
                self.asset_type_cbox.removeItem(index)
            elif element == 2:
                index = self.asset_name_cbox.currentIndex()
                self.asset_name_cbox.removeItem(index)
        #--- update setup manager
        self.__check_project_path()
    #END __remove_asset_structure()

    def __connect_signals(self):
        self.project_name_cbox.currentIndexChanged['QString'].connect(self.__update_project_info)
        self.asset_type_cbox.currentIndexChanged['QString'].connect(self.__update_type_info)

        self.connect(self.plus_project_pic, QtCore.SIGNAL('clicked()'), self.__add_project)
        self.connect(self.plus_type_pic, QtCore.SIGNAL('clicked()'), self.__add_type)
        self.connect(self.plus_asset_pic, QtCore.SIGNAL('clicked()'), self.__add_asset)

        self.connect(self.minus_project_pic, QtCore.SIGNAL('clicked()'), self.__remove_project)
        self.connect(self.minus_type_pic, QtCore.SIGNAL('clicked()'), self.__remove_type)
        self.connect(self.minus_asset_pic, QtCore.SIGNAL('clicked()'), self.__remove_asset)

        self.create_btn.clicked.connect(self.__add_asset_structure)
    #END __connect_signals()

    def __create(self):
        #--- setup ui specifics
        self.__setup_ui()

        #--- create labels
        self.__create_labels()

        #--- create buttons
        self.__create_buttons()

        #--- create line edits
        self.__create_line_edits()

        #--- create combo boxes
        self.__create_combo_boxes()

        #--- setup layout
        self.__setup_layout()

        #--- check project path
        self.__check_project_path()

        #--- connect signals
        self.__connect_signals()
    #END __create()
#END SetupManager()


def main(*args, **kwargs):
    if cmds.window(window_object, query=True, exists=True):
        cmds.deleteUI(window_object)
    global win
    win = SetupManager(content.get_maya_window())
    win.show()
#END main()
