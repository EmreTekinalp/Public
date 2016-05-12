'''
@author:  etekinalp
@date:    Sep 7, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module contains the ui content
'''


import os
import json

from maya import OpenMayaUI, cmds
from PySide import QtGui, QtCore
from shiboken import wrapInstance

from goe_ui.pandoras_box import ui_settings
from goe_functions import data


def get_maya_window():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QWidget)
#END get_maya_window()


def get_project_path():
    #--- get projectPath
    project_path = None
    path = os.getenv('MAYA_PLUG_IN_PATH')
    envs = path.split(':')
    for i in envs:
        if 'PandorasBox' in i:
            project_path = i
    assert project_path, "Please setup the projectPath in the maya env file!"
    return project_path
#END get_project_path()


def get_project_info():
    result = list()
    project_path = get_project_path()

    #--- check if goe_builds path exists in PandorasBox
    build_path = os.path.join(project_path, 'goe_builds')
    if not os.path.exists(build_path):
        raise Exception("Path does not exist: " + repr(build_path))

    #--- get the projects
    projects = list()
    pro_path = os.listdir(build_path)
    for pro in pro_path:
        if os.path.isdir(os.path.join(build_path, pro)):
            projects.append(pro)

    #--- get the types and assets
    for pro in projects:
        assets = dict()
        info = dict()
        #--- list asset types
        if not os.path.isdir(os.path.join(build_path, pro)):
            continue
        typ_path = os.listdir(os.path.join(build_path, pro))
        for typ in typ_path:
            if not os.path.isdir(os.path.join(build_path, pro, typ)):
                continue
            #--- list asset names
            asset_path = os.listdir(os.path.join(build_path, pro, typ))
            asset = list()
            for ass in asset_path:
                if not ass:
                    continue
                if not os.path.isdir(os.path.join(build_path, pro, typ, ass)):
                    continue
                #--- list asset res and append it via dict
                asset_res = os.listdir(os.path.join(build_path, pro, typ, ass))
                resolution = list()
                for res in asset_res:
                    if not res:
                        continue
                    if not os.path.isdir(os.path.join(build_path, pro, typ, ass, res)):
                        continue
                    r = res.split('_')[1]
                    resolution.append(r)
                a = dict()
                a[ass] = resolution
                asset.append(a)
            assets[typ] = asset
        info[pro] = assets
        result.append(info)
    return result
#END get_project_info()


def setup_guide_ui(path):
    gbuilds = data.load_guide_builds(path)
    if not gbuilds:
        return
    result = list()
    for d in gbuilds:
        result.append(d)
    return result
#END setup_guide_ui()


def check_project_path():
    project_path = None
    path = os.getenv('MAYA_PLUG_IN_PATH')
    envs = path.split(':')
    for i in envs:
        if 'PandorasBox' in i:
            project_path = i

    #--- get project info
    get_project_info(project_path)
#END check_project_path()


