"""
This is the ui for the infoBox
"""

import os
import sys
from PySide import QtGui, QtCore
from maya import cmds, OpenMaya
from tools import infoBox

sys.path.append('C:\Users\Isaac Clark\Documents\GitHub\AutoRigger')
from tools.shotFinaling.ui import pysideconvenience
uifilepath = 'C:/Users/Isaac Clark/Documents/GitHub/AutoRigger/tools/infoBox/ui/infobox.ui'
form_class, base_class = pysideconvenience.load_ui_type(uifilepath)


class InfoBoxUI(base_class, form_class):
    '''
    This displays a ui for the infoBox tool.
    '''
    def __init__(self, parent=pysideconvenience.get_maya_window()):
        super(InfoBoxUI, self).__init__(parent)
        self.setupUi(self)

        #vars
        self.world = 0
        self.selection = 0
        self.list = 0

        #methods
        self.__setup()
    #END def __init__()

    def connect_signals(self):
        #--- this method connects the signals
        self.connect(self.translation_BTN, QtCore.SIGNAL('released()'), self.get_translation)
        self.connect(self.rotation_BTN, QtCore.SIGNAL('released()'), self.get_rotation)
        self.connect(self.scale_BTN, QtCore.SIGNAL('released()'), self.get_scale)
    #END def connect_signals()

    def get_checkbox_info(self):
        #--- this method checks the state of the checkboxes
        #--- world space
        if self.worldspace_BOX.isChecked():
            self.world = 1
        else:
            self.world = 0
        #--- print selection
        if self.selection_BOX.isChecked():
            self.selection = 1    
        else:
            self.selection = 0
        #--- append to lists
        if self.list_BOX.isChecked():
            self.list = 1
        else:
            self.list = 0    
        #END def get_checkbox_info()

    def get_translation(self):
        #--- this method gets the translation values
        #--- check the checkboxes
        self.get_checkbox_info()        
        #--- get the selection
        sel = cmds.ls(selection=True)
        #--- get the proper information
        names = list()
        position = list()
        print 'TRANSLATION:'
        for i in sel:
            if cmds.nodeType(i) == 'mesh' or cmds.nodeType(i) == 'nurbsCurve' or cmds.nodeType(i) == 'nurbs':
                self.get_component_position(i)
                return
            elif cmds.nodeType(i) != 'transform':
                raise Exception('Selection has to be a transform node or a mesh!')
            pos = cmds.xform(i, query=True, translation=True, worldSpace=self.world)
            if self.list:
                if self.selection:
                    names.append(i)
                position.append(pos)
            else:
                if self.selection:
                    print i, pos
                else:
                    print pos
        if self.list:
            if self.selection:
                print names
            print position
    #END def get_translation()

    def get_rotation(self):
        #--- this method gets the rotation values
        #--- check the checkboxes
        self.get_checkbox_info()        
        #--- get the selection
        sel = cmds.ls(selection=True)
        #--- get the proper information
        names = list()
        position = list()
        print 'ROTATION:'
        for i in sel:
            pos = cmds.xform(i, query=True, rotation=True, worldSpace=self.world)
            if self.list:
                if self.selection:
                    names.append(i)
                position.append(pos)
            else:
                if self.selection:
                    print i, pos
                else:
                    print pos
        if self.list:
            if self.selection:
                print names
            print position
    #END def get_rotation()

    def get_scale(self):
        #--- this method gets the scale values
        #--- check the checkboxes
        self.get_checkbox_info()        
        #--- get the selection
        sel = cmds.ls(selection=True)
        #--- get the proper information
        names = list()
        position = list()
        print 'SCALE:'
        for i in sel:
            pos = cmds.xform(i, query=True, scale=True, relative=True, worldSpace=self.world)
            if self.list:
                if self.selection:
                    names.append(i)
                position.append(pos)
            else:
                if self.selection:
                    print i, pos
                else:
                    print pos
        if self.list:
            if self.selection:
                print names
            print position
    #END def get_scale()

    def get_component_position(self, comp=None):
        #--- this method gets the vertex position of the selection
        if comp:
            comps = cmds.ls(comp, flatten=True)
            names = list()
            position = list()
            #--- check the checkboxes
            self.get_checkbox_info()
            print 'COMPONENTS:'
            for i in comps:
                pos = cmds.xform(i, query=True, translation=True, worldSpace=self.world)
                if self.list:
                    if self.selection:
                        names.append(i)
                    position.append(pos)
                else:
                    if self.selection:
                        print i, pos
                    else:
                        print pos
            if self.list:
                if self.selection:
                    print names
                print position
    #END def get_component_position

    def __setup(self):
        #--- this method setups the ui
        #--- connect signals
        self.connect_signals()
    #END def __setup()
#END class InfoBoxUI()


def main():
    global et_win
    try:
        et_win.close()
    except:
        pass
    et_win = InfoBoxUI()
    et_win.show()
#END def main
