'''
@author:  etekinalp
@date:    Aug 26, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module creates a Quaternion node
'''


from maya import cmds
from goe_plugins import plugin_master
reload(plugin_master)


class Quaternions(plugin_master.PluginSetup):
    def __init__(self, plugin="quaternions"):
        super(Quaternions, self).__init__(plugin=plugin, suffix="so",
                                          update=True, info=True)
        #--- args
        self._plugin = plugin

        #--- methods
        self.__create()
    #END __init__()

    def __setup_plugin(self):
        quaternion = cmds.createNode(self._plugin)
        loc = cmds.spaceLocator()[0]
        obj = cmds.polySphere()[0]
        cmds.connectAttr(loc + ".worldMatrix", quaternion + ".inMatrix")
        cmds.connectAttr(quaternion + ".outTranslate", obj + ".translate")
        cmds.connectAttr(quaternion + ".outRotate", obj + ".rotate")
    #END __setup_plugin()

    def __create(self):
        self.__setup_plugin()
    #END __create()
#END Quaternions()

Quaternions()