class FrameGuide(QtGui.QFrame):
    def __init__(self, parent, framelist, rigdata):
        super(FrameGuide, self).__init__(parent)
        self.parent = parent
        self.setWhatsThis('QFrame')
        self.framelist = framelist
        self.rigdata = rigdata
        self.setupWidget()
    #END __init__()

    def setupWidget(self):
        #--- create label and edit button
        framecolora = QtGui.QFrame()
        framecolorb = QtGui.QFrame()
        framecolora.setFixedWidth(5)
        framecolorb.setFixedWidth(5)
        framecolora.setStyleSheet('background-color: rgb(255,180,50)')
        framecolorb.setStyleSheet('background-color: rgb(255,180,50)')

        if not isinstance(self.rigdata, list):
            self.setupStyleSheet(self.rigdata, framecolora, framecolorb)
            #--- define and set info text
            self.modname = self.rigdata['moduleName']
            self.objname = (self.rigdata['moduleType'] + ': ' +
                            self.rigdata['side'].upper() + '_' +
                            self.rigdata['moduleName'].upper() + '_MOD')
            self.txt = QtGui.QLabel(self.objname)
        else:
            self.setupStyleSheet(self.rigdata[0], framecolora, framecolorb)
            #--- define and set info text
            self.modname = self.rigdata[0]['moduleName']
            self.objname = (self.rigdata[0]['moduleType'] + ': ' +
                            self.rigdata[0]['side'].upper() + '_' +
                            self.rigdata[0]['moduleName'].upper() + '_MOD')
            self.txt = QtGui.QLabel(self.objname)

        edit_guide_btn = EditButton(self)
        remove_guide_btn = RemoveButton(self, self.parent)

        #--- create layouts and setup
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(framecolora)
        hbox.addWidget(framecolorb)
        hbox.addWidget(self.txt)
        hbox.addStretch()
        hbox.addWidget(edit_guide_btn)
        if isinstance(self.rigdata, list):
            if self.rigdata[0]['mirror']:
                mirror_guide_btn = MirrorButton(self)
                hbox.addWidget(mirror_guide_btn)
        else:
            if self.rigdata['mirror']:
                origin = self.rigdata
                mirror = dict(self.rigdata)
                mirror['side'] = mirror['mirrorside']
                if mirror['side'] == 'R':
                    mirror['color'] = 13
                elif mirror['side'] == 'L':
                    mirror['color'] = 6
                self.rigdata = [origin, mirror]
                mirror_guide_btn = MirrorButton(self)
                hbox.addWidget(mirror_guide_btn)
        hbox.addWidget(remove_guide_btn)

        self.setLayout(hbox)
        self.setStyleSheet('background-color: rgb(50,50,50)')
    #END setupWidget()

    def setupStyleSheet(self, rigdata, framecolora, framecolorb):
        if rigdata['side'] == 'L':
            framecolora.setStyleSheet('background-color: rgb(50,75,255)')
            framecolorb.setStyleSheet('background-color: rgb(50,75,255)')
            if rigdata['mirror']:
                framecolorb.setStyleSheet('background-color: rgb(255,75,50)')
        elif rigdata['side'] == 'R':
            framecolora.setStyleSheet('background-color: rgb(255,75,50)')
            framecolorb.setStyleSheet('background-color: rgb(255,75,50)')
            if rigdata['mirror']:
                framecolorb.setStyleSheet('background-color: rgb(50,75,255)')
    #END setupStyleSheet()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            find = None
            if isinstance(self.rigdata, list):
                find = self.rigdata[0]['moduleName']
            else:
                find = self.rigdata['moduleName']
            sel = cmds.ls('*' + find + '*', type='goe_locator')
            if sel:
                cmds.select(sel)
        elif event.button() == QtCore.Qt.RightButton:
            cmds.select(clear=True)
    #END mousePressEvent()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.setStyleSheet('background-color: rgb(60,60,60)')
            sender = self
            for frame in self.framelist:
                if not self == frame:
                    frame.setStyleSheet('background-color: rgb(50,50,50)')
                else:
                    sender = self
            return sender
        if event.button() == QtCore.Qt.RightButton:
            self.setStyleSheet('background-color: rgb(50,50,50)')
            return self
    #END mouseReleaseEvent()
#END FrameGuide()


class EditButton(QtGui.QPushButton):
    def __init__(self, parent):
        super(EditButton, self).__init__(parent)
        self.setText('Edit')
        self.parent = parent
    #END __init__()

    def mousePressEvent(self, event):
        pass
    #END mousePressEvent()

    def mouseReleaseEvent(self, event):
        try:
            if cmds.window(self.win.objectName(), query=True, exists=True):
                self.win.close()
                self.win.deleteLater()
        except:
            pass
        self.win = ui_settings.SettingsUI(parent=self.parent,
                                          button='Edit', lock=True)
        if isinstance(self.parent.rigdata, list):
            self.win.apply_data(self.parent.rigdata[0])
        else:
            self.win.apply_data(self.parent.rigdata)
        self.win.show()
        self.win.create_btn.clicked.connect(self.create_frame)
    #END mouseReleaseEvent()

    def create_frame(self):
        self.win.data = self.win.get_data()
        if self.win.data:
            self.parent.objname = (self.win.data['moduleType'] + ': ' +
                                   self.win.data['side'].upper() + '_' +
                                   self.win.data['moduleName'].upper() + '_MOD')
            self.parent.txt.setText(self.parent.objname)
            if isinstance(self.parent.rigdata, list):
                self.parent.rigdata = [self.win.data, self.parent.rigdata[1]]
            else:
                self.parent.rigdata = self.win.data
    #END create_frame()
#END EditButton()


