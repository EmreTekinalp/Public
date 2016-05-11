'''
@author:  etekinalp
@date:    Sep 5, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates the PandorasBox menu in maya
'''


from maya import cmds, mel
from goe_functions import data
from goe_ui.pandoras_box import ui_pandorasbox as pbui
from goe_ui.asset_manager import ui as amui
reload(data)


def create_menu():
    #--- set MayaWindow as parent
    gMainWindow = mel.eval('$tempVar = $gMainWindow')
    cmds.setParent(gMainWindow)
    #--- create the PandorasBox menu and the menuItems
    pb = cmds.menu(label="GOE Tools", tearOff=True)
    cmds.menuItem(pb, label="PandorasBox", command=pbui.main)
    cmds.menuItem(pb, divider=True)
    cmds.menuItem(pb, label="Asset Manager", command=amui.main)
    cmds.menuItem(pb, divider=True)
    cmds.menuItem(pb, label="Help")

def remove_menu():
    gMainWindow = mel.eval('$tempVar = $gMainWindow')
    m = cmds.window( gMainWindow, query=True, menuArray=True)
    pb = None
    for i in m:
        l = cmds.menu(i, query=True, label=True)
        if l == "GOE Tools":
            pb = i
    if cmds.menu(pb, exists=True):
        cmds.deleteUI(pb, menu=True)
