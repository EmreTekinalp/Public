'''
@author:  etekinalp
@date:    Aug 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module stores all the goe plugins
'''


from maya import OpenMayaMPx

from goe_plugins import goe_locator
from goe_plugins import goe_mirror
from goe_functions import menu

reload(menu)


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "GravityOfExplosion", "1.0", "Any")
    try:
        plugin.registerUI(menu.create_menu, menu.remove_menu)
    except:
        raise Exception("Failed to load UI: GOE Tools")

    try:
        plugin.registerNode(goe_locator.nodename, goe_locator.nodeid,
                            goe_locator.nodeCreator, goe_locator.nodeInitializer,
                            OpenMayaMPx.MPxNode.kLocatorNode)
    except:
        raise Exception("Failed to load plugin: " + `goe_locator.nodename`)

    try:
        plugin.registerNode(goe_mirror.nodeName, goe_mirror.nodeId,
                            goe_mirror.nodeCreator, goe_mirror.nodeInitializer,
                            OpenMayaMPx.MPxNode.kDependNode)
    except:
        raise Exception("Failed to load plugin: " + `goe_mirror.nodeName`)
    return
# END initializePlugin()


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(goe_locator.nodeid)
    except:
        raise Exception("Failed to unload plugin: " + `goe_locator.nodename`)

    try:
        plugin.deregisterNode(goe_mirror.nodeId)
    except:
        raise Exception("Failed to unload plugin: " + `goe_mirror.nodeName`)
    return
# END uninitializePlugin()