class MirrorButton(QtGui.QPushButton):
    def __init__(self, parent):
        super(MirrorButton, self).__init__(parent)
        self.setText('Mirror')
        self.parent = parent
    #END __init__()

    def mousePressEvent(self, event):
        pass
    #END mousePressEvent()

    def mouseReleaseEvent(self, event):
        try:
            self.parent.rigdata[1]['amount'] = self.parent.rigdata[0]['amount']
        except:
            pass
        try:
            if cmds.window(self.win.objectName(), query=True, exists=True):
                self.win.close()
                self.win.deleteLater()
        except:
            pass
        self.win = ui_settings.SettingsUI(parent=self.parent,
                                          button='Edit Mirror',
                                          lock=True, mirror=True)
        self.win.apply_data(self.parent.rigdata[1])
        self.win.show()
        self.win.create_btn.clicked.connect(self.create_frame)
    #END mouseReleaseEvent()

    def create_frame(self):
        self.win.data = self.win.get_data()
        if self.win.data:
            try:
                self.win.data['amount'] = self.parent.rigdata[0]['amount']
            except:
                pass
            self.parent.rigdata = [self.parent.rigdata[0], self.win.data]
    #END create_frame()
#END MirrorButton()


class RemoveButton(QtGui.QPushButton):
    def __init__(self, parent, grandparent):
        super(RemoveButton, self).__init__(parent)
        self.setText('Remove')
        self.parent = parent
        self.grandparent = grandparent
    #END __init__()

    def mousePressEvent(self, event):
        pass
    #END mousePressEvent()

    def mouseReleaseEvent(self, event):
        self.clear_layout(self.grandparent.rig_lay)
    #END mouseReleaseEvent()

    def clear_layout(self, layout):
        if layout:
            index = 0
            if not self.grandparent.framelist:
                return
            for num, i in enumerate(self.grandparent.framelist):
                if i == self.parent:
                    index = layout.indexOf(i)
                    item = layout.takeAt(index)
                    item.widget().deleteLater()
                    self.grandparent.framelist.pop(num)
#END RemoveButton()


class MoveButton(QtGui.QPushButton):
    def __init__(self, parent, name, up):
        super(MoveButton, self).__init__(parent)
        self.setText(name)
        self.parent = parent
        self.up = up

        #--- vars
        self.check = 0
        self.frameSelected = list()
    #END __init__()

    def mousePressEvent(self, event):
        self.check = 0
        for index, i in enumerate(self.parent.framelist):
            if i.styleSheet() == 'background-color: rgb(60,60,60)':
                self.frameSelected = [i, index]
                self.check = 1
    #END mousePressEvent()

    def mouseReleaseEvent(self, event):
        if not self.check:
            return

        index = self.frameSelected[1]
        if self.up:
            if not index:
                self.parent.frame_layout.insertWidget(0, self.frameSelected[0])
            else:
                self.parent.frame_layout.insertWidget(index - 1, self.frameSelected[0])
                self.parent.framelist.pop(index)
                self.parent.framelist.insert(index - 1, self.frameSelected[0])
        else:
            if index == len(self.parent.framelist):
                self.parent.frame_layout.insertWidget(len(self.parent.framelist),
                                                      self.frameSelected[0])
            else:
                self.parent.frame_layout.insertWidget(index + 1, self.frameSelected[0])
                self.parent.framelist.pop(index)
                self.parent.framelist.insert(index + 1, self.frameSelected[0])
    #END mouseReleaseEvent()
#END MoveButton()


def get_config_file():
    envpath = get_project_path()
    assert envpath, 'Please set MAYA_PLUGIN_PATH to PandorasBox in Maya.env'
    config_path = os.path.join(envpath, 'ASSET_DATA_PATH.config')
    if os.path.exists(config_path):
        with open(config_path) as json_file:
            json_data = json.load(json_file)
            return json_data.values()[0]
#END get_config_file()


def get_latest_release(project=None,
                       assetType=None,
                       assetName=None,
                       resolution=None):
    path = get_config_file()
    #--- define paths
    project_path = os.path.join(path, project)
    asset_type_path = os.path.join(project_path, assetType)
    asset_name_path = os.path.join(asset_type_path, assetName)
    asset_res_path = os.path.join(asset_name_path, resolution)
    asset_dpt_path = os.path.join(asset_res_path, 'modeling')
    asset_status_path = os.path.join(asset_dpt_path, 'release')
    #--- check and create paths
    #--- project path
    if not os.path.exists(project_path):
        return
    #--- assetType path
    if not os.path.exists(asset_type_path):
        return
    #--- assetName path
    if not os.path.exists(asset_name_path):
        return
    #--- assetRes path
    if not os.path.exists(asset_res_path):
        return
    #--- assetDpt path
    if not os.path.exists(asset_dpt_path):
        return
    #--- assetRelease path
    if not os.path.exists(asset_status_path):
        return
    result = os.listdir(asset_status_path)
    result.reverse()
    asset_path = os.path.join(asset_status_path, result[0])
    return asset_path
#END get_latest_release()
